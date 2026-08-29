"""Tests for root Work Item lifecycle coordination."""

import pytest

from azure_devops_backlog_generator.azure_devops.exceptions import (
    AzureDevOpsHttpError,
    AzureDevOpsTransportError,
)
from azure_devops_backlog_generator.azure_devops.models import (
    AzureDevOpsProject,
    AzureDevOpsWorkItem,
)
from azure_devops_backlog_generator.documentation.models import WorkItemType
from azure_devops_backlog_generator.generator.candidates import WorkItemCandidate
from azure_devops_backlog_generator.generator.orchestration import (
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
