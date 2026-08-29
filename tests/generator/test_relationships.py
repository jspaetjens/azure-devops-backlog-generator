"""Tests for reused-child Parent-Child Relationship state classification."""

from __future__ import annotations

from typing import NoReturn

import pytest

from azure_devops_backlog_generator.azure_devops.exceptions import (
    AzureDevOpsResponseError,
    AzureDevOpsTransportError,
)
from azure_devops_backlog_generator.azure_devops.models import (
    AzureDevOpsWorkItem,
    AzureDevOpsWorkItemRelationshipState,
)
from azure_devops_backlog_generator.documentation.models import WorkItemType
from azure_devops_backlog_generator.generator.candidates import WorkItemCandidate
from azure_devops_backlog_generator.generator.relationships import (
    ConflictingReusedChildRelationshipError,
    ReusedChildRelationshipClassification,
    classify_reused_child_relationship_state,
    coordinate_non_root_relationship_lifecycle,
    gate_reused_child_descendant_processing,
    recover_missing_parent_relationship,
)
from azure_devops_backlog_generator.generator.resolution import WorkItemResolution


class _RestClient:
    def __init__(self, error: Exception | None = None) -> None:
        self.error = error
        self.patch_calls: list[tuple[int, int, int, str]] = []

    def patch_parent_child_relationship(
        self,
        parent_work_item_id: int,
        child_work_item_id: int,
        child_revision: int,
        *,
        personal_access_token: str,
    ) -> None:
        self.patch_calls.append(
            (
                parent_work_item_id,
                child_work_item_id,
                child_revision,
                personal_access_token,
            )
        )
        if self.error is not None:
            raise self.error


class _LifecycleRestClient:
    def __init__(
        self,
        *,
        created_work_item: AzureDevOpsWorkItem | None = None,
        relationship_state: AzureDevOpsWorkItemRelationshipState | None = None,
        create_error: Exception | None = None,
        patch_error: Exception | None = None,
        relationship_state_error: Exception | None = None,
    ) -> None:
        self.created_work_item = created_work_item
        self.relationship_state = relationship_state
        self.create_error = create_error
        self.patch_error = patch_error
        self.relationship_state_error = relationship_state_error
        self.create_calls: list[tuple[WorkItemCandidate, str]] = []
        self.patch_calls: list[tuple[int, int, int, str]] = []
        self.relationship_state_calls: list[tuple[int, str]] = []

    def create_work_item(
        self, candidate: WorkItemCandidate, *, personal_access_token: str
    ) -> AzureDevOpsWorkItem:
        self.create_calls.append((candidate, personal_access_token))
        if self.create_error is not None:
            raise self.create_error
        assert self.created_work_item is not None
        return self.created_work_item

    def patch_parent_child_relationship(
        self,
        parent_work_item_id: int,
        child_work_item_id: int,
        child_revision: int,
        *,
        personal_access_token: str,
    ) -> None:
        self.patch_calls.append(
            (
                parent_work_item_id,
                child_work_item_id,
                child_revision,
                personal_access_token,
            )
        )
        if self.patch_error is not None:
            raise self.patch_error

    def retrieve_work_item_relationship_state(
        self, child_work_item_id: int, *, personal_access_token: str
    ) -> AzureDevOpsWorkItemRelationshipState:
        self.relationship_state_calls.append((child_work_item_id, personal_access_token))
        if self.relationship_state_error is not None:
            raise self.relationship_state_error
        assert self.relationship_state is not None
        return self.relationship_state


def _lifecycle_candidate() -> WorkItemCandidate:
    return WorkItemCandidate(
        work_item_type=WorkItemType.FEATURE,
        title="Prepared title",
        description_html="<p>Prepared description</p>\n",
        acceptance_criteria_html=None,
        tags_value=None,
        source_identity="adbg:source-id:v1:sha256:" + "a" * 64,
    )


def _created_work_item() -> AzureDevOpsWorkItem:
    return AzureDevOpsWorkItem(
        id=17,
        revision=3,
        project_name="Canonical Project",
        work_item_type="Feature",
        source_identity="adbg:source-id:v1:sha256:" + "a" * 64,
    )


@pytest.mark.parametrize(
    ("reverse_parent_ids", "expected"),
    [
        ((), ReusedChildRelationshipClassification.MISSING),
        ((42,), ReusedChildRelationshipClassification.CORRECT),
        ((41,), ReusedChildRelationshipClassification.CONFLICTING),
        ((41, 42), ReusedChildRelationshipClassification.CONFLICTING),
        ((42, 42), ReusedChildRelationshipClassification.CONFLICTING),
        ((41, 41), ReusedChildRelationshipClassification.CONFLICTING),
        ((42, 41), ReusedChildRelationshipClassification.CONFLICTING),
        ((40, 42, 43), ReusedChildRelationshipClassification.CONFLICTING),
    ],
)
def test_classifies_reused_child_relationship_state(
    reverse_parent_ids: tuple[int, ...],
    expected: ReusedChildRelationshipClassification,
) -> None:
    relationship_state = AzureDevOpsWorkItemRelationshipState(
        revision=3,
        reverse_parent_ids=reverse_parent_ids,
    )

    assert classify_reused_child_relationship_state(relationship_state, 42) is expected


@pytest.mark.parametrize("reverse_parent_ids", [(41, 42), (42, 41)])
def test_classifies_multi_parent_evidence_as_conflicting_regardless_of_order(
    reverse_parent_ids: tuple[int, ...],
) -> None:
    relationship_state = AzureDevOpsWorkItemRelationshipState(
        revision=3,
        reverse_parent_ids=reverse_parent_ids,
    )

    assert (
        classify_reused_child_relationship_state(relationship_state, 42)
        is ReusedChildRelationshipClassification.CONFLICTING
    )


@pytest.mark.parametrize(
    ("reverse_parent_ids", "expected"),
    [
        ((42,), ReusedChildRelationshipClassification.CORRECT),
        ((), ReusedChildRelationshipClassification.MISSING),
    ],
)
def test_classification_does_not_depend_on_fresh_revision(
    reverse_parent_ids: tuple[int, ...],
    expected: ReusedChildRelationshipClassification,
) -> None:
    first_state = AzureDevOpsWorkItemRelationshipState(
        revision=3,
        reverse_parent_ids=reverse_parent_ids,
    )
    second_state = AzureDevOpsWorkItemRelationshipState(
        revision=-1,
        reverse_parent_ids=reverse_parent_ids,
    )

    assert classify_reused_child_relationship_state(first_state, 42) is expected
    assert classify_reused_child_relationship_state(second_state, 42) is expected


def test_does_not_mutate_relationship_state_evidence() -> None:
    relationship_state = AzureDevOpsWorkItemRelationshipState(
        revision=3,
        reverse_parent_ids=(42, 41),
    )
    original_state = relationship_state
    original_revision = relationship_state.revision
    original_reverse_parent_ids = relationship_state.reverse_parent_ids

    assert (
        classify_reused_child_relationship_state(relationship_state, 42)
        is ReusedChildRelationshipClassification.CONFLICTING
    )
    assert relationship_state == original_state
    assert relationship_state.revision == original_revision
    assert relationship_state.reverse_parent_ids == original_reverse_parent_ids


@pytest.mark.parametrize("intended_parent_work_item_id", [True, False, "42", 42.0, None, object()])
def test_rejects_non_integer_intended_parent_work_item_id(
    intended_parent_work_item_id: object,
) -> None:
    relationship_state = AzureDevOpsWorkItemRelationshipState(revision=3, reverse_parent_ids=())

    with pytest.raises(ValueError, match=r"^A numeric parent Work Item ID is required\.$"):
        classify_reused_child_relationship_state(
            relationship_state,
            intended_parent_work_item_id,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    ("intended_parent_work_item_id", "reverse_parent_ids"),
    [(42, (42,)), (0, (0,)), (-1, (-1,))],
)
def test_accepts_exact_integer_intended_parent_work_item_ids(
    intended_parent_work_item_id: int,
    reverse_parent_ids: tuple[int, ...],
) -> None:
    relationship_state = AzureDevOpsWorkItemRelationshipState(
        revision=3,
        reverse_parent_ids=reverse_parent_ids,
    )

    assert (
        classify_reused_child_relationship_state(relationship_state, intended_parent_work_item_id)
        is ReusedChildRelationshipClassification.CORRECT
    )


def test_defines_exactly_the_approved_classification_members() -> None:
    assert tuple(ReusedChildRelationshipClassification) == (
        ReusedChildRelationshipClassification.MISSING,
        ReusedChildRelationshipClassification.CORRECT,
        ReusedChildRelationshipClassification.CONFLICTING,
    )


def test_recovers_missing_parent_relationship_with_fresh_evidence(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_classification(*args: object) -> NoReturn:
        raise AssertionError("Recovery must not classify relationship evidence.")

    monkeypatch.setattr(
        "azure_devops_backlog_generator.generator.relationships."
        "classify_reused_child_relationship_state",
        fail_classification,
    )
    relationship_state = AzureDevOpsWorkItemRelationshipState(
        revision=7,
        reverse_parent_ids=(),
    )
    original_state = relationship_state
    rest_client = _RestClient()

    assert (
        recover_missing_parent_relationship(
            11,
            17,
            relationship_state,
            rest_client,  # type: ignore[arg-type]
            personal_access_token="secret-pat",
        )
        is None
    )

    assert rest_client.patch_calls == [(11, 17, 7, "secret-pat")]
    assert relationship_state is original_state
    assert relationship_state == AzureDevOpsWorkItemRelationshipState(
        revision=7,
        reverse_parent_ids=(),
    )


def test_propagates_missing_parent_recovery_transport_failure_without_retry() -> None:
    error = AzureDevOpsTransportError("transport failed")
    rest_client = _RestClient(error)

    with pytest.raises(AzureDevOpsTransportError) as raised:
        recover_missing_parent_relationship(
            11,
            17,
            AzureDevOpsWorkItemRelationshipState(revision=7, reverse_parent_ids=()),
            rest_client,  # type: ignore[arg-type]
            personal_access_token="secret-pat",
        )

    assert raised.value is error
    assert rest_client.patch_calls == [(11, 17, 7, "secret-pat")]


def test_propagates_missing_parent_recovery_response_failure_without_retry() -> None:
    error = AzureDevOpsResponseError("invalid response")
    rest_client = _RestClient(error)

    with pytest.raises(AzureDevOpsResponseError) as raised:
        recover_missing_parent_relationship(
            11,
            17,
            AzureDevOpsWorkItemRelationshipState(revision=7, reverse_parent_ids=()),
            rest_client,  # type: ignore[arg-type]
            personal_access_token="secret-pat",
        )

    assert raised.value is error
    assert rest_client.patch_calls == [(11, 17, 7, "secret-pat")]


def test_gates_correct_reused_child_for_descendant_processing_without_rest_operation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_recovery(*args: object, **kwargs: object) -> NoReturn:
        raise AssertionError("CORRECT reused-child evidence must not recover a relationship.")

    def fail_classification(*args: object, **kwargs: object) -> NoReturn:
        raise AssertionError("The gate must consume the supplied classification.")

    monkeypatch.setattr(
        "azure_devops_backlog_generator.generator.relationships."
        "recover_missing_parent_relationship",
        fail_recovery,
    )
    monkeypatch.setattr(
        "azure_devops_backlog_generator.generator.relationships."
        "classify_reused_child_relationship_state",
        fail_classification,
    )
    relationship_state = AzureDevOpsWorkItemRelationshipState(
        revision=7,
        reverse_parent_ids=(11,),
    )
    rest_client = _RestClient()

    assert (
        gate_reused_child_descendant_processing(
            11,
            17,
            relationship_state,
            ReusedChildRelationshipClassification.CORRECT,
            rest_client,  # type: ignore[arg-type]
            personal_access_token="secret-pat",
        )
        is None
    )

    assert rest_client.patch_calls == []
    assert relationship_state == AzureDevOpsWorkItemRelationshipState(
        revision=7,
        reverse_parent_ids=(11,),
    )


def test_gates_missing_reused_child_by_delegating_recovery_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    recovery_calls: list[tuple[int, int, AzureDevOpsWorkItemRelationshipState, object, str]] = []

    def recover(
        intended_parent_work_item_id: int,
        child_work_item_id: int,
        relationship_state: AzureDevOpsWorkItemRelationshipState,
        rest_client: object,
        *,
        personal_access_token: str,
    ) -> None:
        recovery_calls.append(
            (
                intended_parent_work_item_id,
                child_work_item_id,
                relationship_state,
                rest_client,
                personal_access_token,
            )
        )

    monkeypatch.setattr(
        "azure_devops_backlog_generator.generator.relationships."
        "recover_missing_parent_relationship",
        recover,
    )
    relationship_state = AzureDevOpsWorkItemRelationshipState(revision=7, reverse_parent_ids=())
    rest_client = _RestClient()

    assert (
        gate_reused_child_descendant_processing(
            11,
            17,
            relationship_state,
            ReusedChildRelationshipClassification.MISSING,
            rest_client,  # type: ignore[arg-type]
            personal_access_token="secret-pat",
        )
        is None
    )

    assert recovery_calls == [(11, 17, relationship_state, rest_client, "secret-pat")]
    assert recovery_calls[0][2] is relationship_state
    assert recovery_calls[0][3] is rest_client
    assert rest_client.patch_calls == []
    assert relationship_state == AzureDevOpsWorkItemRelationshipState(
        revision=7,
        reverse_parent_ids=(),
    )


def test_propagates_missing_reused_child_recovery_failure_without_retry(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    error = AzureDevOpsTransportError("transport failed")
    recovery_calls = 0

    def fail_recovery(*args: object, **kwargs: object) -> NoReturn:
        nonlocal recovery_calls
        recovery_calls += 1
        raise error

    monkeypatch.setattr(
        "azure_devops_backlog_generator.generator.relationships."
        "recover_missing_parent_relationship",
        fail_recovery,
    )
    rest_client = _RestClient()

    with pytest.raises(AzureDevOpsTransportError) as raised:
        gate_reused_child_descendant_processing(
            11,
            17,
            AzureDevOpsWorkItemRelationshipState(revision=7, reverse_parent_ids=()),
            ReusedChildRelationshipClassification.MISSING,
            rest_client,  # type: ignore[arg-type]
            personal_access_token="secret-pat",
        )

    assert raised.value is error
    assert recovery_calls == 1
    assert rest_client.patch_calls == []


def test_blocks_conflicting_reused_child_descendant_processing_without_rest_operation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_recovery(*args: object, **kwargs: object) -> NoReturn:
        raise AssertionError("CONFLICTING reused-child evidence must not recover a relationship.")

    def fail_classification(*args: object, **kwargs: object) -> NoReturn:
        raise AssertionError("The gate must consume the supplied classification.")

    monkeypatch.setattr(
        "azure_devops_backlog_generator.generator.relationships."
        "recover_missing_parent_relationship",
        fail_recovery,
    )
    monkeypatch.setattr(
        "azure_devops_backlog_generator.generator.relationships."
        "classify_reused_child_relationship_state",
        fail_classification,
    )
    relationship_state = AzureDevOpsWorkItemRelationshipState(
        revision=7,
        reverse_parent_ids=(11, 13),
    )
    rest_client = _RestClient()

    with pytest.raises(ConflictingReusedChildRelationshipError) as raised:
        gate_reused_child_descendant_processing(
            11,
            17,
            relationship_state,
            ReusedChildRelationshipClassification.CONFLICTING,
            rest_client,  # type: ignore[arg-type]
            personal_access_token="secret-pat",
        )

    error = raised.value
    assert error.child_work_item_id == 17
    assert error.intended_parent_work_item_id == 11
    assert error.classification is ReusedChildRelationshipClassification.CONFLICTING
    assert error.relationship_state is relationship_state
    assert len(error.relationship_state.reverse_parent_ids) == 2
    assert str(error) == (
        "Reused-child relationship conflict: child Work Item ID 17; "
        "intended parent Work Item ID 11; classification CONFLICTING; "
        "reverse-parent count 2."
    )
    assert rest_client.patch_calls == []
    assert relationship_state == AzureDevOpsWorkItemRelationshipState(
        revision=7,
        reverse_parent_ids=(11, 13),
    )


def test_coordinates_new_child_relationship_lifecycle(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_retrieve(*args: object, **kwargs: object) -> NoReturn:
        raise AssertionError("New children must not retrieve relationship state.")

    def fail_classification(*args: object, **kwargs: object) -> NoReturn:
        raise AssertionError("New children must not be classified as reused.")

    def fail_gate(*args: object, **kwargs: object) -> NoReturn:
        raise AssertionError("New children must not use the reused-child gate.")

    monkeypatch.setattr(
        _LifecycleRestClient, "retrieve_work_item_relationship_state", fail_retrieve
    )
    monkeypatch.setattr(
        "azure_devops_backlog_generator.generator.relationships."
        "classify_reused_child_relationship_state",
        fail_classification,
    )
    monkeypatch.setattr(
        "azure_devops_backlog_generator.generator.relationships."
        "gate_reused_child_descendant_processing",
        fail_gate,
    )
    candidate = _lifecycle_candidate()
    rest_client = _LifecycleRestClient(created_work_item=_created_work_item())

    assert (
        coordinate_non_root_relationship_lifecycle(
            11,
            candidate,
            WorkItemResolution(work_item_id=None, revision=None),
            rest_client,  # type: ignore[arg-type]
            personal_access_token="secret-pat",
        )
        == 17
    )

    assert rest_client.create_calls == [(candidate, "secret-pat")]
    assert rest_client.patch_calls == [(11, 17, 3, "secret-pat")]
    assert rest_client.relationship_state_calls == []


def test_propagates_new_child_relationship_patch_failure_without_retry(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_retrieve(*args: object, **kwargs: object) -> NoReturn:
        raise AssertionError("New children must not retrieve relationship state.")

    def fail_classification(*args: object, **kwargs: object) -> NoReturn:
        raise AssertionError("New children must not be classified as reused.")

    def fail_gate(*args: object, **kwargs: object) -> NoReturn:
        raise AssertionError("New children must not use the reused-child gate.")

    monkeypatch.setattr(
        _LifecycleRestClient, "retrieve_work_item_relationship_state", fail_retrieve
    )
    monkeypatch.setattr(
        "azure_devops_backlog_generator.generator.relationships."
        "classify_reused_child_relationship_state",
        fail_classification,
    )
    monkeypatch.setattr(
        "azure_devops_backlog_generator.generator.relationships."
        "gate_reused_child_descendant_processing",
        fail_gate,
    )
    error = AzureDevOpsTransportError("transport failed")
    rest_client = _LifecycleRestClient(
        created_work_item=_created_work_item(), patch_error=error
    )

    with pytest.raises(AzureDevOpsTransportError) as raised:
        coordinate_non_root_relationship_lifecycle(
            11,
            _lifecycle_candidate(),
            WorkItemResolution(work_item_id=None, revision=None),
            rest_client,  # type: ignore[arg-type]
            personal_access_token="secret-pat",
        )

    assert raised.value is error
    assert len(rest_client.create_calls) == 1
    assert rest_client.patch_calls == [(11, 17, 3, "secret-pat")]
    assert rest_client.relationship_state_calls == []


@pytest.mark.parametrize(
    "classification",
    [
        ReusedChildRelationshipClassification.CORRECT,
        ReusedChildRelationshipClassification.MISSING,
    ],
)
def test_coordinates_reused_child_relationship_lifecycle(
    monkeypatch: pytest.MonkeyPatch,
    classification: ReusedChildRelationshipClassification,
) -> None:
    relationship_state = AzureDevOpsWorkItemRelationshipState(
        revision=7,
        reverse_parent_ids=(11,),
    )
    classification_calls: list[tuple[AzureDevOpsWorkItemRelationshipState, int]] = []
    gate_calls: list[
        tuple[
            int,
            int,
            AzureDevOpsWorkItemRelationshipState,
            ReusedChildRelationshipClassification,
            object,
            str,
        ]
    ] = []

    def classify(
        supplied_state: AzureDevOpsWorkItemRelationshipState,
        intended_parent_work_item_id: int,
    ) -> ReusedChildRelationshipClassification:
        classification_calls.append((supplied_state, intended_parent_work_item_id))
        return classification

    def gate(
        intended_parent_work_item_id: int,
        child_work_item_id: int,
        supplied_state: AzureDevOpsWorkItemRelationshipState,
        supplied_classification: ReusedChildRelationshipClassification,
        rest_client: object,
        *,
        personal_access_token: str,
    ) -> None:
        gate_calls.append(
            (
                intended_parent_work_item_id,
                child_work_item_id,
                supplied_state,
                supplied_classification,
                rest_client,
                personal_access_token,
            )
        )

    monkeypatch.setattr(
        "azure_devops_backlog_generator.generator.relationships."
        "classify_reused_child_relationship_state",
        classify,
    )
    monkeypatch.setattr(
        "azure_devops_backlog_generator.generator.relationships."
        "gate_reused_child_descendant_processing",
        gate,
    )
    rest_client = _LifecycleRestClient(relationship_state=relationship_state)

    assert (
        coordinate_non_root_relationship_lifecycle(
            11,
            _lifecycle_candidate(),
            WorkItemResolution(work_item_id=17, revision=3),
            rest_client,  # type: ignore[arg-type]
            personal_access_token="secret-pat",
        )
        == 17
    )

    assert rest_client.create_calls == []
    assert rest_client.relationship_state_calls == [(17, "secret-pat")]
    assert classification_calls == [(relationship_state, 11)]
    assert gate_calls == [(11, 17, relationship_state, classification, rest_client, "secret-pat")]


def test_propagates_reused_child_gate_conflict_unchanged(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    relationship_state = AzureDevOpsWorkItemRelationshipState(
        revision=7,
        reverse_parent_ids=(13,),
    )
    error = ConflictingReusedChildRelationshipError(
        17,
        11,
        ReusedChildRelationshipClassification.CONFLICTING,
        relationship_state,
    )
    classification_calls = 0
    gate_calls = 0

    def classify(
        supplied_state: AzureDevOpsWorkItemRelationshipState,
        intended_parent_work_item_id: int,
    ) -> ReusedChildRelationshipClassification:
        nonlocal classification_calls
        classification_calls += 1
        assert supplied_state is relationship_state
        assert intended_parent_work_item_id == 11
        return ReusedChildRelationshipClassification.CONFLICTING

    def fail_gate(*args: object, **kwargs: object) -> NoReturn:
        nonlocal gate_calls
        gate_calls += 1
        raise error

    monkeypatch.setattr(
        "azure_devops_backlog_generator.generator.relationships."
        "classify_reused_child_relationship_state",
        classify,
    )
    monkeypatch.setattr(
        "azure_devops_backlog_generator.generator.relationships."
        "gate_reused_child_descendant_processing",
        fail_gate,
    )
    rest_client = _LifecycleRestClient(relationship_state=relationship_state)

    with pytest.raises(ConflictingReusedChildRelationshipError) as raised:
        coordinate_non_root_relationship_lifecycle(
            11,
            _lifecycle_candidate(),
            WorkItemResolution(work_item_id=17, revision=3),
            rest_client,  # type: ignore[arg-type]
            personal_access_token="secret-pat",
        )

    assert raised.value is error
    assert rest_client.create_calls == []
    assert rest_client.relationship_state_calls == [(17, "secret-pat")]
    assert classification_calls == 1
    assert gate_calls == 1


def test_propagates_reused_child_relationship_state_failure_without_classifying(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_classification(*args: object, **kwargs: object) -> NoReturn:
        raise AssertionError("A failed GET must not be classified.")

    def fail_gate(*args: object, **kwargs: object) -> NoReturn:
        raise AssertionError("A failed GET must not reach the reused-child gate.")

    monkeypatch.setattr(
        "azure_devops_backlog_generator.generator.relationships."
        "classify_reused_child_relationship_state",
        fail_classification,
    )
    monkeypatch.setattr(
        "azure_devops_backlog_generator.generator.relationships."
        "gate_reused_child_descendant_processing",
        fail_gate,
    )
    error = AzureDevOpsTransportError("transport failed")
    rest_client = _LifecycleRestClient(relationship_state_error=error)

    with pytest.raises(AzureDevOpsTransportError) as raised:
        coordinate_non_root_relationship_lifecycle(
            11,
            _lifecycle_candidate(),
            WorkItemResolution(work_item_id=17, revision=3),
            rest_client,  # type: ignore[arg-type]
            personal_access_token="secret-pat",
        )

    assert raised.value is error
    assert rest_client.create_calls == []
    assert rest_client.relationship_state_calls == [(17, "secret-pat")]
    assert rest_client.patch_calls == []
