"""Immutable Azure DevOps response models for endpoint-specific operations."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AzureDevOpsProject:
    """Canonical Azure DevOps project evidence returned by Project retrieval."""

    id: str
    name: str


@dataclass(frozen=True, slots=True)
class AzureDevOpsWorkItem:
    """Persisted Work Item evidence returned by the fixed verification GET."""

    id: int
    revision: int
    project_name: str
    work_item_type: str
    source_identity: str


@dataclass(frozen=True, slots=True)
class AzureDevOpsWorkItemRelationshipState:
    """Validated relationship-state evidence for one reused Work Item."""

    revision: int
    reverse_parent_ids: tuple[int, ...]
