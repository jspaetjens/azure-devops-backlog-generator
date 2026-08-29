"""Generator preflight and root Work Item lifecycle coordination."""

from __future__ import annotations

from dataclasses import dataclass

from azure_devops_backlog_generator.azure_devops.compatibility import (
    _REQUIRED_FIELDS,
    StructuralCompatibilityEvidence,
    evaluate_structural_scrum_compatibility,
)
from azure_devops_backlog_generator.azure_devops.models import AzureDevOpsProject
from azure_devops_backlog_generator.azure_devops.rest_client import AzureDevOpsRestClient
from azure_devops_backlog_generator.documentation.models import DocumentationHierarchy, WorkItemType
from azure_devops_backlog_generator.generator.candidates import (
    WorkItemCandidate,
    build_work_item_candidate,
)
from azure_devops_backlog_generator.generator.identity import (
    _iter_source_order_items,
    validate_source_identity_collisions,
)
from azure_devops_backlog_generator.generator.resolution import resolve_work_item_candidate


@dataclass(frozen=True, slots=True)
class PreflightState:
    """Immutable successful-preflight evidence retained for later traversal."""

    hierarchy: DocumentationHierarchy
    project: AzureDevOpsProject
    candidates: tuple[WorkItemCandidate, ...]


def coordinate_full_preflight(
    hierarchy: DocumentationHierarchy,
    rest_client: AzureDevOpsRestClient,
    *,
    personal_access_token: str,
) -> PreflightState:
    """Complete pre-persistence validation and return state for later traversal."""
    validate_source_identity_collisions(hierarchy)
    candidates = tuple(
        build_work_item_candidate(item) for item in _iter_source_order_items(hierarchy)
    )

    project = rest_client.retrieve_project(personal_access_token=personal_access_token)
    evidence = StructuralCompatibilityEvidence(
        work_item_types={
            work_item_type: rest_client.retrieve_work_item_type(
                work_item_type, personal_access_token=personal_access_token
            )
            for work_item_type in WorkItemType
        },
        work_item_type_fields={
            work_item_type: {
                field_reference: rest_client.retrieve_work_item_type_field(
                    work_item_type,
                    field_reference,
                    personal_access_token=personal_access_token,
                )
                for field_reference in _REQUIRED_FIELDS[work_item_type]
            }
            for work_item_type in WorkItemType
        },
        global_fields={
            field_reference: rest_client.retrieve_field(
                field_reference, personal_access_token=personal_access_token
            )
            for field_reference in _required_global_field_references()
        },
    )
    evaluate_structural_scrum_compatibility(evidence)

    for candidate in candidates:
        rest_client.validate_work_item_create(
            candidate, personal_access_token=personal_access_token
        )

    return PreflightState(
        hierarchy=hierarchy,
        project=project,
        candidates=candidates,
    )


def _required_global_field_references() -> tuple[str, ...]:
    """Return the compatibility evaluator's unique field references in fixed order."""
    return tuple(
        dict.fromkeys(
            field_reference
            for work_item_type in WorkItemType
            for field_reference in _REQUIRED_FIELDS[work_item_type]
        )
    )


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
