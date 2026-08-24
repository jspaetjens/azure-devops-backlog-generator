"""Tests for Documentation Processor foundation discovery and hierarchy parsing."""

from pathlib import Path

import pytest

from azure_devops_backlog_generator.documentation.exceptions import (
    DocumentationReadError,
    DocumentationValidationError,
)
from azure_devops_backlog_generator.documentation.models import WorkItemType
from azure_devops_backlog_generator.documentation.processor import DocumentationProcessor


def _process(tmp_path: Path, filename: str = "input.md", content: str = "# Epic\n"):
    (tmp_path / filename).write_text(content, encoding="utf-8")
    return DocumentationProcessor().process(tmp_path)


def test_requires_at_least_one_eligible_markdown_file(tmp_path: Path) -> None:
    (tmp_path / "notes.txt").write_text("# Not input", encoding="utf-8")

    with pytest.raises(DocumentationValidationError, match="No eligible"):
        DocumentationProcessor().process(tmp_path)


def test_discovers_direct_markdown_files_in_deterministic_casefold_order(tmp_path: Path) -> None:
    (tmp_path / "nested").mkdir()
    (tmp_path / "nested" / "hidden.md").write_text("# Hidden", encoding="utf-8")
    (tmp_path / "ignore.txt").write_text("# Ignore", encoding="utf-8")
    (tmp_path / "b.md").write_text("# B", encoding="utf-8")
    (tmp_path / "A.MD").write_text("# A", encoding="utf-8")

    hierarchy = DocumentationProcessor().process(tmp_path)

    paths = [document.canonical_relative_path for document in hierarchy.documents]
    assert paths == ["A.MD", "b.md"]


def test_excludes_symlinked_markdown_file_where_supported(tmp_path: Path) -> None:
    target = tmp_path / "target.md"
    target.write_text("# Target", encoding="utf-8")
    linked = tmp_path / "linked.md"
    try:
        linked.symlink_to(target)
    except OSError:
        pytest.skip("Symlink creation is unavailable on this platform.")

    hierarchy = DocumentationProcessor().process(tmp_path)

    assert [document.canonical_relative_path for document in hierarchy.documents] == ["target.md"]


def test_accepts_utf8_bom_and_preserves_unicode_title(tmp_path: Path) -> None:
    path = tmp_path / "input.md"
    path.write_bytes("\ufeff# Café\n".encode("utf-8"))

    hierarchy = DocumentationProcessor().process(tmp_path)

    assert hierarchy.documents[0].root_items[0].title == "Café"


def test_rejects_invalid_utf8(tmp_path: Path) -> None:
    (tmp_path / "input.md").write_bytes(b"# Invalid\xff")

    with pytest.raises(DocumentationValidationError, match="Invalid UTF-8"):
        DocumentationProcessor().process(tmp_path)


def test_reports_an_unreadable_matching_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "input.md"
    path.write_text("# Epic", encoding="utf-8")
    original_read_text = Path.read_text

    def denied(self: Path, *args: object, **kwargs: object) -> str:
        if self == path:
            raise PermissionError
        return original_read_text(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", denied)
    with pytest.raises(DocumentationReadError, match="cannot be read"):
        DocumentationProcessor().process(tmp_path)


def test_uses_nfc_canonical_filenames_and_repeated_processing_is_identical(tmp_path: Path) -> None:
    _process(tmp_path, "Cafe\u0301.md", "# First\n")
    _process(tmp_path, "café.md", "# Second\n")

    first = DocumentationProcessor().process(tmp_path)
    second = DocumentationProcessor().process(tmp_path)

    paths = [document.canonical_relative_path for document in first.documents]
    assert paths == ["Café.md", "café.md"]
    assert first == second


@pytest.mark.parametrize(
    ("content", "expected_types"),
    [
        ("# Epic\n", [WorkItemType.EPIC]),
        ("# Epic\n## Feature\n", [WorkItemType.EPIC, WorkItemType.FEATURE]),
        (
            "# Epic\n## Feature\n### PBI\n#### Task\n",
            [
                WorkItemType.EPIC,
                WorkItemType.FEATURE,
                WorkItemType.PRODUCT_BACKLOG_ITEM,
                WorkItemType.TASK,
            ],
        ),
    ],
)
def test_builds_the_fixed_hierarchy(
    content: str, expected_types: list[WorkItemType], tmp_path: Path
) -> None:
    root = _process(tmp_path, content=content).documents[0].root_items[0]
    items = [root]
    while items[-1].children:
        items.append(items[-1].children[0])

    assert [item.work_item_type for item in items] == expected_types
    assert [item.source_order for item in items] == list(range(len(items)))


def test_permits_siblings_multiple_epics_and_resets_hierarchy(tmp_path: Path) -> None:
    hierarchy = _process(tmp_path, content="# One\n## A\n## B\n# Two\n## C\n")
    first, second = hierarchy.documents[0].root_items

    assert [item.title for item in first.children] == ["A", "B"]
    assert second.children[0].heading_hierarchy == (
        second.heading_hierarchy[0],
        second.children[0].heading_hierarchy[1],
    )


@pytest.mark.parametrize(
    ("content", "message"),
    [
        ("## Feature\n", "Orphan Feature"),
        ("### PBI\n", "Orphan Product Backlog Item"),
        ("#### Task\n", "Orphan Task"),
        ("# Epic\n### PBI\n", "Skipped semantic hierarchy"),
        ("# Epic\nFeature\n-------\n", "setext"),
        ("# Epic\n##### Too deep\n", "deeper than H4"),
    ],
)
def test_rejects_invalid_semantic_hierarchy(
    content: str, message: str, tmp_path: Path
) -> None:
    with pytest.raises(DocumentationValidationError, match=message):
        _process(tmp_path, content=content)


def test_ignores_heading_like_content_in_non_semantic_containers(tmp_path: Path) -> None:
    hierarchy = _process(
        tmp_path,
        content="# Epic\n> ## Quoted\n- ### Listed\n```markdown\n#### Fenced\n```\n",
    )

    root = hierarchy.documents[0].root_items[0]
    assert root.title == "Epic"
    assert root.children == ()


def test_extracts_visible_commonmark_title_text_and_normalises_whitespace(tmp_path: Path) -> None:
    hierarchy = _process(
        tmp_path,
        content=(
            "#  *Em* **Strong** `Code` [Link](https://example.test) "
            "![Alt *Text*](x)  \u00a0 \n"
        ),
    )

    assert hierarchy.documents[0].root_items[0].title == "Em Strong Code Link Alt Text"


@pytest.mark.parametrize(
    ("content", "message"),
    [
        ("#    \n", "Empty normalised"),
        ("# " + "x" * 256 + "\n", "exceeds 255"),
        ("# Title <em>HTML</em>\n", "Inline HTML"),
    ],
)
def test_rejects_invalid_semantic_titles(content: str, message: str, tmp_path: Path) -> None:
    with pytest.raises(DocumentationValidationError, match=message):
        _process(tmp_path, content=content)


def test_accepts_a_semantic_title_of_exactly_255_characters(tmp_path: Path) -> None:
    title = "x" * 255

    hierarchy = _process(tmp_path, content=f"# {title}\n")

    assert hierarchy.documents[0].root_items[0].title == title
    assert len(hierarchy.documents[0].root_items[0].title) == 255


@pytest.mark.parametrize(
    ("content", "expected_title"),
    [
        ("# Escape \\*marker\\* \\!\n", "Escape *marker* !"),
        ("# A &amp; B\n", "A & B"),
        ("# <https://example.test/path>\n", "https://example.test/path"),
    ],
)
def test_uses_commonmark_visible_text_for_escaped_entity_and_autolink_titles(
    content: str, expected_title: str, tmp_path: Path
) -> None:
    hierarchy = _process(tmp_path, content=content)

    assert hierarchy.documents[0].root_items[0].title == expected_title


def test_rejects_duplicate_normalised_sibling_titles_but_allows_distinct_parents(
    tmp_path: Path,
) -> None:
    with pytest.raises(DocumentationValidationError, match="Duplicate"):
        _process(tmp_path, content="# Epic\n## Same\n##  Same\n")

    hierarchy = _process(tmp_path, content="# One\n## Same\n# Two\n## Same\n")
    titles = [root.children[0].title for root in hierarchy.documents[0].root_items]
    assert titles == ["Same", "Same"]


def test_rejects_duplicate_normalised_root_epic_titles(tmp_path: Path) -> None:
    with pytest.raises(DocumentationValidationError, match="Duplicate"):
        _process(tmp_path, content="# Same\n#  Same\n")


def test_preserves_a_non_empty_direct_body_span_to_end_of_file(tmp_path: Path) -> None:
    document = _process(tmp_path, content="# Epic\n\nSome body content.\n").documents[0]
    epic = document.root_items[0]

    assert [(span.start, span.end) for span in epic.direct_body_token_spans] == [
        (3, len(document.tokens))
    ]
    span = epic.direct_body_token_spans[0]
    assert [token.type for token in document.tokens[span.start : span.end]] == [
        "paragraph_open",
        "inline",
        "paragraph_close",
    ]
    assert epic.children == ()


def test_preserves_structural_direct_body_spans(tmp_path: Path) -> None:
    document = _process(
        tmp_path,
        content="# Epic\nEpic body\n## Feature\nFeature body\n## Sibling\nSibling body\n# Next\n",
    ).documents[0]
    epic, next_epic = document.root_items
    feature, sibling = epic.children

    assert [(span.start, span.end) for span in epic.direct_body_token_spans] == [(3, 6)]
    assert [(span.start, span.end) for span in feature.direct_body_token_spans] == [(9, 12)]
    assert [(span.start, span.end) for span in sibling.direct_body_token_spans] == [(15, 18)]
    assert next_epic.direct_body_token_spans == ()
    assert document.tokens[feature.direct_body_token_spans[0].start].type == "paragraph_open"


def test_preserves_direct_body_spans_for_a_populated_full_hierarchy(tmp_path: Path) -> None:
    document = _process(
        tmp_path,
        content=(
            "# Epic\nEpic body\n## Feature\nFeature body\n### PBI\nPBI body\n"
            "#### Task\nTask body\n"
        ),
    ).documents[0]
    epic = document.root_items[0]
    feature = epic.children[0]
    pbi = feature.children[0]
    task = pbi.children[0]

    for item, expected_span in zip(
        (epic, feature, pbi, task),
        ((3, 6), (9, 12), (15, 18), (21, len(document.tokens))),
        strict=True,
    ):
        assert [(span.start, span.end) for span in item.direct_body_token_spans] == [
            expected_span
        ]
        span = item.direct_body_token_spans[0]
        assert [token.type for token in document.tokens[span.start : span.end]] == [
            "paragraph_open",
            "inline",
            "paragraph_close",
        ]


def test_ignores_h5_looking_text_inside_a_fenced_code_block(tmp_path: Path) -> None:
    hierarchy = _process(
        tmp_path,
        content="# Epic\n```markdown\n##### Not semantic\n```\n## Feature\n",
    )

    epic = hierarchy.documents[0].root_items[0]
    assert epic.title == "Epic"
    assert [child.title for child in epic.children] == ["Feature"]
