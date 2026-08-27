"""Pure Version 1.0 work-item candidate construction."""

from __future__ import annotations

from dataclasses import dataclass

from azure_devops_backlog_generator.documentation.models import (
    SemanticWorkItem,
    WorkItemType,
)
from azure_devops_backlog_generator.generator.identity import build_source_identity_marker


@dataclass(frozen=True, slots=True)
class WorkItemCandidate:
    """Prepared logical values for one later Azure DevOps Work Item Create."""

    work_item_type: WorkItemType
    title: str
    description_html: str
    acceptance_criteria_html: str | None
    tags_value: str | None
    source_identity: str


def build_work_item_candidate(item: SemanticWorkItem) -> WorkItemCandidate:
    """Build one immutable candidate from a prepared semantic work item."""
    return WorkItemCandidate(
        work_item_type=item.work_item_type,
        title=item.title,
        description_html=item.description_html,
        acceptance_criteria_html=item.acceptance_criteria_html,
        tags_value=item.tags_value,
        source_identity=build_source_identity_marker(
            item.canonical_relative_path, item.heading_hierarchy
        ),
    )
