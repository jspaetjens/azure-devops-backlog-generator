"""Description selection, validation and rendering for source work items."""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping, Sequence
from urllib.parse import urlsplit

from markdown_it import MarkdownIt
from markdown_it.common.utils import normalizeReference, unescapeAll
from markdown_it.token import Token

from azure_devops_backlog_generator.documentation.exceptions import DocumentationValidationError
from azure_devops_backlog_generator.documentation.models import WorkItemType

_TAGS_MARKER = "Tags:"
_ACCEPTANCE_CRITERIA_MARKER = "Acceptance Criteria:"
_PERCENT_ESCAPE = re.compile(r"%(?![0-9A-Fa-f]{2})")
_URI_ALLOWED_CHARACTERS = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    "-._~:/?#[]@!$&'()*+,;=%"
)


def prepare_description(
    *,
    parser: MarkdownIt,
    tokens: Sequence[Token],
    start: int,
    end: int,
    work_item_type: WorkItemType,
    relative_path: str,
    source: str,
    references: Mapping[str, Mapping[str, object]] | None = None,
) -> str:
    """Return the normative HTML Description for one semantic item's direct body."""
    direct_body = list(tokens[start:end])
    markers = _find_reserved_markers(direct_body)
    _validate_marker_order(markers, work_item_type, relative_path)
    description_tokens = direct_body[: markers[0][0]] if markers else direct_body

    if not description_tokens:
        raise DocumentationValidationError(f"Missing Description content: {relative_path}.")
    _validate_description_tokens(
        description_tokens,
        parser,
        source,
        references or {},
        relative_path,
    )

    try:
        rendered = parser.renderer.render(description_tokens, parser.options, {})
    except Exception as error:
        raise DocumentationValidationError(
            f"Description rendering failed: {relative_path}."
        ) from error
    if not rendered:
        raise DocumentationValidationError(f"Empty rendered Description: {relative_path}.")
    return rendered


def _find_reserved_markers(tokens: Sequence[Token]) -> list[tuple[int, str]]:
    markers: list[tuple[int, str]] = []
    for index in range(len(tokens) - 2):
        opening, inline, closing = tokens[index : index + 3]
        if (
            opening.type != "paragraph_open"
            or opening.level != 0
            or inline.type != "inline"
            or closing.type != "paragraph_close"
            or closing.level != 0
        ):
            continue
        if inline.content in {_TAGS_MARKER, _ACCEPTANCE_CRITERIA_MARKER}:
            markers.append((index, inline.content))
    return markers


def _validate_marker_order(
    markers: Sequence[tuple[int, str]],
    work_item_type: WorkItemType,
    relative_path: str,
) -> None:
    tags = [index for index, marker in markers if marker == _TAGS_MARKER]
    acceptance_criteria = [
        index for index, marker in markers if marker == _ACCEPTANCE_CRITERIA_MARKER
    ]
    if len(tags) > 1:
        raise DocumentationValidationError(f"Duplicate Tags marker: {relative_path}.")
    if len(acceptance_criteria) > 1:
        raise DocumentationValidationError(
            f"Duplicate Acceptance Criteria marker: {relative_path}."
        )
    if tags and acceptance_criteria and tags[0] > acceptance_criteria[0]:
        raise DocumentationValidationError(
            f"Tags marker must precede Acceptance Criteria: {relative_path}."
        )
    if acceptance_criteria and work_item_type is WorkItemType.TASK:
        raise DocumentationValidationError(
            f"Acceptance Criteria is not permitted for Task: {relative_path}."
        )


def _validate_description_tokens(
    tokens: Iterable[Token],
    parser: MarkdownIt,
    source: str,
    references: Mapping[str, Mapping[str, object]],
    relative_path: str,
) -> None:
    raw_reference_destinations = _raw_reference_destinations(source, references)
    for token in _walk_tokens(tokens):
        if token.type == "inline":
            _validate_raw_link_destinations(
                token,
                parser,
                references,
                raw_reference_destinations,
                relative_path,
            )
        if token.type in {"html_block", "html_inline"}:
            raise DocumentationValidationError(
                f"Raw HTML in Description is not permitted: {relative_path}."
            )
        if token.type == "image":
            raise DocumentationValidationError(
                f"Markdown images in Description are not permitted: {relative_path}."
            )
        if token.type == "link_open":
            destination = token.attrGet("href")
            if not destination or not _is_permitted_link_destination(destination):
                raise DocumentationValidationError(
                    f"Invalid Description link destination: {relative_path}."
                )


def _validate_raw_link_destinations(
    inline_token: Token,
    parser: MarkdownIt,
    references: Mapping[str, Mapping[str, object]],
    raw_reference_destinations: Mapping[str, str],
    relative_path: str,
) -> None:
    expected_destinations = [
        child.attrGet("href")
        for child in inline_token.children or []
        if child.type == "link_open"
    ]
    if not expected_destinations:
        return

    remaining = list(expected_destinations)
    for kind, value in _source_link_candidates(inline_token.content):
        if kind == "reference":
            _validate_reference_destination(
                value,
                references,
                raw_reference_destinations,
                remaining,
                relative_path,
            )
        else:
            _validate_if_parsed_destination(value, parser, remaining, relative_path)
    if remaining:
        raise DocumentationValidationError(
            f"Cannot determine Description link destination: {relative_path}."
        )


def _validate_if_parsed_destination(
    raw_destination: str,
    parser: MarkdownIt,
    remaining: list[str],
    relative_path: str,
) -> None:
    _validate_raw_link_destination(raw_destination, relative_path)
    destination = parser.normalizeLink(unescapeAll(raw_destination))
    if destination in remaining:
        remaining.remove(destination)


def _validate_reference_destination(
    label: str,
    references: Mapping[str, Mapping[str, object]],
    raw_reference_destinations: Mapping[str, str],
    remaining: list[str],
    relative_path: str,
) -> None:
    key = normalizeReference(label)
    reference = references.get(key)
    if reference is None:
        return
    destination = reference.get("href")
    if not isinstance(destination, str) or destination not in remaining:
        return
    remaining.remove(destination)
    raw_destination = raw_reference_destinations.get(key)
    if raw_destination is None:
        raise DocumentationValidationError(
            f"Cannot determine Description link destination: {relative_path}."
        )
    _validate_raw_link_destination(raw_destination, relative_path)


def _validate_raw_link_destination(destination: str, relative_path: str) -> None:
    if not destination.isascii() or _PERCENT_ESCAPE.search(destination):
        raise DocumentationValidationError(
            f"Invalid Description link destination: {relative_path}."
        )


def _source_link_candidates(content: str) -> Iterable[tuple[str, str]]:
    """Yield source destinations only for syntax that can correspond to parsed links."""
    index = 0
    while index < len(content):
        character = content[index]
        if character == "\\":
            index += 2
            continue
        if character == "`":
            index = _skip_code_span(content, index)
            continue
        if character == "<":
            destination, next_index = _scan_autolink(content, index)
            if destination is not None:
                yield "destination", destination
                index = next_index
                continue
        if character == "[" and (index == 0 or content[index - 1] != "!"):
            label, after_label = _scan_bracketed(content, index)
            if label is not None:
                kind, value, next_index = _scan_link_after_label(content, label, after_label)
                if kind is not None:
                    yield kind, value
                    index = next_index
                    continue
        index += 1


def _skip_code_span(content: str, start: int) -> int:
    delimiter_end = start
    while delimiter_end < len(content) and content[delimiter_end] == "`":
        delimiter_end += 1
    delimiter = content[start:delimiter_end]
    closing = content.find(delimiter, delimiter_end)
    return closing + len(delimiter) if closing >= 0 else delimiter_end


def _scan_autolink(content: str, start: int) -> tuple[str | None, int]:
    closing = content.find(">", start + 1)
    if closing < 0:
        return None, start + 1
    destination = content[start + 1 : closing]
    if ":" not in destination or any(character.isspace() for character in destination):
        return None, closing + 1
    return destination, closing + 1


def _scan_bracketed(content: str, start: int) -> tuple[str | None, int]:
    depth = 1
    index = start + 1
    while index < len(content):
        if content[index] == "\\":
            index += 2
            continue
        if content[index] == "[":
            depth += 1
        elif content[index] == "]":
            depth -= 1
            if depth == 0:
                return content[start + 1 : index], index + 1
        index += 1
    return None, start + 1


def _scan_link_after_label(
    content: str, label: str, start: int
) -> tuple[str | None, str, int]:
    if start < len(content) and content[start] == "(":
        destination, next_index = _scan_inline_destination(content, start + 1)
        if destination is not None:
            return "destination", destination, next_index
        return None, "", start
    if start < len(content) and content[start] == "[":
        reference, next_index = _scan_bracketed(content, start)
        if reference is not None:
            return "reference", reference or label, next_index
        return None, "", start
    return "reference", label, start


def _scan_inline_destination(content: str, start: int) -> tuple[str | None, int]:
    index = start
    while index < len(content) and content[index].isspace():
        index += 1
    if index >= len(content):
        return None, start
    if content[index] == "<":
        closing = content.find(">", index + 1)
        if closing < 0:
            return None, start
        return content[index + 1 : closing], closing + 1

    destination_start = index
    depth = 0
    while index < len(content):
        character = content[index]
        if character == "\\":
            index += 2
            continue
        if character == "(":
            depth += 1
        elif character == ")":
            if depth == 0:
                return content[destination_start:index], index + 1
            depth -= 1
        elif character.isspace() and depth == 0:
            return content[destination_start:index], index
        index += 1
    return None, start


def _raw_reference_destinations(
    source: str, references: Mapping[str, Mapping[str, object]]
) -> dict[str, str]:
    lines = source.splitlines()
    destinations: dict[str, str] = {}
    for key, reference in references.items():
        location = reference.get("map")
        if not isinstance(location, list) or len(location) != 2:
            continue
        definition = "\n".join(lines[location[0] : location[1]])
        parsed_key, destination = _scan_reference_definition(definition)
        if parsed_key == key and destination is not None:
            destinations[key] = destination
    return destinations


def _scan_reference_definition(definition: str) -> tuple[str | None, str | None]:
    index = 0
    while index < len(definition) and index < 3 and definition[index] == " ":
        index += 1
    if index >= len(definition) or definition[index] != "[":
        return None, None
    label, index = _scan_bracketed(definition, index)
    if label is None or index >= len(definition) or definition[index] != ":":
        return None, None
    destination = _scan_reference_destination(definition, index + 1)
    return normalizeReference(label), destination


def _scan_reference_destination(definition: str, start: int) -> str | None:
    index = start
    while index < len(definition) and definition[index].isspace():
        index += 1
    if index >= len(definition):
        return None
    if definition[index] == "<":
        closing = definition.find(">", index + 1)
        return definition[index + 1 : closing] if closing >= 0 else None
    destination_start = index
    while index < len(definition) and not definition[index].isspace():
        if definition[index] == "\\":
            index += 2
        else:
            index += 1
    return definition[destination_start:index]


def _walk_tokens(tokens: Iterable[Token]) -> Iterable[Token]:
    for token in tokens:
        yield token
        yield from _walk_tokens(token.children or [])


def _is_permitted_link_destination(destination: str) -> bool:
    """Return whether a parsed destination meets the fixed RFC 3986 HTTP(S) contract."""
    if not destination.isascii() or not destination:
        return False
    if _PERCENT_ESCAPE.search(destination):
        return False
    if any(character not in _URI_ALLOWED_CHARACTERS for character in destination):
        return False
    try:
        parsed = urlsplit(destination)
        host = parsed.hostname
        _ = parsed.port
    except ValueError:
        return False
    return parsed.scheme.casefold() in {"http", "https"} and bool(parsed.netloc and host)
