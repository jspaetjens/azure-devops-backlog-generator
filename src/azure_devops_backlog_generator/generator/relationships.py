"""Pure reused-child Parent-Child Relationship state classification."""

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
