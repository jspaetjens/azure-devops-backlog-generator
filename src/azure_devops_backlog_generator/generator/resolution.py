"""Single-candidate Version 1.0 existing Work Item resolution."""

from __future__ import annotations

from dataclasses import dataclass

from azure_devops_backlog_generator.azure_devops.models import (
    AzureDevOpsProject,
    AzureDevOpsWorkItem,
)
from azure_devops_backlog_generator.azure_devops.rest_client import AzureDevOpsRestClient
from azure_devops_backlog_generator.generator.candidates import WorkItemCandidate


@dataclass(frozen=True, slots=True)
class WorkItemResolution:
    """The new or verified-existing outcome for one candidate."""

    work_item_id: int | None
    revision: int | None

    def __post_init__(self) -> None:
        """Require either new or verified-existing resolution evidence."""
        if self.work_item_id is None and self.revision is None:
            return
        if type(self.work_item_id) is not int or type(self.revision) is not int:
            raise ValueError(
                "Work Item resolution requires both values to be None or exact integers."
            )


class ExistingWorkItemResolutionError(Exception):
    """Raised when existing Work Item evidence conflicts with one candidate."""


def resolve_work_item_candidate(
    candidate: WorkItemCandidate,
    project: AzureDevOpsProject,
    rest_client: AzureDevOpsRestClient,
    *,
    personal_access_token: str,
) -> WorkItemResolution:
    """Resolve one candidate to new or verified-existing Work Item evidence."""
    work_item_ids = rest_client.lookup_work_item_ids(
        candidate, personal_access_token=personal_access_token
    )
    if not work_item_ids:
        return WorkItemResolution(work_item_id=None, revision=None)
    if len(work_item_ids) != 1:
        raise ExistingWorkItemResolutionError(
            "Azure DevOps returned ambiguous existing Work Item evidence."
        )

    selected_work_item_id = work_item_ids[0]
    work_item = rest_client.retrieve_work_item(
        selected_work_item_id, personal_access_token=personal_access_token
    )
    _validate_existing_work_item_evidence(candidate, project, selected_work_item_id, work_item)
    return WorkItemResolution(work_item_id=work_item.id, revision=work_item.revision)


def _validate_existing_work_item_evidence(
    candidate: WorkItemCandidate,
    project: AzureDevOpsProject,
    selected_work_item_id: int,
    work_item: AzureDevOpsWorkItem,
) -> None:
    if work_item.id != selected_work_item_id:
        raise ExistingWorkItemResolutionError(
            "Azure DevOps Work Item GET evidence does not match the selected Work Item ID."
        )
    if work_item.project_name != project.name:
        raise ExistingWorkItemResolutionError(
            "Azure DevOps Work Item GET evidence does not match the canonical project name."
        )
    if work_item.work_item_type != candidate.work_item_type.value:
        raise ExistingWorkItemResolutionError(
            "Azure DevOps Work Item GET evidence does not match the candidate Work Item Type."
        )
    if work_item.source_identity != candidate.source_identity:
        raise ExistingWorkItemResolutionError(
            "Azure DevOps Work Item GET evidence does not match the candidate source identity."
        )
