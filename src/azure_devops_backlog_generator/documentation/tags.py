"""Tags selection, validation and preparation for source work items."""

from __future__ import annotations

import unicodedata
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

_TAGS_MARKER = "Tags:"
_ACCEPTANCE_CRITERIA_MARKER = "Acceptance Criteria:"
_PROHIBITED_UNICODE_CATEGORIES = frozenset({"Cc", "Cf", "Cs"})


def prepare_tags(
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
    """Return the deterministic prepared Tags value for one semantic item's body."""
    direct_body = list(tokens[start:end])
    markers = _find_reserved_markers(direct_body)
    _validate_marker_order(markers, work_item_type, relative_path)
    tag_indexes = [index for index, marker in markers if marker == _TAGS_MARKER]
    if not tag_indexes:
        return None

    tags_start = tag_indexes[0] + 3
    acceptance_criteria_indexes = [
        index for index, marker in markers if marker == _ACCEPTANCE_CRITERIA_MARKER
    ]
    tags_end = acceptance_criteria_indexes[0] if acceptance_criteria_indexes else len(direct_body)
    tag_tokens = direct_body[tags_start:tags_end]
    item_ranges = _validate_list_grammar(tag_tokens, relative_path)
    _validate_description_tokens(
        tag_tokens,
        parser,
        source,
        references or {},
        relative_path,
    )

    tags = [
        _normalise_and_validate_tag(tag_tokens[item_start:item_end], relative_path)
        for item_start, item_end in item_ranges
    ]
    _validate_duplicates(tags, relative_path)
    return "; ".join(tags)


def _validate_list_grammar(tokens: Sequence[Token], relative_path: str) -> list[tuple[int, int]]:
    if not tokens or tokens[0].type != "bullet_list_open" or tokens[0].level != 0:
        raise DocumentationValidationError(
            f"Tags must contain exactly one top-level unordered list: {relative_path}."
        )
    if tokens[-1].type != "bullet_list_close":
        raise DocumentationValidationError(
            f"Tags must contain exactly one top-level unordered list: {relative_path}."
        )
    top_level_list_count = sum(
        token.type in {"bullet_list_open", "ordered_list_open"} and token.level == 0
        for token in tokens
    )
    if top_level_list_count != 1:
        raise DocumentationValidationError(
            f"Tags must contain exactly one top-level unordered list: {relative_path}."
        )
    if any(
        token.type in {"bullet_list_open", "ordered_list_open"} and token.level != 0
        for token in tokens
    ):
        raise DocumentationValidationError(f"Nested Tags lists are not permitted: {relative_path}.")

    item_ranges = _top_level_item_ranges(tokens)
    if not item_ranges:
        raise DocumentationValidationError(f"Tags list is empty: {relative_path}.")
    return item_ranges


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


def _normalise_and_validate_tag(tokens: Sequence[Token], relative_path: str) -> str:
    value = " ".join(
        _visible_inline_text(token.children or []) for token in tokens if token.type == "inline"
    )
    normalised = " ".join(value.split())
    if not normalised:
        raise DocumentationValidationError(f"Tag is empty: {relative_path}.")
    if len(normalised) > 400:
        raise DocumentationValidationError(f"Tag exceeds 400 characters: {relative_path}.")
    if "," in normalised or ";" in normalised:
        raise DocumentationValidationError(f"Tag contains a reserved delimiter: {relative_path}.")
    if any(
        unicodedata.category(character) in _PROHIBITED_UNICODE_CATEGORIES
        for character in normalised
    ):
        raise DocumentationValidationError(
            f"Tag contains a prohibited Unicode character: {relative_path}."
        )
    return normalised


def _visible_inline_text(tokens: Sequence[Token]) -> str:
    parts: list[str] = []
    for token in tokens:
        if token.type in {"text", "code_inline"}:
            parts.append(token.content)
        elif token.type in {"softbreak", "hardbreak"}:
            parts.append("\n")
    return "".join(parts)


def _validate_duplicates(tags: Sequence[str], relative_path: str) -> None:
    seen: set[str] = set()
    for tag in tags:
        key = tag.casefold()
        if key in seen:
            raise DocumentationValidationError(f"Duplicate Tags value: {relative_path}.")
        seen.add(key)
