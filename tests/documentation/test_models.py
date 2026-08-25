"""Tests for immutable Documentation Processor data models."""

from dataclasses import FrozenInstanceError

import pytest

from azure_devops_backlog_generator.documentation.models import (
    HeadingIdentity,
    SemanticWorkItem,
    TokenSpan,
    WorkItemType,
)


def test_foundation_models_are_immutable() -> None:
    heading = HeadingIdentity(level=1, title="Epic")
    span = TokenSpan(start=3, end=6)

    with pytest.raises(FrozenInstanceError):
        heading.title = "Changed"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        span.end = 7  # type: ignore[misc]


def test_semantic_work_item_acceptance_criteria_value_is_immutable() -> None:
    item = SemanticWorkItem(
        work_item_type=WorkItemType.EPIC,
        level=1,
        title="Epic",
        canonical_relative_path="input.md",
        heading_hierarchy=(HeadingIdentity(level=1, title="Epic"),),
        source_order=0,
        description_html="<p>Description</p>\n",
        acceptance_criteria_html="<ul>\n<li>Criterion</li>\n</ul>\n",
        direct_body_token_spans=(),
        children=(),
    )

    with pytest.raises(FrozenInstanceError):
        item.acceptance_criteria_html = None  # type: ignore[misc]


def test_work_item_type_values_match_the_fixed_source_grammar() -> None:
    assert tuple(WorkItemType) == (
        WorkItemType.EPIC,
        WorkItemType.FEATURE,
        WorkItemType.PRODUCT_BACKLOG_ITEM,
        WorkItemType.TASK,
    )
