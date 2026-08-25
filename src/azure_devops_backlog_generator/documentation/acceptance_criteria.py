"""Acceptance Criteria selection, validation and rendering for source work items."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from markdown_it import MarkdownIt
from markdown_it.token import Token

from azure_devops_backlog_generator.documentation.description import (
    _find_reserved_markers,
    _validate_description_tokens,
    _validate_marker_order,
)
from azure_devops_backlog_generator.documentation.exceptions import DocumentationValidationError
from azure_devops_backlog_generator.documentation.models import WorkItemType

_ACCEPTANCE_CRITERIA_MARKER = "Acceptance Criteria:"


def prepare_acceptance_criteria(
    *,
    parser: MarkdownIt,
    tokens: Sequence[Token],
    start: int,
    end: int,
    work_item_type: WorkItemType,
    relative_path: str,
    source: str,
    references: Mapping[str, Mapping[str, object]] | None = None,
) -> str | None:
    """Return the normative HTML Acceptance Criteria for one semantic item's body."""
    direct_body = list(tokens[start:end])
    markers = _find_reserved_markers(direct_body)
    _validate_marker_order(markers, work_item_type, relative_path)
    marker_indexes = [
        index for index, marker in markers if marker == _ACCEPTANCE_CRITERIA_MARKER
    ]
    if not marker_indexes:
        return None

    acceptance_criteria_tokens = direct_body[marker_indexes[0] + 3 :]
    _validate_list_grammar(acceptance_criteria_tokens, relative_path)
    _validate_description_tokens(
        acceptance_criteria_tokens,
        parser,
        source,
        references or {},
        relative_path,
    )
    try:
        rendered = parser.renderer.render(acceptance_criteria_tokens, parser.options, {})
    except Exception as error:
        raise DocumentationValidationError(
            f"Acceptance Criteria rendering failed: {relative_path}."
        ) from error
    if not rendered:
        raise DocumentationValidationError(
            f"Empty rendered Acceptance Criteria: {relative_path}."
        )
    return rendered


def _validate_list_grammar(tokens: Sequence[Token], relative_path: str) -> None:
    if (
        not tokens
        or tokens[0].type not in {"bullet_list_open", "ordered_list_open"}
        or tokens[0].level != 0
    ):
        raise DocumentationValidationError(
            f"Acceptance Criteria must contain exactly one top-level list: {relative_path}."
        )
    if tokens[-1].type not in {"bullet_list_close", "ordered_list_close"}:
        raise DocumentationValidationError(
            f"Acceptance Criteria must contain exactly one top-level list: {relative_path}."
        )
    top_level_list_count = sum(
        token.type in {"bullet_list_open", "ordered_list_open"} and token.level == 0
        for token in tokens
    )
    if top_level_list_count != 1:
        raise DocumentationValidationError(
            f"Acceptance Criteria must contain exactly one top-level list: {relative_path}."
        )
    if any(
        token.type in {"bullet_list_open", "ordered_list_open"} and token.level != 0
        for token in tokens
    ):
        raise DocumentationValidationError(
            f"Nested Acceptance Criteria lists are not permitted: {relative_path}."
        )

    item_ranges = _top_level_item_ranges(tokens)
    if not item_ranges:
        raise DocumentationValidationError(f"Acceptance Criteria list is empty: {relative_path}.")
    for item_start, item_end in item_ranges:
        if not _has_non_whitespace_content(tokens[item_start:item_end]):
            raise DocumentationValidationError(
                f"Acceptance Criterion is empty: {relative_path}."
            )


def _top_level_item_ranges(tokens: Sequence[Token]) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    item_start: int | None = None
    for index, token in enumerate(tokens):
        if token.type == "list_item_open" and token.level == 1:
            item_start = index + 1
        elif token.type == "list_item_close" and token.level == 1 and item_start is not None:
            ranges.append((item_start, index))
            item_start = None
    return ranges


def _has_non_whitespace_content(tokens: Sequence[Token]) -> bool:
    return any(
        token.type in {"inline", "fence", "code_block"} and bool(token.content.strip())
        for token in tokens
    )
