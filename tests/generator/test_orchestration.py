"""Tests for generator preflight and root Work Item lifecycle coordination."""

from __future__ import annotations

import pytest

from azure_devops_backlog_generator.azure_devops.exceptions import (
    AzureDevOpsCompatibilityError,
    AzureDevOpsHttpError,
    AzureDevOpsTransportError,
)
from azure_devops_backlog_generator.azure_devops.models import (
    AzureDevOpsProject,
    AzureDevOpsWorkItem,
)
from azure_devops_backlog_generator.documentation.models import (
    DocumentationHierarchy,
    HeadingIdentity,
    ParsedDocument,
    SemanticWorkItem,
    WorkItemType,
)
from azure_devops_backlog_generator.generator.candidates import WorkItemCandidate
from azure_devops_backlog_generator.generator.identity import SourceIdentityValidationError
from azure_devops_backlog_generator.generator.orchestration import (
    PreflightState,
    coordinate_full_preflight,
    coordinate_root_work_item_lifecycle,
)


class _RootLifecycleRestClient:
    """Small observable fake for root lifecycle composition."""

    def __init__(
        self,
        *,
        work_item_ids: tuple[int, ...],
        existing_work_item: AzureDevOpsWorkItem | None = None,
        created_work_item: AzureDevOpsWorkItem | None = None,
        lookup_error: Exception | None = None,
        create_error: Exception | None = None,
    ) -> None:
        self.work_item_ids = work_item_ids
        self.existing_work_item = existing_work_item
        self.created_work_item = created_work_item
        self.lookup_error = lookup_error
        self.create_error = create_error
        self.lookup_calls: list[tuple[WorkItemCandidate, str]] = []
        self.retrieve_calls: list[tuple[int, str]] = []
        self.create_calls: list[tuple[WorkItemCandidate, str]] = []
        self.relationship_state_calls = 0
        self.relationship_patch_calls = 0

    def lookup_work_item_ids(
        self, candidate: WorkItemCandidate, *, personal_access_token: str
    ) -> tuple[int, ...]:
        self.lookup_calls.append((candidate, personal_access_token))
        if self.lookup_error is not None:
            raise self.lookup_error
        return self.work_item_ids

    def retrieve_work_item(
        self, work_item_id: int, *, personal_access_token: str
    ) -> AzureDevOpsWorkItem:
        self.retrieve_calls.append((work_item_id, personal_access_token))
        assert self.existing_work_item is not None
        return self.existing_work_item

    def create_work_item(
        self, candidate: WorkItemCandidate, *, personal_access_token: str
    ) -> AzureDevOpsWorkItem:
        self.create_calls.append((candidate, personal_access_token))
        if self.create_error is not None:
            raise self.create_error
        assert self.created_work_item is not None
        return self.created_work_item

    def retrieve_work_item_relationship_state(self, *args: object, **kwargs: object) -> None:
        self.relationship_state_calls += 1
        raise AssertionError("Root coordination must not retrieve relationship state.")

    def patch_parent_child_relationship(self, *args: object, **kwargs: object) -> None:
        self.relationship_patch_calls += 1
        raise AssertionError("Root coordination must not patch a relationship.")


def _candidate() -> WorkItemCandidate:
    return WorkItemCandidate(
        work_item_type=WorkItemType.EPIC,
        title="Prepared root title",
        description_html="<p>Prepared root description</p>\n",
        acceptance_criteria_html=None,
        tags_value=None,
        source_identity="adbg:source-id:v1:sha256:" + "a" * 64,
    )


def _project() -> AzureDevOpsProject:
    return AzureDevOpsProject(id="project-id", name="Canonical Project")


def _work_item(*, revision: int = 3) -> AzureDevOpsWorkItem:
    return AzureDevOpsWorkItem(
        id=17,
        revision=revision,
        project_name="Canonical Project",
        work_item_type="Epic",
        source_identity="adbg:source-id:v1:sha256:" + "a" * 64,
    )


def test_creates_a_new_root_once_and_returns_only_its_id() -> None:
    candidate = _candidate()
    rest_client = _RootLifecycleRestClient(work_item_ids=(), created_work_item=_work_item())

    assert (
        coordinate_root_work_item_lifecycle(
            candidate,
            _project(),
            rest_client,  # type: ignore[arg-type]
            personal_access_token="secret-pat",
        )
        == 17
    )

    assert rest_client.lookup_calls == [(candidate, "secret-pat")]
    assert rest_client.retrieve_calls == []
    assert rest_client.create_calls == [(candidate, "secret-pat")]
    assert rest_client.relationship_state_calls == 0
    assert rest_client.relationship_patch_calls == 0


def test_reuses_a_validated_root_without_creating_it() -> None:
    candidate = _candidate()
    rest_client = _RootLifecycleRestClient(work_item_ids=(17,), existing_work_item=_work_item())

    assert (
        coordinate_root_work_item_lifecycle(
            candidate,
            _project(),
            rest_client,  # type: ignore[arg-type]
            personal_access_token="secret-pat",
        )
        == 17
    )

    assert rest_client.lookup_calls == [(candidate, "secret-pat")]
    assert rest_client.retrieve_calls == [(17, "secret-pat")]
    assert rest_client.create_calls == []
    assert rest_client.relationship_state_calls == 0
    assert rest_client.relationship_patch_calls == 0


def test_propagates_resolution_failure_without_creating_a_root() -> None:
    failure = AzureDevOpsHttpError(503)
    rest_client = _RootLifecycleRestClient(work_item_ids=(), lookup_error=failure)

    with pytest.raises(AzureDevOpsHttpError) as raised:
        coordinate_root_work_item_lifecycle(
            _candidate(),
            _project(),
            rest_client,  # type: ignore[arg-type]
            personal_access_token="secret-pat",
        )

    assert raised.value is failure
    assert rest_client.create_calls == []
    assert rest_client.relationship_state_calls == 0
    assert rest_client.relationship_patch_calls == 0


def test_propagates_create_failure_without_retry_or_relationship_work() -> None:
    failure = AzureDevOpsTransportError("Create failed")
    rest_client = _RootLifecycleRestClient(work_item_ids=(), create_error=failure)

    with pytest.raises(AzureDevOpsTransportError) as raised:
        coordinate_root_work_item_lifecycle(
            _candidate(),
            _project(),
            rest_client,  # type: ignore[arg-type]
            personal_access_token="secret-pat",
        )

    assert raised.value is failure
    assert len(rest_client.lookup_calls) == 1
    assert len(rest_client.create_calls) == 1
    assert rest_client.retrieve_calls == []
    assert rest_client.relationship_state_calls == 0
    assert rest_client.relationship_patch_calls == 0


class _PreflightRestClient:
    """Observable fake that permits only approved preflight REST operations."""

    def __init__(
        self,
        *,
        project_error: Exception | None = None,
        work_item_type_error: Exception | None = None,
        validation_error: Exception | None = None,
    ) -> None:
        self.project_error = project_error
        self.work_item_type_error = work_item_type_error
        self.validation_error = validation_error
        self.events: list[str] = []
        self.validated_candidates: list[WorkItemCandidate] = []
        self._validation_attempts = 0

    def retrieve_project(self, *, personal_access_token: str) -> AzureDevOpsProject:
        self.events.append("project")
        if self.project_error is not None:
            raise self.project_error
        return AzureDevOpsProject(id="project-id", name="Canonical Project")

    def retrieve_work_item_type(
        self, work_item_type: WorkItemType, *, personal_access_token: str
    ) -> dict[str, object]:
        self.events.append(f"type:{work_item_type.value}")
        if self.work_item_type_error is not None:
            raise self.work_item_type_error
        return {"evidence": True}

    def retrieve_work_item_type_field(
        self,
        work_item_type: WorkItemType,
        field_reference: str,
        *,
        personal_access_token: str,
    ) -> dict[str, object]:
        self.events.append(f"type-field:{work_item_type.value}:{field_reference}")
        evidence: dict[str, object] = {"referenceName": field_reference}
        if field_reference == "Custom.BacklogGeneratorSourceIdentity":
            evidence.update({"defaultValue": None, "alwaysRequired": False})
        return evidence

    def retrieve_field(
        self, field_reference: str, *, personal_access_token: str
    ) -> dict[str, object]:
        self.events.append(f"field:{field_reference}")
        evidence: dict[str, object] = {"referenceName": field_reference}
        if field_reference == "Custom.BacklogGeneratorSourceIdentity":
            evidence.update(
                {
                    "name": "Backlog Generator Source Identity",
                    "type": "String",
                    "readOnly": False,
                }
            )
        return evidence

    def validate_work_item_create(
        self, candidate: WorkItemCandidate, *, personal_access_token: str
    ) -> None:
        self.events.append(f"validate:{candidate.title}")
        self.validated_candidates.append(candidate)
        self._validation_attempts += 1
        if self.validation_error is not None and self._validation_attempts == 2:
            raise self.validation_error

    def lookup_work_item_ids(self, *args: object, **kwargs: object) -> None:
        raise AssertionError("Preflight must not perform WIQL lookup.")

    def retrieve_work_item(self, *args: object, **kwargs: object) -> None:
        raise AssertionError("Preflight must not retrieve existing Work Item evidence.")

    def create_work_item(self, *args: object, **kwargs: object) -> None:
        raise AssertionError("Preflight must not persist a Work Item.")

    def retrieve_work_item_relationship_state(self, *args: object, **kwargs: object) -> None:
        raise AssertionError("Preflight must not retrieve relationship state.")

    def patch_parent_child_relationship(self, *args: object, **kwargs: object) -> None:
        raise AssertionError("Preflight must not patch a relationship.")


def _preflight_item(
    work_item_type: WorkItemType,
    title: str,
    path: str,
    hierarchy: tuple[HeadingIdentity, ...],
    source_order: int,
    *,
    children: tuple[SemanticWorkItem, ...] = (),
    acceptance_criteria_html: str | None = "<ul>\n<li>Criterion</li>\n</ul>\n",
    tags_value: str | None = "platform",
) -> SemanticWorkItem:
    return SemanticWorkItem(
        work_item_type=work_item_type,
        level=hierarchy[-1].level,
        title=title,
        canonical_relative_path=path,
        heading_hierarchy=hierarchy,
        source_order=source_order,
        description_html=f"<p>{title}</p>\n",
        acceptance_criteria_html=acceptance_criteria_html,
        tags_value=tags_value,
        direct_body_token_spans=(),
        children=children,
    )


def _preflight_hierarchy(*documents: ParsedDocument) -> DocumentationHierarchy:
    return DocumentationHierarchy(documents=documents)


def _document(path: str, *roots: SemanticWorkItem) -> ParsedDocument:
    return ParsedDocument(canonical_relative_path=path, tokens=(), root_items=roots)


def _complete_preflight_hierarchy() -> DocumentationHierarchy:
    task = _preflight_item(
        WorkItemType.TASK,
        "Task",
        "first.md",
        (
            HeadingIdentity(1, "Epic"),
            HeadingIdentity(2, "Feature"),
            HeadingIdentity(3, "PBI"),
            HeadingIdentity(4, "Task"),
        ),
        3,
        acceptance_criteria_html=None,
        tags_value=None,
    )
    pbi = _preflight_item(
        WorkItemType.PRODUCT_BACKLOG_ITEM,
        "PBI",
        "first.md",
        (HeadingIdentity(1, "Epic"), HeadingIdentity(2, "Feature"), HeadingIdentity(3, "PBI")),
        2,
        children=(task,),
        acceptance_criteria_html=None,
    )
    feature = _preflight_item(
        WorkItemType.FEATURE,
        "Feature",
        "first.md",
        (HeadingIdentity(1, "Epic"), HeadingIdentity(2, "Feature")),
        1,
        children=(pbi,),
    )
    epic = _preflight_item(
        WorkItemType.EPIC,
        "Epic",
        "first.md",
        (HeadingIdentity(1, "Epic"),),
        0,
        children=(feature,),
    )
    second_epic = _preflight_item(
        WorkItemType.EPIC,
        "Second Epic",
        "second.md",
        (HeadingIdentity(1, "Second Epic"),),
        0,
        acceptance_criteria_html=None,
        tags_value=None,
    )
    return _preflight_hierarchy(_document("first.md", epic), _document("second.md", second_epic))


def test_coordinates_complete_preflight_in_source_order_and_returns_minimal_state() -> None:
    hierarchy = _complete_preflight_hierarchy()
    rest_client = _PreflightRestClient()

    state = coordinate_full_preflight(
        hierarchy, rest_client, personal_access_token="secret-pat"  # type: ignore[arg-type]
    )

    assert isinstance(state, PreflightState)
    assert state.hierarchy is hierarchy
    assert state.project == AzureDevOpsProject(id="project-id", name="Canonical Project")
    assert [candidate.title for candidate in state.candidates] == [
        "Epic",
        "Feature",
        "PBI",
        "Task",
        "Second Epic",
    ]
    assert rest_client.validated_candidates == list(state.candidates)
    assert rest_client.events[0] == "project"
    assert rest_client.events[1:5] == [
        "type:Epic",
        "type:Feature",
        "type:Product Backlog Item",
        "type:Task",
    ]
    assert rest_client.events[-5:] == [
        "validate:Epic",
        "validate:Feature",
        "validate:PBI",
        "validate:Task",
        "validate:Second Epic",
    ]


def test_validation_checks_each_same_type_candidate_with_its_actual_optional_values() -> None:
    first = _preflight_item(
        WorkItemType.EPIC,
        "First",
        "input.md",
        (HeadingIdentity(1, "First"),),
        0,
        acceptance_criteria_html=None,
        tags_value=None,
    )
    second = _preflight_item(
        WorkItemType.EPIC,
        "Second",
        "input.md",
        (HeadingIdentity(1, "Second"),),
        1,
    )
    rest_client = _PreflightRestClient()

    coordinate_full_preflight(
        _preflight_hierarchy(_document("input.md", first, second)),
        rest_client,  # type: ignore[arg-type]
        personal_access_token="secret-pat",
    )

    assert [candidate.title for candidate in rest_client.validated_candidates] == [
        "First",
        "Second",
    ]
    assert rest_client.validated_candidates[0].acceptance_criteria_html is None
    assert rest_client.validated_candidates[0].tags_value is None
    assert rest_client.validated_candidates[1].acceptance_criteria_html is not None


def test_source_identity_failure_prevents_all_rest_activity() -> None:
    first = _preflight_item(
        WorkItemType.EPIC, "Same", "input.md", (HeadingIdentity(1, "Same"),), 0
    )
    duplicate = _preflight_item(
        WorkItemType.EPIC, "Same", "input.md", (HeadingIdentity(1, "Same"),), 1
    )
    rest_client = _PreflightRestClient()

    with pytest.raises(SourceIdentityValidationError, match="Source identity validation failed"):
        coordinate_full_preflight(
            _preflight_hierarchy(_document("input.md", first, duplicate)),
            rest_client,  # type: ignore[arg-type]
            personal_access_token="secret-pat",
        )

    assert rest_client.events == []


def test_project_failure_propagates_once_without_later_preflight_requests() -> None:
    failure = AzureDevOpsHttpError(503)
    rest_client = _PreflightRestClient(project_error=failure)

    with pytest.raises(AzureDevOpsHttpError) as raised:
        coordinate_full_preflight(
            _complete_preflight_hierarchy(),
            rest_client,  # type: ignore[arg-type]
            personal_access_token="secret-pat",
        )

    assert raised.value is failure
    assert rest_client.events == ["project"]


def test_metadata_failure_propagates_without_later_metadata_or_validation_requests() -> None:
    failure = AzureDevOpsHttpError(503)
    rest_client = _PreflightRestClient(work_item_type_error=failure)

    with pytest.raises(AzureDevOpsHttpError) as raised:
        coordinate_full_preflight(
            _complete_preflight_hierarchy(),
            rest_client,  # type: ignore[arg-type]
            personal_access_token="secret-pat",
        )

    assert raised.value is failure
    assert rest_client.events == ["project", "type:Epic"]
    assert rest_client.validated_candidates == []


def test_compatibility_failure_prevents_every_validation_only_request(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    failure = AzureDevOpsCompatibilityError("Incompatible")
    rest_client = _PreflightRestClient()
    monkeypatch.setattr(
        "azure_devops_backlog_generator.generator.orchestration.evaluate_structural_scrum_compatibility",
        lambda evidence: (_ for _ in ()).throw(failure),
    )

    with pytest.raises(AzureDevOpsCompatibilityError) as raised:
        coordinate_full_preflight(
            _complete_preflight_hierarchy(),
            rest_client,  # type: ignore[arg-type]
            personal_access_token="secret-pat",
        )

    assert raised.value is failure
    assert rest_client.validated_candidates == []
    assert not any(event.startswith("validate:") for event in rest_client.events)


def test_validation_failure_stops_after_the_failing_candidate_without_retry() -> None:
    failure = AzureDevOpsTransportError("Validation failed")
    rest_client = _PreflightRestClient(validation_error=failure)

    with pytest.raises(AzureDevOpsTransportError) as raised:
        coordinate_full_preflight(
            _complete_preflight_hierarchy(),
            rest_client,  # type: ignore[arg-type]
            personal_access_token="secret-pat",
        )

    assert raised.value is failure
    assert [candidate.title for candidate in rest_client.validated_candidates] == [
        "Epic",
        "Feature",
    ]
    assert rest_client.events[-2:] == ["validate:Epic", "validate:Feature"]
