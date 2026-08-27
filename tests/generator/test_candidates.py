"""Tests for pure Version 1.0 work-item candidate construction."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, replace

import pytest

import azure_devops_backlog_generator.generator.candidates as candidates_module
from azure_devops_backlog_generator.documentation.models import (
    HeadingIdentity,
    SemanticWorkItem,
    WorkItemType,
)
from azure_devops_backlog_generator.generator.candidates import (
    WorkItemCandidate,
    build_work_item_candidate,
)
from azure_devops_backlog_generator.generator.identity import build_source_identity_marker


def _item(work_item_type: WorkItemType) -> SemanticWorkItem:
    level = tuple(WorkItemType).index(work_item_type) + 1
    title = f"{work_item_type.value} title"
    return SemanticWorkItem(
        work_item_type=work_item_type,
        level=level,
        title=title,
        canonical_relative_path="input.md",
        heading_hierarchy=(HeadingIdentity(level, title),),
        source_order=0,
        description_html="<p>Prepared description</p>\n",
        acceptance_criteria_html=(
            None if work_item_type is WorkItemType.TASK else "<ul>\n<li>Criterion</li>\n</ul>\n"
        ),
        tags_value="platform; generator",
        direct_body_token_spans=(),
        children=(),
    )


@pytest.mark.parametrize("work_item_type", list(WorkItemType))
def test_builds_a_candidate_for_each_supported_work_item_type(
    work_item_type: WorkItemType,
) -> None:
    item = _item(work_item_type)

    candidate = build_work_item_candidate(item)

    assert candidate.work_item_type is work_item_type
    assert candidate.title == item.title
    assert candidate.description_html == item.description_html
    assert candidate.acceptance_criteria_html == item.acceptance_criteria_html
    assert candidate.tags_value == item.tags_value
    assert candidate.source_identity == build_source_identity_marker(
        item.canonical_relative_path, item.heading_hierarchy
    )


def test_preserves_absent_optional_values() -> None:
    item = replace(
        _item(WorkItemType.FEATURE),
        acceptance_criteria_html=None,
        tags_value=None,
    )

    candidate = build_work_item_candidate(item)

    assert candidate.acceptance_criteria_html is None
    assert candidate.tags_value is None


def test_task_candidate_preserves_the_upstream_absent_acceptance_criteria_value() -> None:
    candidate = build_work_item_candidate(_item(WorkItemType.TASK))

    assert candidate.acceptance_criteria_html is None


def test_candidate_values_are_immutable() -> None:
    candidate = build_work_item_candidate(_item(WorkItemType.EPIC))

    with pytest.raises(FrozenInstanceError):
        candidate.title = "Changed"  # type: ignore[misc]


def test_candidate_construction_has_no_rest_client_dependency() -> None:
    assert "AzureDevOpsRestClient" not in candidates_module.__dict__
    assert WorkItemCandidate.__module__ == (
        "azure_devops_backlog_generator.generator.candidates"
    )
