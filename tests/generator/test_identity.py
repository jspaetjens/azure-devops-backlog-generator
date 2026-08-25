"""Tests for Version 1.0 persisted source-identity construction."""

from __future__ import annotations

import re
from dataclasses import replace

import pytest

import azure_devops_backlog_generator.generator.identity as identity_module
from azure_devops_backlog_generator.documentation.models import (
    DocumentationHierarchy,
    HeadingIdentity,
    ParsedDocument,
    SemanticWorkItem,
    WorkItemType,
)
from azure_devops_backlog_generator.generator.identity import (
    SourceIdentityValidationError,
    SourceIdentityValidationState,
    build_source_identity_marker,
    calculate_source_identity_digest,
    frame_source_identity,
    validate_source_identity_collisions,
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


def _source_item(
    *,
    path: str = "input.md",
    hierarchy: tuple[HeadingIdentity, ...] = (HeadingIdentity(1, "Platform"),),
    source_order: int = 0,
    children: tuple[SemanticWorkItem, ...] = (),
    description_html: str = "<p>Description</p>\n",
    acceptance_criteria_html: str | None = "<ul>\n<li>Criterion</li>\n</ul>\n",
    tags_value: str | None = "platform",
) -> SemanticWorkItem:
    return replace(
        _item(
            source_order=source_order,
            description_html=description_html,
            acceptance_criteria_html=acceptance_criteria_html,
            tags_value=tags_value,
        ),
        work_item_type=WorkItemType(
            ("Epic", "Feature", "Product Backlog Item", "Task")[len(hierarchy) - 1]
        ),
        level=hierarchy[-1].level,
        title=hierarchy[-1].title,
        canonical_relative_path=path,
        heading_hierarchy=hierarchy,
        children=children,
    )


def _document(path: str, *root_items: SemanticWorkItem) -> ParsedDocument:
    return ParsedDocument(canonical_relative_path=path, tokens=(), root_items=root_items)


def _hierarchy(*documents: ParsedDocument) -> DocumentationHierarchy:
    return DocumentationHierarchy(documents=documents)


def test_run_level_validation_succeeds_for_empty_and_single_item_hierarchies() -> None:
    assert validate_source_identity_collisions(_hierarchy()) is None
    assert validate_source_identity_collisions(
        _hierarchy(_document("input.md", _source_item()))
    ) is None


@pytest.mark.parametrize(
    "items",
    [
        (
            _source_item(path="first.md", hierarchy=(HeadingIdentity(1, "Platform"),)),
            _source_item(
                path="second.md", hierarchy=(HeadingIdentity(1, "Platform"),), source_order=1
            ),
        ),
        (
            _source_item(
                hierarchy=(HeadingIdentity(1, "Platform"), HeadingIdentity(2, "API"))
            ),
            _source_item(
                hierarchy=(HeadingIdentity(1, "Product"), HeadingIdentity(2, "API")),
                source_order=1,
            ),
        ),
        (
            _source_item(path="Input.md"),
            _source_item(path="input.md", source_order=1),
        ),
        (
            _source_item(hierarchy=(HeadingIdentity(1, "Platform"),)),
            _source_item(hierarchy=(HeadingIdentity(1, "platform"),), source_order=1),
        ),
        (
            _source_item(path="caf\u00e9.md", hierarchy=(HeadingIdentity(1, "Cr\u00e8me"),)),
            _source_item(path="cafe.md", hierarchy=(HeadingIdentity(1, "Creme"),), source_order=1),
        ),
    ],
)
def test_run_level_validation_accepts_distinct_logical_identities(
    items: tuple[SemanticWorkItem, SemanticWorkItem],
) -> None:
    hierarchy = _hierarchy(_document("input.md", *items))

    assert validate_source_identity_collisions(hierarchy) is None


@pytest.mark.parametrize(
    "changed_item",
    [
        _source_item(description_html="<p>Changed Description</p>\n"),
        _source_item(acceptance_criteria_html="<ul>\n<li>Changed</li>\n</ul>\n"),
        _source_item(tags_value="changed"),
        _source_item(source_order=99),
    ],
)
def test_duplicate_logical_identity_ignores_business_values_and_source_order(
    changed_item: SemanticWorkItem,
) -> None:
    hierarchy = _hierarchy(_document("input.md", _source_item(), changed_item))

    with pytest.raises(SourceIdentityValidationError) as error:
        validate_source_identity_collisions(hierarchy)

    assert error.value.state is SourceIdentityValidationState.DUPLICATE_LOGICAL_IDENTITY
    assert error.value.marker is None


def test_duplicate_logical_identity_takes_precedence_over_marker_collision(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    marker = "adbg:source-id:v1:sha256:" + "0" * 64
    monkeypatch.setattr(identity_module, "build_source_identity_marker", lambda *_: marker)
    hierarchy = _hierarchy(_document("input.md", _source_item(), _source_item(source_order=1)))

    with pytest.raises(SourceIdentityValidationError) as error:
        validate_source_identity_collisions(hierarchy)

    assert error.value.state is SourceIdentityValidationState.DUPLICATE_LOGICAL_IDENTITY


def test_distinct_logical_identities_with_one_complete_marker_fail(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    marker = "adbg:source-id:v1:sha256:" + "f" * 64
    monkeypatch.setattr(identity_module, "build_source_identity_marker", lambda *_: marker)
    hierarchy = _hierarchy(
        _document(
            "input.md",
            _source_item(),
            _source_item(path="other.md", source_order=1),
        )
    )

    with pytest.raises(SourceIdentityValidationError) as error:
        validate_source_identity_collisions(hierarchy)

    assert error.value.state is SourceIdentityValidationState.PERSISTED_MARKER_COLLISION
    assert error.value.marker == marker


def test_complete_marker_not_digest_alone_controls_collision_grouping(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    markers = iter(
        [
            "adbg:source-id:v1:sha256:" + "a" * 64,
            "adbg:source-id:v2:sha256:" + "a" * 64,
        ]
    )
    monkeypatch.setattr(identity_module, "build_source_identity_marker", lambda *_: next(markers))
    hierarchy = _hierarchy(
        _document("input.md", _source_item(), _source_item(path="other.md", source_order=1))
    )

    assert validate_source_identity_collisions(hierarchy) is None


def test_run_level_validation_traverses_roots_descendants_and_multiple_documents(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    observed: list[tuple[str, tuple[HeadingIdentity, ...]]] = []
    original = identity_module.build_source_identity_marker

    def record_marker(path: str, headings: tuple[HeadingIdentity, ...]) -> str:
        observed.append((path, headings))
        return original(path, headings)

    monkeypatch.setattr(identity_module, "build_source_identity_marker", record_marker)
    task = _source_item(
        hierarchy=(
            HeadingIdentity(1, "Epic"),
            HeadingIdentity(2, "Feature"),
            HeadingIdentity(3, "PBI"),
            HeadingIdentity(4, "Task"),
        ),
        source_order=3,
    )
    pbi = _source_item(
        hierarchy=(
            HeadingIdentity(1, "Epic"),
            HeadingIdentity(2, "Feature"),
            HeadingIdentity(3, "PBI"),
        ),
        source_order=2,
        children=(task,),
    )
    feature = _source_item(
        hierarchy=(HeadingIdentity(1, "Epic"), HeadingIdentity(2, "Feature")),
        source_order=1,
        children=(pbi,),
    )
    epic = _source_item(hierarchy=(HeadingIdentity(1, "Epic"),), children=(feature,))
    second_epic = _source_item(path="second.md", hierarchy=(HeadingIdentity(1, "Second"),))

    assert validate_source_identity_collisions(
        _hierarchy(_document("input.md", epic), _document("second.md", second_epic))
    ) is None
    assert observed == [
        ("input.md", epic.heading_hierarchy),
        ("input.md", feature.heading_hierarchy),
        ("input.md", pbi.heading_hierarchy),
        ("input.md", task.heading_hierarchy),
        ("second.md", second_epic.heading_hierarchy),
    ]


def test_duplicate_failure_is_the_first_condition_in_document_source_order(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    observed: list[str] = []

    def record_marker(path: str, _: tuple[HeadingIdentity, ...]) -> str:
        observed.append(path)
        return "adbg:source-id:v1:sha256:" + path[0] * 64

    monkeypatch.setattr(identity_module, "build_source_identity_marker", record_marker)
    first = _source_item(path="alpha.md")
    duplicate = _source_item(path="alpha.md")
    collision = _source_item(path="beta.md")
    hierarchy = _hierarchy(
        _document("first.md", first),
        _document("second.md", duplicate, collision),
    )

    with pytest.raises(SourceIdentityValidationError) as error:
        validate_source_identity_collisions(hierarchy)

    assert error.value.state is SourceIdentityValidationState.DUPLICATE_LOGICAL_IDENTITY
    assert observed == ["alpha.md"]


def test_marker_collision_is_the_first_condition_in_document_source_order(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    marker = "adbg:source-id:v1:sha256:" + "c" * 64
    calls: list[str] = []

    def colliding_marker(path: str, _: tuple[HeadingIdentity, ...]) -> str:
        calls.append(path)
        return marker

    monkeypatch.setattr(identity_module, "build_source_identity_marker", colliding_marker)
    hierarchy = _hierarchy(
        _document("first.md", _source_item(path="alpha.md")),
        _document("second.md", _source_item(path="beta.md")),
        _document("third.md", _source_item(path="gamma.md")),
    )

    with pytest.raises(SourceIdentityValidationError) as error:
        validate_source_identity_collisions(hierarchy)

    assert error.value.state is SourceIdentityValidationState.PERSISTED_MARKER_COLLISION
    assert calls == ["alpha.md", "beta.md"]


def test_validation_is_generator_owned_and_does_not_mutate_the_hierarchy() -> None:
    hierarchy = _hierarchy(_document("input.md", _source_item()))
    original = hierarchy

    assert validate_source_identity_collisions(hierarchy) is None
    assert hierarchy == original
    assert SourceIdentityValidationError.__module__ == (
        "azure_devops_backlog_generator.generator.identity"
    )
