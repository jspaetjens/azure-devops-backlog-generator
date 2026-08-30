"""Generator preflight and root Work Item lifecycle coordination."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass

from azure_devops_backlog_generator.azure_devops.compatibility import (
    _REQUIRED_FIELDS,
    StructuralCompatibilityEvidence,
    evaluate_structural_scrum_compatibility,
)
from azure_devops_backlog_generator.azure_devops.models import AzureDevOpsProject
from azure_devops_backlog_generator.azure_devops.rest_client import AzureDevOpsRestClient
from azure_devops_backlog_generator.documentation.models import (
    DocumentationHierarchy,
    SemanticWorkItem,
    WorkItemType,
)
from azure_devops_backlog_generator.generator.candidates import (
    WorkItemCandidate,
    build_work_item_candidate,
)
from azure_devops_backlog_generator.generator.identity import (
    _iter_source_order_items,
    build_source_identity_marker,
    validate_source_identity_collisions,
)
from azure_devops_backlog_generator.generator.relationships import (
    coordinate_non_root_relationship_lifecycle,
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


def coordinate_generator_orchestration(
    hierarchy: DocumentationHierarchy,
    rest_client: AzureDevOpsRestClient,
    *,
    personal_access_token: str,
) -> None:
    """Run complete Generator preflight before deterministic persistence traversal."""
    preflight_state = coordinate_full_preflight(
        hierarchy,
        rest_client,
        personal_access_token=personal_access_token,
    )
    coordinate_deterministic_hierarchy_traversal(
        preflight_state,
        rest_client,
        personal_access_token=personal_access_token,
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


def coordinate_deterministic_hierarchy_traversal(
    preflight_state: PreflightState,
    rest_client: AzureDevOpsRestClient,
    *,
    personal_access_token: str,
) -> None:
    """Persist the validated hierarchy in deterministic parent-before-child order."""
    _validate_preflight_state_association(preflight_state)
    candidates = iter(preflight_state.candidates)

    for document in preflight_state.hierarchy.documents:
        for root in sorted(document.root_items, key=lambda item: item.source_order):
            _coordinate_semantic_subtree(
                root,
                candidates,
                preflight_state.project,
                rest_client,
                personal_access_token=personal_access_token,
                parent_work_item_id=None,
            )


def _validate_preflight_state_association(preflight_state: PreflightState) -> None:
    """Reject malformed preflight state before any persistent operation begins."""
    items = tuple(_iter_source_order_items(preflight_state.hierarchy))
    if len(items) != len(preflight_state.candidates):
        raise ValueError("Preflight state candidates do not match the semantic item count.")

    for item, candidate in zip(items, preflight_state.candidates, strict=True):
        expected_source_identity = build_source_identity_marker(
            item.canonical_relative_path, item.heading_hierarchy
        )
        if candidate.source_identity != expected_source_identity:
            raise ValueError(
                "Preflight state candidate does not match its semantic source identity."
            )


def _coordinate_semantic_subtree(
    item: SemanticWorkItem,
    candidates: Iterator[WorkItemCandidate],
    project: AzureDevOpsProject,
    rest_client: AzureDevOpsRestClient,
    *,
    personal_access_token: str,
    parent_work_item_id: int | None,
) -> None:
    """Persist one semantic item, then its descendants after eligibility."""
    candidate = next(candidates)
    if parent_work_item_id is None:
        work_item_id = coordinate_root_work_item_lifecycle(
            candidate,
            project,
            rest_client,
            personal_access_token=personal_access_token,
        )
    else:
        resolution = resolve_work_item_candidate(
            candidate,
            project,
            rest_client,
            personal_access_token=personal_access_token,
        )
        work_item_id = coordinate_non_root_relationship_lifecycle(
            parent_work_item_id,
            candidate,
            resolution,
            rest_client,
            personal_access_token=personal_access_token,
        )

    for child in sorted(item.children, key=lambda child: child.source_order):
        _coordinate_semantic_subtree(
            child,
            candidates,
            project,
            rest_client,
            personal_access_token=personal_access_token,
            parent_work_item_id=work_item_id,
        )
