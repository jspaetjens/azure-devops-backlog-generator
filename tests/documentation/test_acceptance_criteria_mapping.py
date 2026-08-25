"""Tests for the Version 1.0 Acceptance Criteria Mapping contract."""

from pathlib import Path

import pytest
from markdown_it import MarkdownIt

from azure_devops_backlog_generator.documentation.acceptance_criteria import (
    prepare_acceptance_criteria,
)
from azure_devops_backlog_generator.documentation.exceptions import DocumentationValidationError
from azure_devops_backlog_generator.documentation.models import WorkItemType
from azure_devops_backlog_generator.documentation.processor import DocumentationProcessor


def _item(tmp_path: Path, content: str):
    (tmp_path / "input.md").write_text(content, encoding="utf-8")
    return DocumentationProcessor().process(tmp_path).documents[0].root_items[0]


def test_prepares_optional_acceptance_criteria_for_each_supported_type(tmp_path: Path) -> None:
    epic = _item(
        tmp_path,
        "# Epic\nDescription\n\nAcceptance Criteria:\n\n- Epic criterion\n"
        "## Feature\nDescription\n\nAcceptance Criteria:\n\n- Feature criterion\n"
        "### PBI\nDescription\n\nAcceptance Criteria:\n\n- PBI criterion\n",
    )

    assert epic.acceptance_criteria_html == "<ul>\n<li>Epic criterion</li>\n</ul>\n"
    assert epic.children[0].acceptance_criteria_html == (
        "<ul>\n<li>Feature criterion</li>\n</ul>\n"
    )
    assert epic.children[0].children[0].acceptance_criteria_html == (
        "<ul>\n<li>PBI criterion</li>\n</ul>\n"
    )


def test_no_marker_produces_no_acceptance_criteria_value(tmp_path: Path) -> None:
    item = _item(tmp_path, "# Epic\nDescription\n")

    assert item.acceptance_criteria_html is None


@pytest.mark.parametrize(
    "marker",
    [
        "acceptance criteria:",
        "Acceptance criteria:",
        "Acceptance Criteria: extra",
        "Acceptance Criteria :",
    ],
)
def test_non_exact_direct_body_markers_remain_description(
    marker: str, tmp_path: Path
) -> None:
    item = _item(tmp_path, f"# Epic\nDescription\n\n{marker}\n")

    assert item.acceptance_criteria_html is None
    assert item.description_html == f"<p>Description</p>\n<p>{marker}</p>\n"


def test_rejects_recognised_acceptance_criteria_on_task(tmp_path: Path) -> None:
    with pytest.raises(DocumentationValidationError, match="not permitted for Task"):
        _item(
            tmp_path,
            "# Epic\nDescription\n## Feature\nDescription\n### PBI\nDescription\n"
            "#### Task\nDescription\n\nAcceptance Criteria:\n\n- Criterion\n",
        )


@pytest.mark.parametrize(
    ("body", "expected"),
    [
        ("- One\n- Two\n", "<ul>\n<li>One</li>\n<li>Two</li>\n</ul>\n"),
        ("1. One\n2. Two\n", "<ol>\n<li>One</li>\n<li>Two</li>\n</ol>\n"),
        (
            "- First paragraph.\n\n  Second paragraph.\n",
            "<ul>\n<li>\n<p>First paragraph.</p>\n<p>Second paragraph.</p>\n</li>\n</ul>\n",
        ),
    ],
)
def test_accepts_list_forms_and_preserves_exact_html(
    body: str, expected: str, tmp_path: Path
) -> None:
    item = _item(tmp_path, f"# Epic\nDescription\n\nAcceptance Criteria:\n\n{body}")

    assert item.acceptance_criteria_html == expected


def test_renders_complex_inline_content_and_final_lf(tmp_path: Path) -> None:
    item = _item(
        tmp_path,
        "# Epic\nDescription\n\nAcceptance Criteria:\n\n"
        "- *em* **strong** `code` [link](https://example.test) 声\n",
    )

    assert item.acceptance_criteria_html == (
        '<ul>\n<li><em>em</em> <strong>strong</strong> <code>code</code> '
        '<a href="https://example.test">link</a> 声</li>\n</ul>\n'
    )
    assert item.acceptance_criteria_html.endswith("\n")


@pytest.mark.parametrize(
    ("body", "message"),
    [
        ("", "exactly one top-level list"),
        ("Before\n\n- Criterion\n", "exactly one top-level list"),
        ("- Criterion\n\nAfter\n", "exactly one top-level list"),
        ("- One\n\n---\n\n- Two\n", "exactly one top-level list"),
        ("- Parent\n  - Child\n", "Nested"),
        ("-\n", "list is empty|Criterion is empty"),
        ("-   \n", "list is empty|Criterion is empty"),
    ],
)
def test_rejects_invalid_acceptance_criteria_list_grammar(
    body: str, message: str, tmp_path: Path
) -> None:
    with pytest.raises(DocumentationValidationError, match=message):
        _item(tmp_path, f"# Epic\nDescription\n\nAcceptance Criteria:\n\n{body}")


@pytest.mark.parametrize(
    "body",
    [
        "> Acceptance Criteria:\n",
        "- Acceptance Criteria:\n",
        "```text\nAcceptance Criteria:\n```\n",
        "    Acceptance Criteria:\n",
    ],
)
def test_marker_looking_container_content_remains_description(
    body: str, tmp_path: Path
) -> None:
    assert _item(tmp_path, f"# Epic\n{body}").acceptance_criteria_html is None


def test_marker_looking_html_block_remains_description_and_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(DocumentationValidationError, match="Raw HTML"):
        _item(tmp_path, "# Epic\n<div>\nAcceptance Criteria:\n</div>\n")


def test_rejects_duplicate_marker_and_reversed_tags_order(tmp_path: Path) -> None:
    for body, message in (
        ("Acceptance Criteria:\n\n- One\n\nAcceptance Criteria:\n\n- Two\n", "Duplicate"),
        ("Acceptance Criteria:\n\n- One\n\nTags:\n\n- Two\n", "must precede"),
    ):
        with pytest.raises(DocumentationValidationError, match=message):
            _item(tmp_path, f"# Epic\nDescription\n\n{body}")


def test_tags_before_acceptance_criteria_is_partitioned(tmp_path: Path) -> None:
    item = _item(
        tmp_path,
        "# Epic\nDescription\n\nTags:\n\n- Deferred tag\n\n"
        "Acceptance Criteria:\n\n- Criterion\n",
    )

    assert item.description_html == "<p>Description</p>\n"
    assert item.acceptance_criteria_html == "<ul>\n<li>Criterion</li>\n</ul>\n"


@pytest.mark.parametrize(
    "criterion",
    [
        "[HTTP](http://example.test/path)",
        "[HTTPS](https://example.test/path)",
        "<https://example.test/path>",
        "[reference][id]\n\n[id]: https://example.test/path",
        "[id][]\n\n[id]: https://example.test/path",
        "[id]\n\n[id]: https://example.test/path",
        "[parentheses](https://example.test/a(b(c)))",
        r"[escaped](https://example.test/a\(b\))",
        r"`[not](https://example.test/a\(b\))`",
    ],
)
def test_acceptance_criteria_reuses_valid_link_contract(
    criterion: str, tmp_path: Path
) -> None:
    item = _item(tmp_path, f"# Epic\nDescription\n\nAcceptance Criteria:\n\n- {criterion}\n")

    assert item.acceptance_criteria_html is not None


def test_rejects_raw_unicode_reference_destination_in_acceptance_criteria(
    tmp_path: Path,
) -> None:
    with pytest.raises(DocumentationValidationError, match="Invalid Description link"):
        _item(
            tmp_path,
            "# Epic\nDescription\n\nAcceptance Criteria:\n\n"
            "- Criterion with [link][ref]\n\n"
            "[ref]: https://\u00e9xample.test/path\n",
        )


@pytest.mark.parametrize(
    "criterion",
    [
        "- Criterion\n\n  ```text\n  [not a link](https://\u00e9xample.test/a\\(b\\))\n  ```\n",
        "- Criterion\n\n      [not a link](https://\u00e9xample.test/a\\(b\\))\n",
    ],
)
def test_link_looking_code_in_acceptance_criteria_is_not_validated_as_a_link(
    criterion: str, tmp_path: Path
) -> None:
    item = _item(tmp_path, f"# Epic\nDescription\n\nAcceptance Criteria:\n\n{criterion}")

    assert item.acceptance_criteria_html is not None
    assert "<code" in item.acceptance_criteria_html
    assert "[not a link](https://\u00e9xample.test/a\\(b\\))" in item.acceptance_criteria_html


@pytest.mark.parametrize(
    "criterion",
    [
        "[relative](guide.md)",
        "[mailto](mailto:person@example.test)",
        "[hostless](https:///guide)",
        "[port](https://example.test:not-a-port/guide)",
        "[percent](https://example.test/%zz)",
        "[unicode](https://éxample.test/path)",
        "![image](https://example.test/image.png)",
        "Text <em>HTML</em>",
    ],
)
def test_rejects_invalid_acceptance_criteria_content(criterion: str, tmp_path: Path) -> None:
    with pytest.raises(DocumentationValidationError):
        _item(tmp_path, f"# Epic\nDescription\n\nAcceptance Criteria:\n\n- {criterion}\n")


def test_rejects_html_block_in_acceptance_criteria(tmp_path: Path) -> None:
    with pytest.raises(DocumentationValidationError):
        _item(
            tmp_path,
            "# Epic\nDescription\n\nAcceptance Criteria:\n\n- Criterion\n\n<div>HTML</div>\n",
        )


def test_acceptance_criteria_runs_to_direct_body_boundary(tmp_path: Path) -> None:
    epic = _item(
        tmp_path,
        "# Epic\nDescription\n\nAcceptance Criteria:\n\n- Epic\n"
        "## Feature\nDescription\n\nAcceptance Criteria:\n\n- Feature\n"
        "## Sibling\nDescription\n",
    )

    assert epic.acceptance_criteria_html == "<ul>\n<li>Epic</li>\n</ul>\n"
    assert epic.children[0].acceptance_criteria_html == "<ul>\n<li>Feature</li>\n</ul>\n"
    assert epic.children[1].acceptance_criteria_html is None


def test_full_hierarchy_preserves_acceptance_criteria_and_descriptions(tmp_path: Path) -> None:
    epic = _item(
        tmp_path,
        "# Epic\nEpic description\n\nAcceptance Criteria:\n\n- Epic criterion\n"
        "## Feature\nFeature description\n\nAcceptance Criteria:\n\n- Feature criterion\n"
        "### PBI\nPBI description\n\nAcceptance Criteria:\n\n- PBI criterion\n"
        "#### Task\nTask description\n",
    )
    feature = epic.children[0]
    pbi = feature.children[0]
    task = pbi.children[0]

    assert [item.work_item_type for item in (epic, feature, pbi, task)] == list(WorkItemType)
    assert [item.description_html for item in (epic, feature, pbi, task)] == [
        "<p>Epic description</p>\n",
        "<p>Feature description</p>\n",
        "<p>PBI description</p>\n",
        "<p>Task description</p>\n",
    ]
    assert [item.acceptance_criteria_html for item in (epic, feature, pbi, task)] == [
        "<ul>\n<li>Epic criterion</li>\n</ul>\n",
        "<ul>\n<li>Feature criterion</li>\n</ul>\n",
        "<ul>\n<li>PBI criterion</li>\n</ul>\n",
        None,
    ]


def test_reports_acceptance_criteria_renderer_failures(monkeypatch: pytest.MonkeyPatch) -> None:
    parser = MarkdownIt("commonmark")
    tokens = parser.parse("Acceptance Criteria:\n\n- Criterion\n")
    marker = 0

    def fail(*args: object, **kwargs: object) -> str:
        raise RuntimeError("renderer unavailable")

    monkeypatch.setattr(parser.renderer, "render", fail)
    with pytest.raises(DocumentationValidationError, match="Acceptance Criteria rendering failed"):
        prepare_acceptance_criteria(
            parser=parser,
            tokens=tokens,
            start=marker,
            end=len(tokens),
            work_item_type=WorkItemType.EPIC,
            relative_path="input.md",
            source="Acceptance Criteria:\n\n- Criterion\n",
        )


def test_rejects_empty_rendered_acceptance_criteria(monkeypatch: pytest.MonkeyPatch) -> None:
    parser = MarkdownIt("commonmark")
    tokens = parser.parse("Acceptance Criteria:\n\n- Criterion\n")
    monkeypatch.setattr(parser.renderer, "render", lambda *args: "")

    with pytest.raises(DocumentationValidationError, match="Empty rendered Acceptance Criteria"):
        prepare_acceptance_criteria(
            parser=parser,
            tokens=tokens,
            start=0,
            end=len(tokens),
            work_item_type=WorkItemType.EPIC,
            relative_path="input.md",
            source="Acceptance Criteria:\n\n- Criterion\n",
        )
