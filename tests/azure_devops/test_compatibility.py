"""Tests for pure structural Scrum compatibility evaluation."""

from __future__ import annotations

from copy import deepcopy

import pytest

from azure_devops_backlog_generator.azure_devops.compatibility import (
    StructuralCompatibilityEvidence,
    evaluate_structural_scrum_compatibility,
)
from azure_devops_backlog_generator.azure_devops.exceptions import (
    AzureDevOpsCompatibilityError,
)
from azure_devops_backlog_generator.documentation.models import WorkItemType

_TITLE = "System.Title"
_DESCRIPTION = "System.Description"
_ACCEPTANCE_CRITERIA = "Microsoft.VSTS.Common.AcceptanceCriteria"
_TAGS = "System.Tags"
_IDENTITY = "Custom.BacklogGeneratorSourceIdentity"

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


def _evidence() -> StructuralCompatibilityEvidence:
    fields = {
        work_item_type: {
            field_reference: {"referenceName": field_reference}
            for field_reference in field_references
        }
        for work_item_type, field_references in _REQUIRED_FIELDS.items()
    }
    for work_item_type in WorkItemType:
        fields[work_item_type][_IDENTITY].update(
            {"defaultValue": None, "alwaysRequired": False}
        )

    return StructuralCompatibilityEvidence(
        work_item_types={work_item_type: {"evidence": True} for work_item_type in WorkItemType},
        work_item_type_fields=fields,
        global_fields={
            _TITLE: {"referenceName": _TITLE},
            _DESCRIPTION: {"referenceName": _DESCRIPTION},
            _ACCEPTANCE_CRITERIA: {"referenceName": _ACCEPTANCE_CRITERIA},
            _TAGS: {"referenceName": _TAGS},
            _IDENTITY: {
                "referenceName": _IDENTITY,
                "name": "Backlog Generator Source Identity",
                "type": "String",
                "readOnly": False,
            },
        },
    )


def _copy_evidence(evidence: StructuralCompatibilityEvidence) -> StructuralCompatibilityEvidence:
    return StructuralCompatibilityEvidence(
        work_item_types=deepcopy(evidence.work_item_types),
        work_item_type_fields=deepcopy(evidence.work_item_type_fields),
        global_fields=deepcopy(evidence.global_fields),
    )


def test_accepts_complete_compatible_evidence_without_returning_persistence_authority() -> None:
    assert evaluate_structural_scrum_compatibility(_evidence()) is None


@pytest.mark.parametrize("work_item_type", list(WorkItemType))
def test_rejects_missing_required_work_item_type(work_item_type: WorkItemType) -> None:
    evidence = _copy_evidence(_evidence())
    del evidence.work_item_types[work_item_type]

    with pytest.raises(AzureDevOpsCompatibilityError, match=work_item_type.value):
        evaluate_structural_scrum_compatibility(evidence)


def test_rejects_insufficient_work_item_type_evidence() -> None:
    evidence = _copy_evidence(_evidence())
    evidence.work_item_types[WorkItemType.EPIC] = {}

    with pytest.raises(AzureDevOpsCompatibilityError, match="work-item type evidence"):
        evaluate_structural_scrum_compatibility(evidence)


@pytest.mark.parametrize("attribute", ("work_item_type_fields", "global_fields"))
def test_rejects_non_mapping_field_evidence(attribute: str) -> None:
    evidence = _evidence()
    object.__setattr__(evidence, attribute, [])

    with pytest.raises(AzureDevOpsCompatibilityError, match="must be a mapping"):
        evaluate_structural_scrum_compatibility(evidence)


@pytest.mark.parametrize(
    ("work_item_type", "field_reference"),
    [
        (work_item_type, field_reference)
        for work_item_type, fields in _REQUIRED_FIELDS.items()
        for field_reference in fields
    ],
)
def test_rejects_missing_required_type_specific_field_evidence(
    work_item_type: WorkItemType, field_reference: str
) -> None:
    evidence = _copy_evidence(_evidence())
    del evidence.work_item_type_fields[work_item_type][field_reference]

    with pytest.raises(AzureDevOpsCompatibilityError, match=field_reference):
        evaluate_structural_scrum_compatibility(evidence)


@pytest.mark.parametrize("field_reference", (_TITLE, _DESCRIPTION, _ACCEPTANCE_CRITERIA, _TAGS))
def test_rejects_missing_required_global_standard_field_evidence(field_reference: str) -> None:
    evidence = _copy_evidence(_evidence())
    del evidence.global_fields[field_reference]

    with pytest.raises(AzureDevOpsCompatibilityError, match=field_reference):
        evaluate_structural_scrum_compatibility(evidence)


def test_task_does_not_require_acceptance_criteria_evidence() -> None:
    evidence = _copy_evidence(_evidence())
    assert _ACCEPTANCE_CRITERIA not in evidence.work_item_type_fields[WorkItemType.TASK]

    evaluate_structural_scrum_compatibility(evidence)


def test_rejects_mismatched_standard_field_reference_evidence() -> None:
    evidence = _copy_evidence(_evidence())
    evidence.work_item_type_fields[WorkItemType.EPIC][_TITLE]["referenceName"] = _DESCRIPTION

    with pytest.raises(AzureDevOpsCompatibilityError, match="reference name"):
        evaluate_structural_scrum_compatibility(evidence)


def test_rejects_missing_global_identity_evidence() -> None:
    evidence = _copy_evidence(_evidence())
    del evidence.global_fields[_IDENTITY]

    with pytest.raises(AzureDevOpsCompatibilityError, match="global field evidence"):
        evaluate_structural_scrum_compatibility(evidence)


@pytest.mark.parametrize(
    ("property_name", "value", "message"),
    [
        ("referenceName", "Custom.Other", "reference name"),
        ("name", "Other", "display name"),
        ("type", "PlainText", "type"),
        ("readOnly", True, "non-read-only"),
        ("isDeleted", True, "deleted"),
    ],
)
def test_rejects_incompatible_global_identity_evidence(
    property_name: str, value: object, message: str
) -> None:
    evidence = _copy_evidence(_evidence())
    evidence.global_fields[_IDENTITY][property_name] = value

    with pytest.raises(AzureDevOpsCompatibilityError, match=message):
        evaluate_structural_scrum_compatibility(evidence)


@pytest.mark.parametrize("work_item_type", list(WorkItemType))
def test_rejects_missing_identity_type_specific_evidence(work_item_type: WorkItemType) -> None:
    evidence = _copy_evidence(_evidence())
    del evidence.work_item_type_fields[work_item_type][_IDENTITY]

    with pytest.raises(AzureDevOpsCompatibilityError, match=_IDENTITY):
        evaluate_structural_scrum_compatibility(evidence)


def test_rejects_mismatched_identity_type_specific_evidence() -> None:
    evidence = _copy_evidence(_evidence())
    evidence.work_item_type_fields[WorkItemType.EPIC][_IDENTITY]["referenceName"] = "Custom.Other"

    with pytest.raises(AzureDevOpsCompatibilityError, match="reference name"):
        evaluate_structural_scrum_compatibility(evidence)


@pytest.mark.parametrize(
    ("property_name", "value", "message"),
    [
        ("defaultValue", "generated", "configured default"),
        ("alwaysRequired", True, "process-required"),
    ],
)
def test_rejects_incompatible_identity_type_specific_evidence(
    property_name: str, value: object, message: str
) -> None:
    evidence = _copy_evidence(_evidence())
    evidence.work_item_type_fields[WorkItemType.EPIC][_IDENTITY][property_name] = value

    with pytest.raises(AzureDevOpsCompatibilityError, match=message):
        evaluate_structural_scrum_compatibility(evidence)


def test_rejects_missing_identity_default_value_evidence() -> None:
    evidence = _copy_evidence(_evidence())
    del evidence.work_item_type_fields[WorkItemType.EPIC][_IDENTITY]["defaultValue"]

    with pytest.raises(AzureDevOpsCompatibilityError, match="configured default"):
        evaluate_structural_scrum_compatibility(evidence)


def test_does_not_reject_an_additional_always_required_field() -> None:
    evidence = _copy_evidence(_evidence())
    evidence.work_item_type_fields[WorkItemType.EPIC]["Custom.Additional"] = {
        "referenceName": "Custom.Additional",
        "alwaysRequired": True,
    }

    evaluate_structural_scrum_compatibility(evidence)


def test_does_not_infer_locked_identity_field_incompatibility() -> None:
    evidence = _copy_evidence(_evidence())
    evidence.global_fields[_IDENTITY]["isLocked"] = True

    evaluate_structural_scrum_compatibility(evidence)
