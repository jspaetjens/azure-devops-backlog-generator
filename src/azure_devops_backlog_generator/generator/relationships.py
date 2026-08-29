"""Reused-child Parent-Child Relationship state coordination."""

from enum import StrEnum

from azure_devops_backlog_generator.azure_devops.models import (
    AzureDevOpsWorkItemRelationshipState,
)
from azure_devops_backlog_generator.azure_devops.rest_client import AzureDevOpsRestClient


class ReusedChildRelationshipClassification(StrEnum):
    """The logical Parent-Child Relationship state of one reused child."""

    MISSING = "MISSING"
    CORRECT = "CORRECT"
    CONFLICTING = "CONFLICTING"


class ConflictingReusedChildRelationshipError(Exception):
    """Raised when reused-child parent evidence blocks descendant processing."""

    def __init__(
        self,
        child_work_item_id: int,
        intended_parent_work_item_id: int,
        classification: ReusedChildRelationshipClassification,
        relationship_state: AzureDevOpsWorkItemRelationshipState,
    ) -> None:
        self.child_work_item_id = child_work_item_id
        self.intended_parent_work_item_id = intended_parent_work_item_id
        self.classification = classification
        self.relationship_state = relationship_state
        super().__init__(
            "Reused-child relationship conflict: "
            f"child Work Item ID {child_work_item_id}; "
            f"intended parent Work Item ID {intended_parent_work_item_id}; "
            f"classification {classification.value}; "
            f"reverse-parent count {len(relationship_state.reverse_parent_ids)}."
        )


def classify_reused_child_relationship_state(
    relationship_state: AzureDevOpsWorkItemRelationshipState,
    intended_parent_work_item_id: int,
) -> ReusedChildRelationshipClassification:
    """Classify validated reused-child relationship evidence against its intended parent."""
    if type(intended_parent_work_item_id) is not int:
        raise ValueError("A numeric parent Work Item ID is required.")

    if not relationship_state.reverse_parent_ids:
        return ReusedChildRelationshipClassification.MISSING
    if (
        len(relationship_state.reverse_parent_ids) == 1
        and relationship_state.reverse_parent_ids[0] == intended_parent_work_item_id
    ):
        return ReusedChildRelationshipClassification.CORRECT
    return ReusedChildRelationshipClassification.CONFLICTING


def recover_missing_parent_relationship(
    intended_parent_work_item_id: int,
    child_work_item_id: int,
    relationship_state: AzureDevOpsWorkItemRelationshipState,
    rest_client: AzureDevOpsRestClient,
    *,
    personal_access_token: str,
) -> None:
    """Add the intended Parent-Child Relationship using fresh reused-child evidence."""
    rest_client.patch_parent_child_relationship(
        intended_parent_work_item_id,
        child_work_item_id,
        relationship_state.revision,
        personal_access_token=personal_access_token,
    )


def gate_reused_child_descendant_processing(
    intended_parent_work_item_id: int,
    child_work_item_id: int,
    relationship_state: AzureDevOpsWorkItemRelationshipState,
    classification: ReusedChildRelationshipClassification,
    rest_client: AzureDevOpsRestClient,
    *,
    personal_access_token: str,
) -> None:
    """Permit descendants only after reused-child parent state is acceptable."""
    if classification is ReusedChildRelationshipClassification.CORRECT:
        return
    if classification is ReusedChildRelationshipClassification.MISSING:
        recover_missing_parent_relationship(
            intended_parent_work_item_id,
            child_work_item_id,
            relationship_state,
            rest_client,
            personal_access_token=personal_access_token,
        )
        return
    if classification is ReusedChildRelationshipClassification.CONFLICTING:
        raise ConflictingReusedChildRelationshipError(
            child_work_item_id,
            intended_parent_work_item_id,
            classification,
            relationship_state,
        )
