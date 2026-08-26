"""Immutable Azure DevOps response models for endpoint-specific operations."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AzureDevOpsProject:
    """Canonical Azure DevOps project evidence returned by Project retrieval."""

    id: str
    name: str
