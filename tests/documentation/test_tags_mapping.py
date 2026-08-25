"""Tests for the Version 1.0 Tags Mapping contract."""

from pathlib import Path

import pytest
from markdown_it import MarkdownIt

from azure_devops_backlog_generator.documentation.exceptions import DocumentationValidationError
from azure_devops_backlog_generator.documentation.models import WorkItemType
from azure_devops_backlog_generator.documentation.processor import DocumentationProcessor
from azure_devops_backlog_generator.documentation.tags import prepare_tags


def _item(tmp_path: Path, content: str):
    (tmp_path / "input.md").write_text(content, encoding="utf-8")
    return DocumentationProcessor().process(tmp_path).documents[0].root_items[0]


def test_prepares_optional_tags_for_all_supported_work_item_types(tmp_path: Path) -> None:
    epic = _item(
        tmp_path,
        "# Epic\nDescription\n\nTags:\n\n- epic\n"
        "## Feature\nDescription\n\nTags:\n\n- feature\n"
        "### PBI\nDescription\n\nTags:\n\n- pbi\n"
        "#### Task\nDescription\n\nTags:\n\n- task\n",
    )
    feature = epic.children[0]
    pbi = feature.children[0]
    task = pbi.children[0]

    assert [item.work_item_type for item in (epic, feature, pbi, task)] == list(WorkItemType)
    assert [item.tags_value for item in (epic, feature, pbi, task)] == [
        "epic",
        "feature",
        "pbi",
        "task",
    ]


def test_no_tags_marker_produces_no_tags_value(tmp_path: Path) -> None:
    item = _item(tmp_path, "# Epic\nDescription\n")

    assert item.tags_value is None


@pytest.mark.parametrize(
    "marker",
    ["tags:", "Tags: extra", "Tags :"],
)
def test_non_exact_direct_body_markers_remain_description(marker: str, tmp_path: Path) -> None:
    item = _item(tmp_path, f"# Epic\nDescription\n\n{marker}\n")

    assert item.tags_value is None
    assert item.description_html == f"<p>Description</p>\n<p>{marker}</p>\n"


@pytest.mark.parametrize(
    "body",
    ["> Tags:\n", "- Tags:\n", "```text\nTags:\n```\n", "    Tags:\n"],
)
def test_marker_looking_container_content_is_not_reserved(body: str, tmp_path: Path) -> None:
    assert _item(tmp_path, f"# Epic\n{body}").tags_value is None


def test_marker_looking_html_block_remains_description_and_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(DocumentationValidationError, match="Raw HTML"):
        _item(tmp_path, "# Epic\n<div>\nTags:\n</div>\n")


@pytest.mark.parametrize(
    ("body", "message"),
    [
        ("Tags:\n\n- one\n\nTags:\n\n- two\n", "Duplicate Tags"),
        ("Acceptance Criteria:\n\n- criterion\n\nTags:\n\n- tag\n", "must precede"),
    ],
)
def test_rejects_duplicate_or_reversed_reserved_markers(
    body: str, message: str, tmp_path: Path
) -> None:
    with pytest.raises(DocumentationValidationError, match=message):
        _item(tmp_path, f"# Epic\nDescription\n\n{body}")


def test_tags_stop_before_acceptance_criteria_and_preserve_description(tmp_path: Path) -> None:
    item = _item(
        tmp_path,
        "# Epic\nDescription\n\nTags:\n\n- alpha\n- beta\n\n"
        "Acceptance Criteria:\n\n- criterion\n",
    )

    assert item.description_html == "<p>Description</p>\n"
    assert item.tags_value == "alpha; beta"
    assert item.acceptance_criteria_html == "<ul>\n<li>criterion</li>\n</ul>\n"


@pytest.mark.parametrize(
    ("body", "message"),
    [
        ("1. tag\n", "unordered list"),
        ("- one\n\n---\n\n- two\n", "exactly one"),
        ("Before\n\n- tag\n", "exactly one"),
        ("- tag\n\nAfter\n", "exactly one"),
        ("- parent\n  - child\n", "Nested"),
        ("-\n", "Tag is empty"),
        ("-   \n", "Tag is empty"),
    ],
)
def test_rejects_invalid_tags_list_grammar(
    body: str, message: str, tmp_path: Path
) -> None:
    with pytest.raises(DocumentationValidationError, match=message):
        _item(tmp_path, f"# Epic\nDescription\n\nTags:\n\n{body}")


@pytest.mark.parametrize(
    ("tag", "expected"),
    [
        ("  Alpha\u00a0\u00a0Beta  ", "Alpha Beta"),
        ("*Em* **Strong** `Code`", "Em Strong Code"),
        ("A &amp; B \\!", "A & B !"),
        ("[Visible](https://example.test/path)", "Visible"),
        ("\u58f0", "\u58f0"),
    ],
)
def test_extracts_and_normalises_visible_tag_text(
    tag: str, expected: str, tmp_path: Path
) -> None:
    item = _item(tmp_path, f"# Epic\nDescription\n\nTags:\n\n- {tag}\n")

    assert item.tags_value == expected


def test_prepares_exact_delimiter_and_preserves_source_order(tmp_path: Path) -> None:
    item = _item(
        tmp_path,
        "# Epic\nDescription\n\nTags:\n\n- zebra\n- Alpha\n- middle\n",
    )

    assert item.tags_value == "zebra; Alpha; middle"


@pytest.mark.parametrize(
    "tag",
    [
        "contains,comma",
        "contains;semicolon",
        "x" * 401,
        "control\u0001character",
        "format\u200echaracter",
    ],
)
def test_rejects_invalid_normalised_tag_values(tag: str, tmp_path: Path) -> None:
    with pytest.raises(DocumentationValidationError):
        _item(tmp_path, f"# Epic\nDescription\n\nTags:\n\n- {tag}\n")


def test_rejects_an_unpaired_surrogate_when_preparation_is_called_in_memory() -> None:
    parser = MarkdownIt("commonmark")
    source = "Tags:\n\n- surrogate\ud800\n"
    tokens = parser.parse(source)

    with pytest.raises(DocumentationValidationError, match="prohibited Unicode"):
        prepare_tags(
            parser=parser,
            tokens=tokens,
            start=0,
            end=len(tokens),
            work_item_type=WorkItemType.EPIC,
            relative_path="input.md",
            source=source,
        )


def test_accepts_tag_of_exactly_400_characters(tmp_path: Path) -> None:
    item = _item(tmp_path, f"# Epic\nDescription\n\nTags:\n\n- {'x' * 400}\n")

    assert item.tags_value == "x" * 400


@pytest.mark.parametrize(
    "body",
    ["- alpha\n- alpha\n", "- Alpha\n- alpha\n"],
)
def test_rejects_exact_and_casefold_duplicate_tags(body: str, tmp_path: Path) -> None:
    with pytest.raises(DocumentationValidationError, match="Duplicate Tags"):
        _item(tmp_path, f"# Epic\nDescription\n\nTags:\n\n{body}")


def test_distinct_prefix_tags_are_not_duplicates(tmp_path: Path) -> None:
    item = _item(tmp_path, "# Epic\nDescription\n\nTags:\n\n- api\n- api-client\n")

    assert item.tags_value == "api; api-client"


@pytest.mark.parametrize(
    "tag",
    [
        "[HTTP](http://example.test/path)",
        "[HTTPS](https://example.test/path)",
        "<https://example.test/path>",
        "[reference][id]\n\n[id]: https://example.test/path",
        "`[not](https://\u00e9xample.test/a\\(b\\))`",
    ],
)
def test_valid_tag_link_content_uses_visible_text_or_code(tag: str, tmp_path: Path) -> None:
    item = _item(tmp_path, f"# Epic\nDescription\n\nTags:\n\n- {tag}\n")

    assert item.tags_value is not None


@pytest.mark.parametrize(
    "tag",
    [
        "[relative](guide.md)",
        "[unicode](https://\u00e9xample.test/path)",
        "![image](https://example.test/image.png)",
        "Text <em>HTML</em>",
    ],
)
def test_rejects_invalid_tag_link_html_and_image_content(tag: str, tmp_path: Path) -> None:
    with pytest.raises(DocumentationValidationError):
        _item(tmp_path, f"# Epic\nDescription\n\nTags:\n\n- {tag}\n")


def test_rejects_html_block_in_tags(tmp_path: Path) -> None:
    with pytest.raises(DocumentationValidationError):
        _item(tmp_path, "# Epic\nDescription\n\nTags:\n\n- tag\n\n<div>HTML</div>\n")


def test_tags_respect_child_and_sibling_boundaries(tmp_path: Path) -> None:
    epic = _item(
        tmp_path,
        "# Epic\nDescription\n\nTags:\n\n- epic\n"
        "## Feature\nDescription\n\nTags:\n\n- feature\n"
        "## Sibling\nDescription\n",
    )

    assert epic.tags_value == "epic"
    assert epic.children[0].tags_value == "feature"
    assert epic.children[1].tags_value is None
