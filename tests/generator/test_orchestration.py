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
    AzureDevOpsWorkItemRelationshipState,
)
from azure_devops_backlog_generator.documentation.models import (
    DocumentationHierarchy,
    HeadingIdentity,
    ParsedDocument,
    SemanticWorkItem,
    WorkItemType,
)
from azure_devops_backlog_generator.generator.candidates import (
    WorkItemCandidate,
    build_work_item_candidate,
)
from azure_devops_backlog_generator.generator.identity import SourceIdentityValidationError
from azure_devops_backlog_generator.generator.orchestration import (
    PreflightState,
    coordinate_deterministic_hierarchy_traversal,
    coordinate_full_preflight,
    coordinate_root_work_item_lifecycle,
)
from azure_devops_backlog_generator.generator.relationships import (
    ConflictingReusedChildRelationshipError,
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


class _TraversalRestClient:
    """Observable REST boundary for deterministic traversal composition."""

    def __init__(
        self,
        *,
        existing_titles: set[str] | None = None,
        relationship_parent_ids: dict[str, tuple[int, ...]] | None = None,
        relationship_state_error_title: str | None = None,
        resolution_error_title: str | None = None,
        create_error_title: str | None = None,
        patch_error_title: str | None = None,
    ) -> None:
        self.existing_titles = existing_titles or set()
        self.relationship_parent_ids = relationship_parent_ids or {}
        self.relationship_state_error_title = relationship_state_error_title
        self.resolution_error_title = resolution_error_title
        self.create_error_title = create_error_title
        self.patch_error_title = patch_error_title
        self.events: list[str] = []
        self.lookup_candidates: list[WorkItemCandidate] = []
        self.create_candidates: list[WorkItemCandidate] = []
        self._work_items: dict[int, AzureDevOpsWorkItem] = {}
        self._ids_by_identity: dict[str, int] = {}
        self._titles_by_id: dict[int, str] = {}
        self._next_id = 10

    def lookup_work_item_ids(
        self, candidate: WorkItemCandidate, *, personal_access_token: str
    ) -> tuple[int, ...]:
        self.events.append(f"resolve:{candidate.title}")
        self.lookup_candidates.append(candidate)
        if candidate.title == self.resolution_error_title:
            raise AzureDevOpsTransportError("Resolution failed")
        if candidate.title not in self.existing_titles:
            return ()
        return (self._ensure_work_item(candidate).id,)

    def retrieve_work_item(
        self, work_item_id: int, *, personal_access_token: str
    ) -> AzureDevOpsWorkItem:
        self.events.append(f"get:{work_item_id}")
        return self._work_items[work_item_id]

    def create_work_item(
        self, candidate: WorkItemCandidate, *, personal_access_token: str
    ) -> AzureDevOpsWorkItem:
        self.events.append(f"create:{candidate.title}")
        self.create_candidates.append(candidate)
        if candidate.title == self.create_error_title:
            raise AzureDevOpsTransportError("Create failed")
        return self._ensure_work_item(candidate)

    def retrieve_work_item_relationship_state(
        self, child_work_item_id: int, *, personal_access_token: str
    ) -> AzureDevOpsWorkItemRelationshipState:
        work_item = self._work_items[child_work_item_id]
        self.events.append(f"relationship-get:{work_item.work_item_type}")
        if self._titles_by_id[child_work_item_id] == self.relationship_state_error_title:
            raise AzureDevOpsTransportError("Relationship-state GET failed")
        return AzureDevOpsWorkItemRelationshipState(
            revision=8,
            reverse_parent_ids=self.relationship_parent_ids.get(work_item.source_identity, ()),
        )

    def patch_parent_child_relationship(
        self,
        parent_work_item_id: int,
        child_work_item_id: int,
        child_revision: int,
        *,
        personal_access_token: str,
    ) -> None:
        child_title = self._titles_by_id[child_work_item_id]
        self.events.append(f"patch:{child_title}")
        if child_title == self.patch_error_title:
            raise AzureDevOpsTransportError("Relationship PATCH failed")

    def retrieve_project(self, *args: object, **kwargs: object) -> None:
        raise AssertionError("Traversal must not retrieve the project.")

    def retrieve_work_item_type(self, *args: object, **kwargs: object) -> None:
        raise AssertionError("Traversal must not retrieve metadata.")

    def retrieve_work_item_type_field(self, *args: object, **kwargs: object) -> None:
        raise AssertionError("Traversal must not retrieve metadata.")

    def retrieve_field(self, *args: object, **kwargs: object) -> None:
        raise AssertionError("Traversal must not retrieve metadata.")

    def validate_work_item_create(self, *args: object, **kwargs: object) -> None:
        raise AssertionError("Traversal must not validate Work Item Create.")

    def _ensure_work_item(self, candidate: WorkItemCandidate) -> AzureDevOpsWorkItem:
        work_item_id = self._ids_by_identity.get(candidate.source_identity)
        if work_item_id is not None:
            return self._work_items[work_item_id]
        work_item_id = self._next_id
        self._next_id += 1
        work_item = AzureDevOpsWorkItem(
            id=work_item_id,
            revision=3,
            project_name="Canonical Project",
            work_item_type=candidate.work_item_type.value,
            source_identity=candidate.source_identity,
        )
        self._ids_by_identity[candidate.source_identity] = work_item_id
        self._work_items[work_item_id] = work_item
        self._titles_by_id[work_item_id] = candidate.title
        return work_item


def _traversal_state(hierarchy: DocumentationHierarchy) -> PreflightState:
    candidates = tuple(
        build_work_item_candidate(item)
        for document in hierarchy.documents
        for root in sorted(document.root_items, key=lambda item: item.source_order)
        for item in _source_order_subtree(root)
    )
    return PreflightState(hierarchy, _project(), candidates)


def _source_order_subtree(item: SemanticWorkItem) -> tuple[SemanticWorkItem, ...]:
    return (item,) + tuple(
        descendant
        for child in sorted(item.children, key=lambda child: child.source_order)
        for descendant in _source_order_subtree(child)
    )


def test_rejects_malformed_preflight_state_before_persistent_operations() -> None:
    hierarchy = _complete_preflight_hierarchy()
    state = PreflightState(hierarchy, _project(), ())
    rest_client = _TraversalRestClient()

    with pytest.raises(ValueError, match="semantic item count"):
        coordinate_deterministic_hierarchy_traversal(
            state, rest_client, personal_access_token="secret-pat"  # type: ignore[arg-type]
        )

    assert rest_client.events == []


def test_rejects_source_identity_mismatch_before_persistent_operations() -> None:
    state = _traversal_state(_complete_preflight_hierarchy())
    mismatched = WorkItemCandidate(
        state.candidates[0].work_item_type,
        state.candidates[0].title,
        state.candidates[0].description_html,
        state.candidates[0].acceptance_criteria_html,
        state.candidates[0].tags_value,
        "adbg:source-id:v1:sha256:" + "0" * 64,
    )
    rest_client = _TraversalRestClient()

    with pytest.raises(ValueError, match="semantic source identity"):
        coordinate_deterministic_hierarchy_traversal(
            PreflightState(state.hierarchy, state.project, (mismatched, *state.candidates[1:])),
            rest_client,  # type: ignore[arg-type]
            personal_access_token="secret-pat",
        )

    assert rest_client.events == []


def test_traverses_complete_new_hierarchy_in_parent_before_child_order(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_candidate_construction(item: SemanticWorkItem) -> WorkItemCandidate:
        raise AssertionError("Traversal must not rebuild candidates.")

    state = _traversal_state(_complete_preflight_hierarchy())
    rest_client = _TraversalRestClient()
    monkeypatch.setattr(
        "azure_devops_backlog_generator.generator.orchestration.build_work_item_candidate",
        fail_candidate_construction,
    )

    assert (
        coordinate_deterministic_hierarchy_traversal(
            state, rest_client, personal_access_token="secret-pat"  # type: ignore[arg-type]
        )
        is None
    )

    assert rest_client.events == [
        "resolve:Epic",
        "create:Epic",
        "resolve:Feature",
        "create:Feature",
        "patch:Feature",
        "resolve:PBI",
        "create:PBI",
        "patch:PBI",
        "resolve:Task",
        "create:Task",
        "patch:Task",
        "resolve:Second Epic",
        "create:Second Epic",
    ]
    assert rest_client.lookup_candidates == list(state.candidates)
    assert rest_client.create_candidates == list(state.candidates)
    assert all(
        actual is expected
        for actual, expected in zip(rest_client.lookup_candidates, state.candidates, strict=True)
    )
    assert all(
        actual is expected
        for actual, expected in zip(rest_client.create_candidates, state.candidates, strict=True)
    )


def test_reused_non_root_missing_relationship_repairs_before_descendant() -> None:
    task = _preflight_item(
        WorkItemType.TASK,
        "Task",
        "input.md",
        (
            HeadingIdentity(1, "Epic"),
            HeadingIdentity(2, "Feature"),
            HeadingIdentity(3, "PBI"),
            HeadingIdentity(4, "Task"),
        ),
        3,
        acceptance_criteria_html=None,
    )
    feature = _preflight_item(
        WorkItemType.FEATURE,
        "Feature",
        "input.md",
        (HeadingIdentity(1, "Epic"), HeadingIdentity(2, "Feature")),
        1,
        children=(task,),
    )
    epic = _preflight_item(
        WorkItemType.EPIC, "Epic", "input.md", (HeadingIdentity(1, "Epic"),), 0, children=(feature,)
    )
    state = _traversal_state(_preflight_hierarchy(_document("input.md", epic)))
    rest_client = _TraversalRestClient(existing_titles={"Epic", "Feature"})

    coordinate_deterministic_hierarchy_traversal(
        state, rest_client, personal_access_token="secret-pat"  # type: ignore[arg-type]
    )

    assert rest_client.events == [
        "resolve:Epic",
        "get:10",
        "resolve:Feature",
        "get:11",
        "relationship-get:Feature",
        "patch:Feature",
        "resolve:Task",
        "create:Task",
        "patch:Task",
    ]


def test_failure_stops_later_sibling_root_and_document() -> None:
    failing_feature = _preflight_item(
        WorkItemType.FEATURE,
        "Failing Feature",
        "first.md",
        (HeadingIdentity(1, "Root A"), HeadingIdentity(2, "Failing Feature")),
        1,
    )
    later_sibling = _preflight_item(
        WorkItemType.FEATURE,
        "Later Sibling",
        "first.md",
        (HeadingIdentity(1, "Root A"), HeadingIdentity(2, "Later Sibling")),
        2,
    )
    root_a = _preflight_item(
        WorkItemType.EPIC,
        "Root A",
        "first.md",
        (HeadingIdentity(1, "Root A"),),
        0,
        children=(failing_feature, later_sibling),
    )
    root_b = _preflight_item(
        WorkItemType.EPIC, "Root B", "first.md", (HeadingIdentity(1, "Root B"),), 3
    )
    root_c = _preflight_item(
        WorkItemType.EPIC, "Root C", "second.md", (HeadingIdentity(1, "Root C"),), 0
    )
    state = _traversal_state(
        _preflight_hierarchy(_document("first.md", root_a, root_b), _document("second.md", root_c))
    )
    rest_client = _TraversalRestClient(create_error_title="Failing Feature")

    with pytest.raises(AzureDevOpsTransportError, match="Create failed"):
        coordinate_deterministic_hierarchy_traversal(
            state, rest_client, personal_access_token="secret-pat"  # type: ignore[arg-type]
        )

    assert rest_client.events[-1] == "create:Failing Feature"
    assert "resolve:Later Sibling" not in rest_client.events
    assert "resolve:Root B" not in rest_client.events
    assert "resolve:Root C" not in rest_client.events


def test_empty_hierarchy_performs_no_persistent_operations() -> None:
    state = PreflightState(DocumentationHierarchy(documents=()), _project(), ())
    rest_client = _TraversalRestClient()

    assert (
        coordinate_deterministic_hierarchy_traversal(
            state, rest_client, personal_access_token="secret-pat"  # type: ignore[arg-type]
        )
        is None
    )
    assert rest_client.events == []


def test_empty_root_document_performs_no_persistent_operations() -> None:
    state = PreflightState(
        DocumentationHierarchy(documents=(_document("empty.md"),)), _project(), ()
    )
    rest_client = _TraversalRestClient()

    assert (
        coordinate_deterministic_hierarchy_traversal(
            state, rest_client, personal_access_token="secret-pat"  # type: ignore[arg-type]
        )
        is None
    )
    assert rest_client.events == []


def test_reuses_root_without_create_or_relationship_work() -> None:
    epic = _preflight_item(
        WorkItemType.EPIC, "Epic", "input.md", (HeadingIdentity(1, "Epic"),), 0
    )
    state = _traversal_state(_preflight_hierarchy(_document("input.md", epic)))
    rest_client = _TraversalRestClient(existing_titles={"Epic"})

    coordinate_deterministic_hierarchy_traversal(
        state, rest_client, personal_access_token="secret-pat"  # type: ignore[arg-type]
    )

    assert rest_client.events == ["resolve:Epic", "get:10"]
    assert rest_client.create_candidates == []


def test_correct_reused_non_root_allows_descendant_processing() -> None:
    task = _preflight_item(
        WorkItemType.TASK,
        "Task",
        "input.md",
        (
            HeadingIdentity(1, "Epic"),
            HeadingIdentity(2, "Feature"),
            HeadingIdentity(3, "PBI"),
            HeadingIdentity(4, "Task"),
        ),
        2,
        acceptance_criteria_html=None,
    )
    feature = _preflight_item(
        WorkItemType.FEATURE,
        "Feature",
        "input.md",
        (HeadingIdentity(1, "Epic"), HeadingIdentity(2, "Feature")),
        1,
        children=(task,),
    )
    epic = _preflight_item(
        WorkItemType.EPIC, "Epic", "input.md", (HeadingIdentity(1, "Epic"),), 0, children=(feature,)
    )
    state = _traversal_state(_preflight_hierarchy(_document("input.md", epic)))
    rest_client = _TraversalRestClient(
        existing_titles={"Epic", "Feature"},
        relationship_parent_ids={state.candidates[1].source_identity: (10,)},
    )

    coordinate_deterministic_hierarchy_traversal(
        state, rest_client, personal_access_token="secret-pat"  # type: ignore[arg-type]
    )

    assert rest_client.events[-3:] == ["resolve:Task", "create:Task", "patch:Task"]
    assert "patch:Feature" not in rest_client.events


def test_conflicting_reused_non_root_stops_descendant_and_later_work() -> None:
    state = _traversal_state(_complete_preflight_hierarchy())
    rest_client = _TraversalRestClient(
        existing_titles={"Epic", "Feature"},
        relationship_parent_ids={state.candidates[1].source_identity: (99,)},
    )

    with pytest.raises(
        ConflictingReusedChildRelationshipError,
        match="Reused-child relationship conflict",
    ):
        coordinate_deterministic_hierarchy_traversal(
            state, rest_client, personal_access_token="secret-pat"  # type: ignore[arg-type]
        )

    assert "resolve:PBI" not in rest_client.events
    assert "resolve:Second Epic" not in rest_client.events


def test_relationship_state_get_failure_stops_all_later_traversal() -> None:
    task = _preflight_item(
        WorkItemType.TASK,
        "Task",
        "first.md",
        (
            HeadingIdentity(1, "Root A"),
            HeadingIdentity(2, "Feature"),
            HeadingIdentity(3, "PBI"),
            HeadingIdentity(4, "Task"),
        ),
        3,
        acceptance_criteria_html=None,
    )
    pbi = _preflight_item(
        WorkItemType.PRODUCT_BACKLOG_ITEM,
        "PBI",
        "first.md",
        (
            HeadingIdentity(1, "Root A"),
            HeadingIdentity(2, "Feature"),
            HeadingIdentity(3, "PBI"),
        ),
        2,
        children=(task,),
    )
    feature = _preflight_item(
        WorkItemType.FEATURE,
        "Feature",
        "first.md",
        (HeadingIdentity(1, "Root A"), HeadingIdentity(2, "Feature")),
        1,
        children=(pbi,),
    )
    root_a = _preflight_item(
        WorkItemType.EPIC,
        "Root A",
        "first.md",
        (HeadingIdentity(1, "Root A"),),
        0,
        children=(feature,),
    )
    root_b = _preflight_item(
        WorkItemType.EPIC, "Root B", "first.md", (HeadingIdentity(1, "Root B"),), 2
    )
    root_c = _preflight_item(
        WorkItemType.EPIC, "Root C", "second.md", (HeadingIdentity(1, "Root C"),), 0
    )
    state = _traversal_state(
        _preflight_hierarchy(_document("first.md", root_a, root_b), _document("second.md", root_c))
    )
    rest_client = _TraversalRestClient(
        existing_titles={"Root A", "Feature"},
        relationship_state_error_title="Feature",
    )

    with pytest.raises(AzureDevOpsTransportError, match="Relationship-state GET failed") as raised:
        coordinate_deterministic_hierarchy_traversal(
            state, rest_client, personal_access_token="secret-pat"  # type: ignore[arg-type]
        )

    assert str(raised.value) == "Relationship-state GET failed"
    assert rest_client.events.count("relationship-get:Feature") == 1
    assert "patch:Feature" not in rest_client.events
    assert "resolve:PBI" not in rest_client.events
    assert "resolve:Task" not in rest_client.events
    assert "resolve:Root B" not in rest_client.events
    assert "resolve:Root C" not in rest_client.events


def test_multiple_roots_and_documents_complete_in_source_order() -> None:
    child_a = _preflight_item(
        WorkItemType.FEATURE,
        "Child A",
        "first.md",
        (HeadingIdentity(1, "Root A"), HeadingIdentity(2, "Child A")),
        1,
    )
    root_a = _preflight_item(
        WorkItemType.EPIC,
        "Root A",
        "first.md",
        (HeadingIdentity(1, "Root A"),),
        0,
        children=(child_a,),
    )
    root_b = _preflight_item(
        WorkItemType.EPIC, "Root B", "first.md", (HeadingIdentity(1, "Root B"),), 2
    )
    root_c = _preflight_item(
        WorkItemType.EPIC, "Root C", "second.md", (HeadingIdentity(1, "Root C"),), 0
    )
    state = _traversal_state(
        _preflight_hierarchy(_document("first.md", root_a, root_b), _document("second.md", root_c))
    )
    rest_client = _TraversalRestClient()

    coordinate_deterministic_hierarchy_traversal(
        state, rest_client, personal_access_token="secret-pat"  # type: ignore[arg-type]
    )

    assert rest_client.events == [
        "resolve:Root A",
        "create:Root A",
        "resolve:Child A",
        "create:Child A",
        "patch:Child A",
        "resolve:Root B",
        "create:Root B",
        "resolve:Root C",
        "create:Root C",
    ]


def test_root_resolution_failure_stops_later_roots_and_documents() -> None:
    state = _traversal_state(_complete_preflight_hierarchy())
    rest_client = _TraversalRestClient(resolution_error_title="Epic")

    with pytest.raises(AzureDevOpsTransportError, match="Resolution failed"):
        coordinate_deterministic_hierarchy_traversal(
            state, rest_client, personal_access_token="secret-pat"  # type: ignore[arg-type]
        )

    assert rest_client.events == ["resolve:Epic"]


def test_non_root_resolution_failure_prevents_lifecycle_and_later_work() -> None:
    state = _traversal_state(_complete_preflight_hierarchy())
    rest_client = _TraversalRestClient(resolution_error_title="Feature")

    with pytest.raises(AzureDevOpsTransportError, match="Resolution failed"):
        coordinate_deterministic_hierarchy_traversal(
            state, rest_client, personal_access_token="secret-pat"  # type: ignore[arg-type]
        )

    assert rest_client.events == ["resolve:Epic", "create:Epic", "resolve:Feature"]


def test_relationship_patch_failure_stops_later_work() -> None:
    state = _traversal_state(_complete_preflight_hierarchy())
    rest_client = _TraversalRestClient(patch_error_title="Feature")

    with pytest.raises(AzureDevOpsTransportError, match="Relationship PATCH failed"):
        coordinate_deterministic_hierarchy_traversal(
            state, rest_client, personal_access_token="secret-pat"  # type: ignore[arg-type]
        )

    assert rest_client.events[-1] == "patch:Feature"
    assert "resolve:PBI" not in rest_client.events


def test_later_run_recovers_created_child_without_duplicate_create() -> None:
    feature = _preflight_item(
        WorkItemType.FEATURE,
        "Feature",
        "input.md",
        (HeadingIdentity(1, "Epic"), HeadingIdentity(2, "Feature")),
        1,
    )
    epic = _preflight_item(
        WorkItemType.EPIC, "Epic", "input.md", (HeadingIdentity(1, "Epic"),), 0, children=(feature,)
    )
    state = _traversal_state(_preflight_hierarchy(_document("input.md", epic)))
    rest_client = _TraversalRestClient(patch_error_title="Feature")

    with pytest.raises(AzureDevOpsTransportError, match="Relationship PATCH failed"):
        coordinate_deterministic_hierarchy_traversal(
            state, rest_client, personal_access_token="secret-pat"  # type: ignore[arg-type]
        )

    rest_client.patch_error_title = None
    rest_client.existing_titles.update({"Epic", "Feature"})
    coordinate_deterministic_hierarchy_traversal(
        state, rest_client, personal_access_token="secret-pat"  # type: ignore[arg-type]
    )

    assert [candidate.title for candidate in rest_client.create_candidates] == ["Epic", "Feature"]
