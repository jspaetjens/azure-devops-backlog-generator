"""Tests for single-candidate Version 1.0 existing Work Item resolution."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, replace

import pytest

from azure_devops_backlog_generator.azure_devops.exceptions import AzureDevOpsHttpError
from azure_devops_backlog_generator.azure_devops.models import (
    AzureDevOpsProject,
    AzureDevOpsWorkItem,
)
from azure_devops_backlog_generator.documentation.models import WorkItemType
from azure_devops_backlog_generator.generator.candidates import WorkItemCandidate
from azure_devops_backlog_generator.generator.resolution import (
    ExistingWorkItemResolutionError,
    WorkItemResolution,
    resolve_work_item_candidate,
)


class _RestClient:
    def __init__(
        self,
        work_item_ids: tuple[int, ...],
        work_item: AzureDevOpsWorkItem | Exception | None = None,
    ) -> None:
        self.work_item_ids = work_item_ids
        self.work_item = work_item
        self.lookup_calls: list[tuple[WorkItemCandidate, str]] = []
        self.retrieve_calls: list[tuple[int, str]] = []

    def lookup_work_item_ids(
        self, candidate: WorkItemCandidate, *, personal_access_token: str
    ) -> tuple[int, ...]:
        self.lookup_calls.append((candidate, personal_access_token))
        return self.work_item_ids

    def retrieve_work_item(
        self, work_item_id: int, *, personal_access_token: str
    ) -> AzureDevOpsWorkItem:
        self.retrieve_calls.append((work_item_id, personal_access_token))
        if isinstance(self.work_item, Exception):
            raise self.work_item
        assert self.work_item is not None
        return self.work_item


def _candidate(**changes: object) -> WorkItemCandidate:
    candidate = WorkItemCandidate(
        work_item_type=WorkItemType.EPIC,
        title="Prepared title",
        description_html="<p>Prepared description</p>\n",
        acceptance_criteria_html="<ul>\n<li>Criterion</li>\n</ul>\n",
        tags_value="platform; generator",
        source_identity="adbg:source-id:v1:sha256:" + "a" * 64,
    )
    return replace(candidate, **changes)


def _project() -> AzureDevOpsProject:
    return AzureDevOpsProject(id="project-id", name="Canonical Project")


def _work_item(**changes: object) -> AzureDevOpsWorkItem:
    work_item = AzureDevOpsWorkItem(
        id=17,
        revision=3,
        project_name="Canonical Project",
        work_item_type="Epic",
        source_identity="adbg:source-id:v1:sha256:" + "a" * 64,
    )
    return replace(work_item, **changes)


@pytest.mark.parametrize(
    ("work_item_id", "revision"),
    [(None, None), (17, 3)],
)
def test_accepts_valid_work_item_resolution_states(
    work_item_id: int | None, revision: int | None
) -> None:
    assert WorkItemResolution(work_item_id=work_item_id, revision=revision) == WorkItemResolution(
        work_item_id=work_item_id, revision=revision
    )


@pytest.mark.parametrize(
    ("work_item_id", "revision"),
    [
        (17, None),
        (None, 3),
        (True, 3),
        (17, True),
        ("17", 3),
        (17, 3.0),
        (object(), 3),
        (17, object()),
    ],
)
def test_rejects_invalid_work_item_resolution_states(
    work_item_id: object, revision: object
) -> None:
    with pytest.raises(ValueError, match="both values"):
        WorkItemResolution(  # type: ignore[arg-type]
            work_item_id=work_item_id,
            revision=revision,
        )


def test_resolves_zero_wiql_ids_as_a_new_work_item() -> None:
    rest_client = _RestClient(())

    resolution = resolve_work_item_candidate(
        _candidate(), _project(), rest_client, personal_access_token="secret-pat"  # type: ignore[arg-type]
    )

    assert resolution == WorkItemResolution(work_item_id=None, revision=None)
    assert rest_client.lookup_calls == [(_candidate(), "secret-pat")]
    assert rest_client.retrieve_calls == []


def test_resolves_one_matching_work_item_as_verified_existing_evidence() -> None:
    candidate = _candidate()
    rest_client = _RestClient((17,), _work_item())

    resolution = resolve_work_item_candidate(
        candidate, _project(), rest_client, personal_access_token="secret-pat"  # type: ignore[arg-type]
    )

    assert resolution == WorkItemResolution(work_item_id=17, revision=3)
    assert rest_client.lookup_calls == [(candidate, "secret-pat")]
    assert rest_client.retrieve_calls == [(17, "secret-pat")]
    with pytest.raises(FrozenInstanceError):
        resolution.work_item_id = 18  # type: ignore[misc]


@pytest.mark.parametrize("work_item_ids", [(17, 18), (17, 18, 19)])
def test_rejects_ambiguous_wiql_evidence_without_retrieving_a_work_item(
    work_item_ids: tuple[int, ...],
) -> None:
    rest_client = _RestClient(work_item_ids)

    with pytest.raises(ExistingWorkItemResolutionError, match="ambiguous"):
        resolve_work_item_candidate(
            _candidate(), _project(), rest_client, personal_access_token="secret-pat"  # type: ignore[arg-type]
        )

    assert len(rest_client.lookup_calls) == 1
    assert rest_client.retrieve_calls == []


@pytest.mark.parametrize(
    ("work_item", "message"),
    [
        (_work_item(id=18), "selected Work Item ID"),
        (_work_item(project_name="Other Project"), "canonical project name"),
        (_work_item(work_item_type="Feature"), "candidate Work Item Type"),
        (_work_item(work_item_type="epic"), "candidate Work Item Type"),
        (
            _work_item(source_identity="adbg:source-id:v1:sha256:" + "b" * 64),
            "candidate source identity",
        ),
        (
            _work_item(source_identity="adbg:source-id:v1:sha256:" + "A" * 64),
            "candidate source identity",
        ),
    ],
)
def test_rejects_conflicting_existing_work_item_evidence(
    work_item: AzureDevOpsWorkItem, message: str
) -> None:
    rest_client = _RestClient((17,), work_item)

    with pytest.raises(ExistingWorkItemResolutionError, match=message):
        resolve_work_item_candidate(
            _candidate(), _project(), rest_client, personal_access_token="secret-pat"  # type: ignore[arg-type]
        )

    assert rest_client.retrieve_calls == [(17, "secret-pat")]


def test_does_not_compare_mutable_candidate_business_values() -> None:
    candidate = _candidate(
        title="Changed title",
        description_html="<p>Changed description</p>\n",
        acceptance_criteria_html=None,
        tags_value=None,
    )
    rest_client = _RestClient((17,), _work_item())

    assert resolve_work_item_candidate(
        candidate, _project(), rest_client, personal_access_token="secret-pat"  # type: ignore[arg-type]
    ) == WorkItemResolution(work_item_id=17, revision=3)


def test_propagates_get_404_without_fallback_or_retry() -> None:
    rest_client = _RestClient((17,), AzureDevOpsHttpError(404))

    with pytest.raises(AzureDevOpsHttpError) as error:
        resolve_work_item_candidate(
            _candidate(), _project(), rest_client, personal_access_token="secret-pat"  # type: ignore[arg-type]
        )

    assert error.value.status == 404
    assert len(rest_client.lookup_calls) == 1
    assert rest_client.retrieve_calls == [(17, "secret-pat")]
