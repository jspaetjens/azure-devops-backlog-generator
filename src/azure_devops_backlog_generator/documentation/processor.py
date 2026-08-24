"""Foundation parsing for approved backlog-input Markdown documents."""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

from markdown_it import MarkdownIt
from markdown_it.token import Token

from azure_devops_backlog_generator.documentation.exceptions import (
    DocumentationReadError,
    DocumentationValidationError,
)
from azure_devops_backlog_generator.documentation.models import (
    DocumentationHierarchy,
    HeadingIdentity,
    ParsedDocument,
    ParsedToken,
    SemanticWorkItem,
    TokenSpan,
    WorkItemType,
)

_WORK_ITEM_TYPES = {
    1: WorkItemType.EPIC,
    2: WorkItemType.FEATURE,
    3: WorkItemType.PRODUCT_BACKLOG_ITEM,
    4: WorkItemType.TASK,
}


@dataclass(slots=True)
class _PendingItem:
    level: int
    title: str
    heading_open_index: int
    heading_close_index: int
    source_order: int
    hierarchy: tuple[HeadingIdentity, ...]
    end_index: int = 0
    children: list[_PendingItem] = field(default_factory=list)


class DocumentationProcessor:
    """Discover and parse the Version 1.0 source-document hierarchy."""

    def __init__(self) -> None:
        self._parser = MarkdownIt("commonmark")

    def process(self, source_directory: Path) -> DocumentationHierarchy:
        """Return the deterministic semantic hierarchy for ``source_directory``."""
        files = self._discover_files(source_directory)
        return DocumentationHierarchy(
            documents=tuple(self._parse_file(source_directory, path) for path in files)
        )

    def _discover_files(self, source_directory: Path) -> list[Path]:
        try:
            files = [
                entry
                for entry in source_directory.iterdir()
                if not entry.is_symlink() and entry.is_file() and entry.suffix.casefold() == ".md"
            ]
        except OSError as error:
            message = "Documentation source directory cannot be read."
            raise DocumentationReadError(message) from error

        files.sort(key=lambda path: (_nfc(path.name).casefold(), _nfc(path.name)))
        if not files:
            raise DocumentationValidationError("No eligible Markdown input files were found.")
        return files

    def _parse_file(self, source_directory: Path, path: Path) -> ParsedDocument:
        relative_path = _canonical_relative_path(path, source_directory)
        try:
            source = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError as error:
            raise DocumentationValidationError(
                f"Invalid UTF-8 in source document: {relative_path}."
            ) from error
        except OSError as error:
            message = f"Source document cannot be read: {relative_path}."
            raise DocumentationReadError(message) from error

        tokens = self._parser.parse(source)
        pending_items = self._build_pending_items(tokens, relative_path)
        snapshots = tuple(_snapshot_token(token) for token in tokens)
        return ParsedDocument(
            canonical_relative_path=relative_path,
            tokens=snapshots,
            root_items=tuple(_freeze_item(item, relative_path) for item in pending_items),
        )

    def _build_pending_items(self, tokens: list[Token], relative_path: str) -> list[_PendingItem]:
        roots: list[_PendingItem] = []
        active: list[_PendingItem] = []
        items_in_source_order: list[_PendingItem] = []
        sibling_titles: dict[tuple[int, int | None], set[str]] = {}
        source_order = 0

        for index, token in enumerate(tokens):
            if token.type != "heading_open" or token.level != 0:
                continue
            if token.markup in {"=", "-"}:
                raise DocumentationValidationError(
                    f"Top-level setext heading is not permitted: {relative_path}."
                )
            if not token.markup.startswith("#"):
                continue

            heading_level = int(token.tag.removeprefix("h"))
            if heading_level > 4:
                raise DocumentationValidationError(
                    f"Top-level ATX heading deeper than H4 is not permitted: {relative_path}."
                )
            if index + 2 >= len(tokens) or tokens[index + 1].type != "inline":
                raise DocumentationValidationError(f"Invalid semantic heading: {relative_path}.")

            title = _normalised_title(tokens[index + 1], relative_path)
            while active and active[-1].level >= heading_level:
                active.pop()
            parent = active[-1] if active else None
            self._validate_parent(heading_level, parent, relative_path)

            sibling_key = (heading_level, id(parent) if parent else None)
            titles = sibling_titles.setdefault(sibling_key, set())
            if title in titles:
                raise DocumentationValidationError(
                    f"Duplicate normalised sibling title: {title!r} in {relative_path}."
                )
            titles.add(title)

            hierarchy = (
                (*parent.hierarchy, HeadingIdentity(heading_level, title))
                if parent
                else (HeadingIdentity(heading_level, title),)
            )
            item = _PendingItem(
                level=heading_level,
                title=title,
                heading_open_index=index,
                heading_close_index=index + 2,
                source_order=source_order,
                hierarchy=hierarchy,
            )
            source_order += 1
            items_in_source_order.append(item)
            if parent:
                parent.children.append(item)
            else:
                roots.append(item)
            active.append(item)
        for item_index, item in enumerate(items_in_source_order):
            item.end_index = next(
                (
                    later.heading_open_index
                    for later in items_in_source_order[item_index + 1 :]
                    if later.level <= item.level
                ),
                len(tokens),
            )
        return roots

    @staticmethod
    def _validate_parent(level: int, parent: _PendingItem | None, relative_path: str) -> None:
        if level == 1:
            return
        if parent is None:
            names = {2: "Feature", 3: "Product Backlog Item", 4: "Task"}
            raise DocumentationValidationError(f"Orphan {names[level]}: {relative_path}.")
        if parent.level != level - 1:
            raise DocumentationValidationError(
                f"Skipped semantic hierarchy level before H{level}: {relative_path}."
            )


def _freeze_item(item: _PendingItem, relative_path: str) -> SemanticWorkItem:
    children = tuple(_freeze_item(child, relative_path) for child in item.children)
    body_end = item.children[0].heading_open_index if item.children else item.end_index
    spans = (
        (TokenSpan(item.heading_close_index + 1, body_end),)
        if item.heading_close_index + 1 < body_end
        else ()
    )
    return SemanticWorkItem(
        work_item_type=_WORK_ITEM_TYPES[item.level],
        level=item.level,
        title=item.title,
        canonical_relative_path=relative_path,
        heading_hierarchy=item.hierarchy,
        source_order=item.source_order,
        direct_body_token_spans=spans,
        children=children,
    )
def _normalised_title(inline_token: Token, relative_path: str) -> str:
    text = _visible_inline_text(inline_token.children or [], relative_path)
    title = " ".join(text.split())
    if not title:
        raise DocumentationValidationError(f"Empty normalised semantic title: {relative_path}.")
    if len(title) > 255:
        message = f"Semantic title exceeds 255 characters: {relative_path}."
        raise DocumentationValidationError(message)
    return title


def _visible_inline_text(tokens: list[Token], relative_path: str) -> str:
    parts: list[str] = []
    for token in tokens:
        if token.type == "html_inline":
            raise DocumentationValidationError(
                f"Inline HTML in semantic title is not permitted: {relative_path}."
            )
        if token.type in {"text", "code_inline", "softbreak", "hardbreak"}:
            parts.append(token.content)
        elif token.type == "image":
            parts.append(_visible_inline_text(token.children or [], relative_path))
    return "".join(parts)


def _snapshot_token(token: Token) -> ParsedToken:
    return ParsedToken(
        type=token.type,
        tag=token.tag,
        nesting=token.nesting,
        level=token.level,
        markup=token.markup,
        content=token.content,
        map=tuple(token.map) if token.map is not None else None,
        info=token.info,
        attrs=tuple(sorted(token.attrs.items())),
        children=tuple(_snapshot_token(child) for child in token.children or []),
    )


def _canonical_relative_path(path: Path, source_directory: Path) -> str:
    relative = path.relative_to(source_directory)
    return "/".join(_nfc(part) for part in relative.parts)


def _nfc(value: str) -> str:
    return unicodedata.normalize("NFC", value)
