"""Root Work Item lifecycle coordination."""

from azure_devops_backlog_generator.azure_devops.models import AzureDevOpsProject
from azure_devops_backlog_generator.azure_devops.rest_client import AzureDevOpsRestClient
from azure_devops_backlog_generator.generator.candidates import WorkItemCandidate
from azure_devops_backlog_generator.generator.resolution import resolve_work_item_candidate


def coordinate_root_work_item_lifecycle(
    candidate: WorkItemCandidate,
    project: AzureDevOpsProject,
    rest_client: AzureDevOpsRestClient,
    *,
    personal_access_token: str,
) -> int:
    """Resolve or create one root Work Item and return its eligible ID."""
    resolution = resolve_work_item_candidate(
        candidate,
        project,
        rest_client,
        personal_access_token=personal_access_token,
    )
    if resolution.work_item_id is not None:
        return resolution.work_item_id

    return rest_client.create_work_item(
        candidate, personal_access_token=personal_access_token
    ).id
