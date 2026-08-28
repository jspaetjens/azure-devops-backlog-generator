"""Tests for reused-child Parent-Child Relationship state classification."""

from __future__ import annotations

import pytest

from azure_devops_backlog_generator.azure_devops.models import (
    AzureDevOpsWorkItemRelationshipState,
)
from azure_devops_backlog_generator.generator.relationships import (
    ReusedChildRelationshipClassification,
    classify_reused_child_relationship_state,
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
