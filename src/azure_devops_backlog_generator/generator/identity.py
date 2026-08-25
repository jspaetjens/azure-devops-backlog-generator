"""Version 1.0 persisted source-identity framing and marker construction."""

from __future__ import annotations

import hashlib

from azure_devops_backlog_generator.documentation.models import HeadingIdentity

_DOMAIN_PREFIX = b"adbg-source-identity-v1"
_MARKER_PREFIX = "adbg:source-id:v1:sha256:"
_MAX_UINT32 = (1 << 32) - 1


def frame_source_identity(
    canonical_relative_path: str,
    heading_hierarchy: tuple[HeadingIdentity, ...],
) -> bytes:
    """Return the exact Version 1.0 binary framing for logical source identity."""
    path_bytes = canonical_relative_path.encode("utf-8")
    _require_uint32(len(path_bytes), "Canonical relative path byte length")
    _require_uint32(len(heading_hierarchy), "Heading hierarchy component count")

    framed = bytearray(_DOMAIN_PREFIX)
    framed.append(0)
    framed.extend(len(path_bytes).to_bytes(4, "big"))
    framed.extend(path_bytes)
    framed.extend(len(heading_hierarchy).to_bytes(4, "big"))
    for heading in heading_hierarchy:
        if heading.level not in {1, 2, 3, 4}:
            raise ValueError("Semantic heading level must be in the range H1 through H4.")
        title_bytes = heading.title.encode("utf-8")
        _require_uint32(len(title_bytes), "Semantic heading title byte length")
        framed.append(heading.level)
        framed.extend(len(title_bytes).to_bytes(4, "big"))
        framed.extend(title_bytes)
    return bytes(framed)


def calculate_source_identity_digest(
    canonical_relative_path: str,
    heading_hierarchy: tuple[HeadingIdentity, ...],
) -> str:
    """Return the lowercase SHA-256 digest for one logical source identity."""
    return hashlib.sha256(
        frame_source_identity(canonical_relative_path, heading_hierarchy)
    ).hexdigest()


def build_source_identity_marker(
    canonical_relative_path: str,
    heading_hierarchy: tuple[HeadingIdentity, ...],
) -> str:
    """Return the complete Version 1.0 persisted source-identity marker."""
    digest = calculate_source_identity_digest(canonical_relative_path, heading_hierarchy)
    return f"{_MARKER_PREFIX}{digest}"


def _require_uint32(value: int, name: str) -> None:
    if not 0 <= value <= _MAX_UINT32:
        raise ValueError(f"{name} must fit in an unsigned 32-bit integer.")
