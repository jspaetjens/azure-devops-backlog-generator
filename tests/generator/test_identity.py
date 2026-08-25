"""Tests for Version 1.0 persisted source-identity construction."""

from __future__ import annotations

import re

import pytest

from azure_devops_backlog_generator.documentation.models import (
    HeadingIdentity,
    SemanticWorkItem,
    WorkItemType,
)
from azure_devops_backlog_generator.generator.identity import (
    build_source_identity_marker,
    calculate_source_identity_digest,
    frame_source_identity,
)

_MARKER_PATTERN = re.compile(r"adbg:source-id:v1:sha256:[0-9a-f]{64}\Z")


@pytest.mark.parametrize(
    ("path", "hierarchy", "framed_hex", "digest", "marker"),
    [
        (
            "file-a.md",
            (HeadingIdentity(1, "Platform"),),
            "616462672d736f757263652d6964656e746974792d7631000000000966696c652d612e6d64000000010100000008506c6174666f726d",
            "fc590bceef6c25da9e47138a34883f99eadf0e52201fe04fb700a20edc14acaf",
            "adbg:source-id:v1:sha256:fc590bceef6c25da9e47138a34883f99eadf0e52201fe04fb700a20edc14acaf",
        ),
        (
            "file-a.md",
            (HeadingIdentity(1, "Platform"), HeadingIdentity(2, "API")),
            "616462672d736f757263652d6964656e746974792d7631000000000966696c652d612e6d64000000020100000008506c6174666f726d0200000003415049",
            "2dd6a0940a9677d61a11c4726af7f0ab39814419cfb9bcdda8c28cfe91751d63",
            "adbg:source-id:v1:sha256:2dd6a0940a9677d61a11c4726af7f0ab39814419cfb9bcdda8c28cfe91751d63",
        ),
        (
            "caf\u00e9.md",
            (HeadingIdentity(1, "Cr\u00e8me"),),
            "616462672d736f757263652d6964656e746974792d76310000000008636166c3a92e6d640000000101000000064372c3a86d65",
            "d5e7aab193d51ff379aee0fc4c1fdbe4260801e2e8600dbd67d2b21bc95df7bc",
            "adbg:source-id:v1:sha256:d5e7aab193d51ff379aee0fc4c1fdbe4260801e2e8600dbd67d2b21bc95df7bc",
        ),
    ],
)
def test_documented_source_identity_vectors(
    path: str,
    hierarchy: tuple[HeadingIdentity, ...],
    framed_hex: str,
    digest: str,
    marker: str,
) -> None:
    assert frame_source_identity(path, hierarchy) == bytes.fromhex(framed_hex)
    assert calculate_source_identity_digest(path, hierarchy) == digest
    assert build_source_identity_marker(path, hierarchy) == marker


def test_non_ascii_vector_uses_utf8_byte_lengths_and_exact_bytes() -> None:
    path = "caf\u00e9.md"
    title = "Cr\u00e8me"
    framed = frame_source_identity(path, (HeadingIdentity(1, title),))

    assert path.encode("utf-8") == bytes.fromhex("63 61 66 c3 a9 2e 6d 64")
    assert title.encode("utf-8") == bytes.fromhex("43 72 c3 a8 6d 65")
    assert len(path.encode("utf-8")) == 8
    assert len(path) == 7
    assert len(title.encode("utf-8")) == 6
    assert len(title) == 5
    assert framed == bytes.fromhex(
        "61 64 62 67 2d 73 6f 75 72 63 65 2d 69 64 65 6e 74 69 74 79 2d 76 31 "
        "00 00 00 00 08 63 61 66 c3 a9 2e 6d 64 00 00 00 01 01 00 00 00 06 "
        "43 72 c3 a8 6d 65"
    )


def test_repeated_invocation_is_deterministic_for_a_full_hierarchy() -> None:
    hierarchy = tuple(HeadingIdentity(level, f"Level {level}") for level in range(1, 5))

    assert frame_source_identity("input.md", hierarchy) == frame_source_identity(
        "input.md", hierarchy
    )
    assert calculate_source_identity_digest(
        "input.md", hierarchy
    ) == calculate_source_identity_digest("input.md", hierarchy)
    assert build_source_identity_marker("input.md", hierarchy) == build_source_identity_marker(
        "input.md", hierarchy
    )


@pytest.mark.parametrize(
    ("path", "hierarchy"),
    [
        ("other.md", (HeadingIdentity(1, "Platform"),)),
        ("FILE-A.md", (HeadingIdentity(1, "Platform"),)),
        ("file-a.md", (HeadingIdentity(1, "platform"),)),
        ("file-a.md", (HeadingIdentity(1, "Platform"), HeadingIdentity(2, "Api"))),
        ("file-a.md", (HeadingIdentity(1, "Product"), HeadingIdentity(2, "API"))),
        ("file-a.md", (HeadingIdentity(2, "Platform"),)),
        ("file-a.md", (HeadingIdentity(1, "Other"), HeadingIdentity(2, "API"))),
    ],
)
def test_identity_significant_input_changes_change_the_marker(
    path: str, hierarchy: tuple[HeadingIdentity, ...]
) -> None:
    baseline = build_source_identity_marker("file-a.md", (HeadingIdentity(1, "Platform"),))

    assert build_source_identity_marker(path, hierarchy) != baseline


def test_same_visible_title_under_different_parents_changes_the_marker() -> None:
    first = (HeadingIdentity(1, "Platform"), HeadingIdentity(2, "API"))
    second = (HeadingIdentity(1, "Product"), HeadingIdentity(2, "API"))

    assert build_source_identity_marker("input.md", first) != build_source_identity_marker(
        "input.md", second
    )


def _item(
    *,
    description_html: str = "<p>Description</p>\n",
    acceptance_criteria_html: str | None = "<ul>\n<li>Criterion</li>\n</ul>\n",
    tags_value: str | None = "platform",
    source_order: int = 0,
) -> SemanticWorkItem:
    return SemanticWorkItem(
        work_item_type=WorkItemType.EPIC,
        level=1,
        title="Platform",
        canonical_relative_path="input.md",
        heading_hierarchy=(HeadingIdentity(1, "Platform"),),
        source_order=source_order,
        description_html=description_html,
        acceptance_criteria_html=acceptance_criteria_html,
        tags_value=tags_value,
        direct_body_token_spans=(),
        children=(),
    )


@pytest.mark.parametrize(
    "changed_item",
    [
        _item(description_html="<p>Changed Description</p>\n"),
        _item(acceptance_criteria_html="<ul>\n<li>Changed criterion</li>\n</ul>\n"),
        _item(tags_value="changed"),
        _item(source_order=99),
    ],
)
def test_business_values_and_source_order_are_not_identity_inputs(
    changed_item: SemanticWorkItem,
) -> None:
    original = _item()

    assert build_source_identity_marker(
        original.canonical_relative_path, original.heading_hierarchy
    ) == build_source_identity_marker(
        changed_item.canonical_relative_path, changed_item.heading_hierarchy
    )


def test_marker_is_lowercase_and_has_the_exact_versioned_syntax() -> None:
    marker = build_source_identity_marker("input.md", (HeadingIdentity(1, "Platform"),))

    assert _MARKER_PATTERN.fullmatch(marker)
    assert marker == marker.lower()


def test_framing_does_not_apply_host_path_or_unicode_normalisation() -> None:
    hierarchy = (HeadingIdentity(1, "Cafe\u0301"),)

    assert frame_source_identity("folder\\input.md", hierarchy) != frame_source_identity(
        "folder/input.md", hierarchy
    )
    assert frame_source_identity("cafe\u0301.md", hierarchy) != frame_source_identity(
        "caf\u00e9.md", (HeadingIdentity(1, "Caf\u00e9"),)
    )


@pytest.mark.parametrize("level", [0, 5, 256])
def test_rejects_heading_levels_outside_the_approved_representation(level: int) -> None:
    with pytest.raises(ValueError, match="H1 through H4"):
        frame_source_identity("input.md", (HeadingIdentity(level, "Title"),))
