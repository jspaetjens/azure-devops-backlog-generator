"""Tests for the Version 1.0 Description Mapping contract."""

from pathlib import Path

import pytest
from markdown_it import MarkdownIt

from azure_devops_backlog_generator.documentation.description import prepare_description
from azure_devops_backlog_generator.documentation.exceptions import DocumentationValidationError
from azure_devops_backlog_generator.documentation.models import WorkItemType
from azure_devops_backlog_generator.documentation.processor import DocumentationProcessor


def _item(tmp_path: Path, content: str):
    (tmp_path / "input.md").write_text(content, encoding="utf-8")
    return DocumentationProcessor().process(tmp_path).documents[0].root_items[0]


@pytest.mark.parametrize(
    ("body", "expected"),
    [
        ("One paragraph.\n", "<p>One paragraph.</p>\n"),
        ("First.\n\nSecond.\n", "<p>First.</p>\n<p>Second.</p>\n"),
        ("Caf\u00e9 \u2014 \u58f0\n", "<p>Caf\u00e9 \u2014 \u58f0</p>\n"),
        (
            "*em* **strong** `code` \\* &amp;\n",
            "<p><em>em</em> <strong>strong</strong> <code>code</code> * &amp;</p>\n",
        ),
    ],
)
def test_prepares_exact_basic_and_inline_description_html(
    body: str, expected: str, tmp_path: Path
) -> None:
    assert _item(tmp_path, f"# Epic\n{body}").description_html == expected


@pytest.mark.parametrize(
    ("body", "expected"),
    [
        ("- One\n- Two\n", "<ul>\n<li>One</li>\n<li>Two</li>\n</ul>\n"),
        ("1. One\n2. Two\n", "<ol>\n<li>One</li>\n<li>Two</li>\n</ol>\n"),
        ("- One\n  - Nested\n", "<ul>\n<li>One\n<ul>\n<li>Nested</li>\n</ul>\n</li>\n</ul>\n"),
        ("> Quote\n", "<blockquote>\n<p>Quote</p>\n</blockquote>\n"),
        (
            "```python\nprint('x')\n```\n",
            "<pre><code class=\"language-python\">print('x')\n</code></pre>\n",
        ),
        ("    indented\n", "<pre><code>indented\n</code></pre>\n"),
    ],
)
def test_renders_supported_block_content(body: str, expected: str, tmp_path: Path) -> None:
    assert _item(tmp_path, f"# Epic\n{body}").description_html == expected


def test_renders_valid_http_https_and_autolinks(tmp_path: Path) -> None:
    item = _item(
        tmp_path,
        "# Epic\n[HTTP](http://example.test:8443/a?b=c#d) [HTTPS](https://example.test) "
        "<https://example.test/path>\n",
    )

    assert item.description_html == (
        '<p><a href="http://example.test:8443/a?b=c#d">HTTP</a> '
        '<a href="https://example.test">HTTPS</a> '
        '<a href="https://example.test/path">https://example.test/path</a></p>\n'
    )


@pytest.mark.parametrize(
    ("destination", "expected"),
    [
        ("https://example.test/a(b)", "https://example.test/a(b)"),
        ("https://example.test/a(b(c))", "https://example.test/a(b(c))"),
        (r"https://example.test/a\(b\)", "https://example.test/a(b)"),
        (r"https://example.test/a\(b\(c\)\)", "https://example.test/a(b(c))"),
        ("<https://example.test/a(b)>", "https://example.test/a(b)"),
    ],
)
def test_renders_inline_destinations_with_balanced_parentheses(
    destination: str, expected: str, tmp_path: Path
) -> None:
    item = _item(tmp_path, f"# Epic\n[x]({destination})\n")

    assert item.description_html == f'<p><a href="{expected}">x</a></p>\n'


def test_renders_inline_destination_with_escaped_ascii_punctuation(tmp_path: Path) -> None:
    item = _item(tmp_path, "# Epic\n[x](https://example.test/a\\[b\\])\n")

    assert item.description_html == '<p><a href="https://example.test/a%5Bb%5D">x</a></p>\n'


@pytest.mark.parametrize(
    "destination",
    [
        "https://\u00e9xample.test/a(b)",
        "https://\u00e9xample.test/a(b(c))",
        "https://\u00e9xample.test/a\\(b\\)",
    ],
)
def test_rejects_raw_unicode_inline_destinations_with_balanced_parentheses(
    destination: str, tmp_path: Path
) -> None:
    with pytest.raises(DocumentationValidationError, match="Invalid Description link"):
        _item(tmp_path, f"# Epic\n[x]({destination})\n")


@pytest.mark.parametrize(
    "body",
    [
        "[relative](guide.md)\n",
        "[mailto](mailto:person@example.test)\n",
        "[hostless](https:///guide)\n",
        "[bad-port](https://example.test:not-a-port/guide)\n",
        "[bad-percent](https://example.test/%zz)\n",
        "[unicode](https://\u00e9xample.test/path)\n",
    ],
)
def test_rejects_invalid_description_link_destinations(body: str, tmp_path: Path) -> None:
    with pytest.raises(DocumentationValidationError, match="Invalid Description link"):
        _item(tmp_path, f"# Epic\n{body}")


@pytest.mark.parametrize("reference", ["[x][id]", "[id][]", "[id]"])
def test_rejects_raw_unicode_reference_link_destinations(
    reference: str, tmp_path: Path
) -> None:
    with pytest.raises(DocumentationValidationError, match="Invalid Description link"):
        _item(tmp_path, f"# Epic\n{reference}\n\n[id]: https://\u00e9xample.test/path\n")


def test_renders_valid_ascii_reference_link(tmp_path: Path) -> None:
    item = _item(tmp_path, "# Epic\n[x][id]\n\n[id]: https://example.test/path\n")

    assert item.description_html == '<p><a href="https://example.test/path">x</a></p>\n'


def test_renders_valid_ascii_reference_link_with_escaped_punctuation(tmp_path: Path) -> None:
    item = _item(tmp_path, "# Epic\n[x][id]\n\n[id]: https://example.test/a\\(b\\)\n")

    assert item.description_html == '<p><a href="https://example.test/a(b)">x</a></p>\n'


def test_rejects_invalid_parsed_reference_destination(tmp_path: Path) -> None:
    with pytest.raises(DocumentationValidationError, match="Invalid Description link"):
        _item(tmp_path, "# Epic\n[x][id]\n\n[id]: https://example.test/%zz\n")


def test_ignores_unused_raw_unicode_reference_definition(tmp_path: Path) -> None:
    item = _item(tmp_path, "# Epic\nDescription\n\n[id]: https://\u00e9xample.test/path\n")

    assert item.description_html == "<p>Description</p>\n"


def test_link_looking_code_with_escaped_destination_syntax_remains_valid(tmp_path: Path) -> None:
    inline = _item(tmp_path, "# Epic\n`[not a link](https://example.test/a\\(b\\))`\n")
    fenced = _item(
        tmp_path,
        "# Epic\n```text\n[not a link](https://example.test/a\\(b\\))\n```\n",
    )
    indented = _item(
        tmp_path,
        "# Epic\n    [not a link](https://example.test/a\\(b\\))\n",
    )

    assert inline.description_html == "<p><code>[not a link](https://example.test/a\\(b\\))</code></p>\n"
    assert fenced.description_html == (
        "<pre><code class=\"language-text\">[not a link](https://example.test/a\\(b\\))\n"
        "</code></pre>\n"
    )
    assert indented.description_html == (
        "<pre><code>[not a link](https://example.test/a\\(b\\))\n</code></pre>\n"
    )


@pytest.mark.parametrize("body", ["Text <em>HTML</em>\n", "<div>HTML</div>\n", "![Alt](https://example.test/image.png)\n"])
def test_rejects_html_and_images(body: str, tmp_path: Path) -> None:
    with pytest.raises(DocumentationValidationError):
        _item(tmp_path, f"# Epic\n{body}")


def test_excludes_child_and_sibling_content_from_description(tmp_path: Path) -> None:
    epic = _item(
        tmp_path,
        "# Epic\nEpic body\n## Feature\nFeature body\n## Sibling\nSibling body\n",
    )

    assert epic.description_html == "<p>Epic body</p>\n"
    assert [child.description_html for child in epic.children] == [
        "<p>Feature body</p>\n",
        "<p>Sibling body</p>\n",
    ]


def test_full_hierarchy_prepares_each_supported_type(tmp_path: Path) -> None:
    epic = _item(
        tmp_path,
        "# Epic\nEpic\n## Feature\nFeature\n### PBI\nPBI\n#### Task\nTask\n",
    )
    feature = epic.children[0]
    pbi = feature.children[0]
    task = pbi.children[0]

    assert [item.work_item_type for item in (epic, feature, pbi, task)] == list(WorkItemType)
    assert [item.description_html for item in (epic, feature, pbi, task)] == [
        "<p>Epic</p>\n",
        "<p>Feature</p>\n",
        "<p>PBI</p>\n",
        "<p>Task</p>\n",
    ]


def test_excludes_tags_and_acceptance_criteria_regions(tmp_path: Path) -> None:
    item = _item(
        tmp_path,
        "# Epic\nDescription\n\nTags:\n\n- ignored\n\nAcceptance Criteria:\n\n- ignored\n",
    )

    assert item.description_html == "<p>Description</p>\n"


@pytest.mark.parametrize(
    ("body", "message"),
    [
        ("Description\n\nAcceptance Criteria:\n\n- A\n\nTags:\n\n- T\n", "must precede"),
        ("Description\n\nTags:\n\n- A\n\nTags:\n\n- B\n", "Duplicate Tags"),
        (
            "Description\n\nAcceptance Criteria:\n\n- A\n\nAcceptance Criteria:\n\n- B\n",
            "Duplicate Acceptance",
        ),
    ],
)
def test_rejects_non_deterministic_reserved_markers(
    body: str, message: str, tmp_path: Path
) -> None:
    with pytest.raises(DocumentationValidationError, match=message):
        _item(tmp_path, f"# Epic\n{body}")


@pytest.mark.parametrize("body", ["> Tags:\n", "- Tags:\n", "```text\nTags:\n```\n"])
def test_marker_looking_container_content_remains_description(body: str, tmp_path: Path) -> None:
    assert _item(tmp_path, f"# Epic\n{body}").description_html


def test_marker_looking_indented_code_remains_description(tmp_path: Path) -> None:
    item = _item(tmp_path, "# Epic\n    Tags:\n    Acceptance Criteria:\n")

    assert item.description_html == "<pre><code>Tags:\nAcceptance Criteria:\n</code></pre>\n"


def test_marker_looking_html_block_is_not_reserved(tmp_path: Path) -> None:
    with pytest.raises(DocumentationValidationError, match="Raw HTML"):
        _item(tmp_path, "# Epic\n<div>\nTags:\nAcceptance Criteria:\n</div>\n")


@pytest.mark.parametrize(
    "content", ["# Epic\n", "# Epic\n\nTags:\n\n- tag\n", "# Epic\n   \n\t\n"]
)
def test_rejects_missing_or_whitespace_only_description(content: str, tmp_path: Path) -> None:
    with pytest.raises(DocumentationValidationError, match="Description"):
        _item(tmp_path, content)


def test_rejects_acceptance_criteria_marker_on_task(tmp_path: Path) -> None:
    with pytest.raises(DocumentationValidationError, match="not permitted for Task"):
        _item(
            tmp_path,
            "# Epic\nEpic\n## Feature\nFeature\n### PBI\nPBI\n#### Task\nTask\n\n"
            "Acceptance Criteria:\n\n- Criterion\n",
        )


def test_reports_renderer_failure_as_validation_error(monkeypatch: pytest.MonkeyPatch) -> None:
    parser = MarkdownIt("commonmark")
    tokens = parser.parse("Body\n")

    def fail(*args: object, **kwargs: object) -> str:
        raise RuntimeError("renderer unavailable")

    monkeypatch.setattr(parser.renderer, "render", fail)
    with pytest.raises(DocumentationValidationError, match="rendering failed"):
        prepare_description(
            parser=parser,
            tokens=tokens,
            start=0,
            end=len(tokens),
            work_item_type=WorkItemType.EPIC,
            relative_path="input.md",
            source="Body\n",
        )


def test_rejects_empty_rendered_description(monkeypatch: pytest.MonkeyPatch) -> None:
    parser = MarkdownIt("commonmark")
    tokens = parser.parse("Body\n")
    monkeypatch.setattr(parser.renderer, "render", lambda *args: "")

    with pytest.raises(DocumentationValidationError, match="Empty rendered Description"):
        prepare_description(
            parser=parser,
            tokens=tokens,
            start=0,
            end=len(tokens),
            work_item_type=WorkItemType.EPIC,
            relative_path="input.md",
            source="Body\n",
        )
