"""Pure structural Scrum compatibility evaluation for Azure DevOps metadata."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from azure_devops_backlog_generator.azure_devops.exceptions import (
    AzureDevOpsCompatibilityError,
)
from azure_devops_backlog_generator.documentation.models import WorkItemType

_TITLE = "System.Title"
_DESCRIPTION = "System.Description"
_ACCEPTANCE_CRITERIA = "Microsoft.VSTS.Common.AcceptanceCriteria"
_TAGS = "System.Tags"
_IDENTITY = "Custom.BacklogGeneratorSourceIdentity"
_IDENTITY_NAME = "Backlog Generator Source Identity"
_IDENTITY_TYPE = "String"

_REQUIRED_FIELDS = {
    WorkItemType.EPIC: (_TITLE, _DESCRIPTION, _ACCEPTANCE_CRITERIA, _TAGS, _IDENTITY),
    WorkItemType.FEATURE: (_TITLE, _DESCRIPTION, _ACCEPTANCE_CRITERIA, _TAGS, _IDENTITY),
    WorkItemType.PRODUCT_BACKLOG_ITEM: (
        _TITLE,
        _DESCRIPTION,
        _ACCEPTANCE_CRITERIA,
        _TAGS,
        _IDENTITY,
    ),
    WorkItemType.TASK: (_TITLE, _DESCRIPTION, _TAGS, _IDENTITY),
}


@dataclass(frozen=True, slots=True)
class StructuralCompatibilityEvidence:
    """Retrieved metadata required to assess the fixed Version 1.0 contract."""

    work_item_types: Mapping[WorkItemType, Mapping[str, Any]]
    work_item_type_fields: Mapping[WorkItemType, Mapping[str, Mapping[str, Any]]]
    global_fields: Mapping[str, Mapping[str, Any]]


def evaluate_structural_scrum_compatibility(
    evidence: StructuralCompatibilityEvidence,
) -> None:
    """Raise a controlled error unless metadata proves structural compatibility.

    A successful return only establishes the documented metadata-level contract.
    It does not establish that Azure DevOps will accept a candidate Create request.
    """
    if not isinstance(evidence, StructuralCompatibilityEvidence):
        raise TypeError("StructuralCompatibilityEvidence is required.")

    _validate_work_item_types(evidence.work_item_types)
    if not isinstance(evidence.work_item_type_fields, Mapping):
        _fail("Work-item type field evidence must be a mapping.")
    if not isinstance(evidence.global_fields, Mapping):
        _fail("Global field evidence must be a mapping.")
    for work_item_type, fields in _REQUIRED_FIELDS.items():
        for field_reference in fields:
            _validate_type_specific_field(evidence, work_item_type, field_reference)
            _validate_global_field(evidence, field_reference)

    _validate_identity_global_field(evidence.global_fields[_IDENTITY])
    for work_item_type in WorkItemType:
        _validate_identity_type_field(evidence, work_item_type)


def _validate_work_item_types(
    work_item_types: Mapping[WorkItemType, Mapping[str, Any]],
) -> None:
    if not isinstance(work_item_types, Mapping):
        _fail("Work-item type evidence must be a mapping.")

    for work_item_type in WorkItemType:
        metadata = work_item_types.get(work_item_type)
        if not isinstance(metadata, Mapping) or not metadata:
            _fail(f"Missing or insufficient work-item type evidence for {work_item_type.value!r}.")


def _validate_type_specific_field(
    evidence: StructuralCompatibilityEvidence,
    work_item_type: WorkItemType,
    field_reference: str,
) -> None:
    fields = evidence.work_item_type_fields.get(work_item_type)
    metadata = fields.get(field_reference) if isinstance(fields, Mapping) else None
    if not isinstance(metadata, Mapping):
        _fail(
            "Missing type-specific field evidence for "
            f"{field_reference!r} on {work_item_type.value!r}."
        )
    if metadata.get("referenceName") != field_reference:
        _fail(
            "Type-specific field evidence has an incompatible reference name for "
            f"{field_reference!r} on {work_item_type.value!r}."
        )


def _validate_global_field(
    evidence: StructuralCompatibilityEvidence, field_reference: str
) -> None:
    metadata = evidence.global_fields.get(field_reference)
    if not isinstance(metadata, Mapping):
        _fail(f"Missing global field evidence for {field_reference!r}.")
    if metadata.get("referenceName") != field_reference:
        _fail(f"Global field evidence has an incompatible reference name for {field_reference!r}.")


def _validate_identity_global_field(metadata: Mapping[str, Any]) -> None:
    if metadata.get("name") != _IDENTITY_NAME:
        _fail("Identity field display name is incompatible.")
    if metadata.get("type") != _IDENTITY_TYPE:
        _fail("Identity field type is incompatible.")
    if metadata.get("readOnly") is not False:
        _fail("Identity field must be evidenced as non-read-only.")
    if metadata.get("isDeleted") is True:
        _fail("Identity field is deleted.")


def _validate_identity_type_field(
    evidence: StructuralCompatibilityEvidence, work_item_type: WorkItemType
) -> None:
    metadata = evidence.work_item_type_fields[work_item_type][_IDENTITY]
    if "defaultValue" not in metadata or metadata["defaultValue"] is not None:
        _fail(f"Identity field has a configured default for {work_item_type.value!r}.")
    if metadata.get("alwaysRequired") is not False:
        _fail(f"Identity field is process-required for {work_item_type.value!r}.")


def _fail(message: str) -> None:
    raise AzureDevOpsCompatibilityError(message)
