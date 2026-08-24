"""Immutable models produced by the Documentation Processor foundation."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class WorkItemType(StrEnum):
    """The fixed Version 1.0 source work-item types."""

    EPIC = "Epic"
    FEATURE = "Feature"
    PRODUCT_BACKLOG_ITEM = "Product Backlog Item"
    TASK = "Task"


@dataclass(frozen=True, slots=True)
class HeadingIdentity:
    """One normalised semantic heading in a source item's identity path."""

    level: int
    title: str


@dataclass(frozen=True, slots=True)
class TokenSpan:
    """A half-open range in a document's immutable parsed-token sequence."""

    start: int
    end: int


@dataclass(frozen=True, slots=True)
class ParsedToken:
    """An immutable snapshot of a markdown-it block or inline token."""

    type: str
    tag: str
    nesting: int
    level: int
    markup: str
    content: str
    map: tuple[int, int] | None
    info: str
    attrs: tuple[tuple[str, str], ...]
    children: tuple[ParsedToken, ...]


@dataclass(frozen=True, slots=True)
class SemanticWorkItem:
    """A source work item and its structural direct-body boundaries."""

    work_item_type: WorkItemType
    level: int
    title: str
    canonical_relative_path: str
    heading_hierarchy: tuple[HeadingIdentity, ...]
    source_order: int
    direct_body_token_spans: tuple[TokenSpan, ...]
    children: tuple[SemanticWorkItem, ...]


@dataclass(frozen=True, slots=True)
class ParsedDocument:
    """A parsed source document and its root Epic items."""

    canonical_relative_path: str
    tokens: tuple[ParsedToken, ...]
    root_items: tuple[SemanticWorkItem, ...]


@dataclass(frozen=True, slots=True)
class DocumentationHierarchy:
    """All parsed source documents in deterministic processing order."""

    documents: tuple[ParsedDocument, ...]
