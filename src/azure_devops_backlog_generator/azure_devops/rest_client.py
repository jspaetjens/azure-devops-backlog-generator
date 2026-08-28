"""Internal urllib transport foundation for Azure DevOps Services requests."""

from __future__ import annotations

import base64
import json
import re
from collections.abc import Mapping, Sequence
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode, urlsplit
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener

from azure_devops_backlog_generator.azure_devops.exceptions import (
    AzureDevOpsHttpError,
    AzureDevOpsResponseError,
    AzureDevOpsTransportError,
)
from azure_devops_backlog_generator.azure_devops.models import (
    AzureDevOpsProject,
    AzureDevOpsWorkItem,
)
from azure_devops_backlog_generator.documentation.models import WorkItemType
from azure_devops_backlog_generator.generator.candidates import WorkItemCandidate

API_VERSION = "7.1"
REQUEST_TIMEOUT_SECONDS = 30
_ACCEPT_HEADER = "application/json"
_SOURCE_IDENTITY_MARKER_PATTERN = re.compile(r"adbg:source-id:v1:sha256:[0-9a-f]{64}\Z")
_WORK_ITEM_EVIDENCE_FIELDS = (
    "System.TeamProject",
    "System.WorkItemType",
    "Custom.BacklogGeneratorSourceIdentity",
)
_COMPATIBILITY_FIELD_REFERENCES = frozenset(
    {
        "System.Title",
        "System.Description",
        "Microsoft.VSTS.Common.AcceptanceCriteria",
        "System.Tags",
        "Custom.BacklogGeneratorSourceIdentity",
    }
)


def build_work_item_create_json_patch(candidate: WorkItemCandidate) -> list[dict[str, str]]:
    """Return the approved JSON Patch body for one later Work Item Create."""
    operations = [
        {"op": "add", "path": "/fields/System.Title", "value": candidate.title},
        {
            "op": "add",
            "path": "/fields/System.Description",
            "value": candidate.description_html,
        },
    ]
    if (
        candidate.work_item_type is not WorkItemType.TASK
        and candidate.acceptance_criteria_html is not None
    ):
        operations.append(
            {
                "op": "add",
                "path": "/fields/Microsoft.VSTS.Common.AcceptanceCriteria",
                "value": candidate.acceptance_criteria_html,
            }
        )
    if candidate.tags_value is not None:
        operations.append(
            {"op": "add", "path": "/fields/System.Tags", "value": candidate.tags_value}
        )
    operations.append(
        {
            "op": "add",
            "path": "/fields/Custom.BacklogGeneratorSourceIdentity",
            "value": candidate.source_identity,
        }
    )
    return operations


class AzureDevOpsRestClient:
    """Build and send one independent Azure DevOps Services JSON request at a time."""

    def __init__(self, organization: str, project: str) -> None:
        self._organization = organization
        self._project = project

    def __repr__(self) -> str:
        """Return diagnostics that deliberately omit runtime-only credentials."""
        return (
            "AzureDevOpsRestClient("
            f"organization={self._organization!r}, project={self._project!r})"
        )

    def build_url(
        self,
        path_segments: Sequence[str],
        *,
        query: Mapping[str, str] | None = None,
        project_scoped: bool = True,
    ) -> str:
        """Build one HTTPS Azure DevOps Services URL with the fixed API version."""
        if query is not None and "api-version" in query:
            raise ValueError("The Azure DevOps API version is application controlled.")

        segments = [self._organization]
        if project_scoped:
            segments.append(self._project)
        segments.extend(path_segments)
        path = "/".join(quote(segment, safe="") for segment in segments)
        query_values = list((query or {}).items())
        query_values.append(("api-version", API_VERSION))
        url = f"https://dev.azure.com/{path}?{urlencode(query_values)}"
        if urlsplit(url).scheme != "https":
            raise ValueError("Azure DevOps requests must use HTTPS.")
        return url

    def send_json_request(
        self,
        *,
        method: str,
        path_segments: Sequence[str],
        personal_access_token: str,
        query: Mapping[str, str] | None = None,
        project_scoped: bool = True,
        json_body: Any | None = None,
        content_type: str | None = None,
    ) -> Any:
        """Send one JSON request and return its required JSON response body.

        Endpoint-specific operations remain responsible for their paths, request
        bodies and response-shape validation. This foundation accepts only the
        documented successful ``200 OK`` response status.
        """
        if type(personal_access_token) is not str or not personal_access_token.strip():
            raise ValueError("A non-empty Azure DevOps personal access token is required.")
        if json_body is not None and content_type is None:
            raise ValueError("A JSON request body requires an endpoint content type.")

        body = _serialize_json_body(json_body)
        headers = {
            "Accept": _ACCEPT_HEADER,
            "Authorization": _basic_authorization(personal_access_token),
        }
        if content_type is not None:
            headers["Content-Type"] = content_type
        request = Request(
            self.build_url(path_segments, query=query, project_scoped=project_scoped),
            data=body,
            headers=headers,
            method=method,
        )

        try:
            response = _build_opener().open(request, timeout=REQUEST_TIMEOUT_SECONDS)
        except HTTPError as error:
            _consume_and_close(error)
            raise AzureDevOpsHttpError(error.code) from error
        except (URLError, TimeoutError, OSError) as error:
            raise AzureDevOpsTransportError("Azure DevOps request transport failed.") from error

        status, response_body = _consume_response(response)
        if status != 200:
            raise AzureDevOpsHttpError(status)
        if not response_body:
            raise AzureDevOpsResponseError("Azure DevOps response body is required.")
        try:
            return json.loads(response_body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise AzureDevOpsResponseError(
                "Azure DevOps response body is not valid JSON."
            ) from error

    def retrieve_project(self, *, personal_access_token: str) -> AzureDevOpsProject:
        """Retrieve and validate the configured Azure DevOps project evidence."""
        response = self.send_json_request(
            method="GET",
            path_segments=("_apis", "projects", self._project),
            personal_access_token=personal_access_token,
            project_scoped=False,
        )
        if not isinstance(response, Mapping):
            raise AzureDevOpsResponseError(
                "Azure DevOps project response must be a JSON object."
            )

        project_id = _required_project_value(response, "id")
        project_name = _required_project_value(response, "name")
        return AzureDevOpsProject(id=project_id, name=project_name)

    def validate_work_item_create(
        self,
        candidate: WorkItemCandidate,
        *,
        personal_access_token: str,
    ) -> None:
        """Validate one candidate Create request without persisting a work item."""
        self.send_json_request(
            method="POST",
            path_segments=("_apis", "wit", "workitems", candidate.work_item_type.value),
            personal_access_token=personal_access_token,
            query={"validateOnly": "true"},
            json_body=build_work_item_create_json_patch(candidate),
            content_type="application/json-patch+json",
        )

    def create_work_item(
        self,
        candidate: WorkItemCandidate,
        *,
        personal_access_token: str,
    ) -> AzureDevOpsWorkItem:
        """Create one work item and return its validated persisted evidence."""
        response = self.send_json_request(
            method="POST",
            path_segments=("_apis", "wit", "workitems", candidate.work_item_type.value),
            personal_access_token=personal_access_token,
            json_body=build_work_item_create_json_patch(candidate),
            content_type="application/json-patch+json",
        )
        return _work_item_evidence_from_response(response)

    def lookup_work_item_ids(
        self,
        candidate: WorkItemCandidate,
        *,
        personal_access_token: str,
    ) -> tuple[int, ...]:
        """Return validated candidate IDs from the fixed source-identity WIQL lookup."""
        _validate_lookup_candidate(candidate)
        query = _build_identity_lookup_query(candidate.work_item_type, candidate.source_identity)
        response = self.send_json_request(
            method="POST",
            path_segments=("_apis", "wit", "wiql"),
            personal_access_token=personal_access_token,
            query={"$top": "2"},
            json_body={"query": query},
            content_type="application/json",
        )
        return _work_item_ids_from_wiql_response(response)

    def retrieve_work_item(
        self,
        work_item_id: int,
        *,
        personal_access_token: str,
    ) -> AzureDevOpsWorkItem:
        """Retrieve the fixed persisted evidence for one Work Item ID."""
        if type(work_item_id) is not int:
            raise ValueError("A numeric Work Item ID is required.")

        response = self.send_json_request(
            method="GET",
            path_segments=("_apis", "wit", "workitems", str(work_item_id)),
            personal_access_token=personal_access_token,
            query={"fields": ",".join(_WORK_ITEM_EVIDENCE_FIELDS)},
        )
        return _work_item_evidence_from_response(response)

    def retrieve_work_item_type(
        self,
        work_item_type: WorkItemType,
        *,
        personal_access_token: str,
    ) -> Mapping[str, Any]:
        """Retrieve metadata for one fixed Version 1.0 work-item type."""
        if not isinstance(work_item_type, WorkItemType):
            raise ValueError("A supported WorkItemType is required.")

        response = self.send_json_request(
            method="GET",
            path_segments=("_apis", "wit", "workitemtypes", work_item_type),
            personal_access_token=personal_access_token,
        )
        if not isinstance(response, Mapping):
            raise AzureDevOpsResponseError(
                "Azure DevOps work-item type response must be a JSON object."
            )
        return response

    def retrieve_work_item_type_field(
        self,
        work_item_type: WorkItemType,
        field_reference: str,
        *,
        personal_access_token: str,
    ) -> Mapping[str, Any]:
        """Retrieve metadata for one approved field on a fixed work-item type."""
        if not isinstance(work_item_type, WorkItemType):
            raise ValueError("A supported WorkItemType is required.")
        if (
            type(field_reference) is not str
            or field_reference not in _COMPATIBILITY_FIELD_REFERENCES
        ):
            raise ValueError("An approved field reference is required.")

        response = self.send_json_request(
            method="GET",
            path_segments=(
                "_apis",
                "wit",
                "workitemtypes",
                work_item_type,
                "fields",
                field_reference,
            ),
            personal_access_token=personal_access_token,
            query={"$expand": "All"},
        )
        if not isinstance(response, Mapping):
            raise AzureDevOpsResponseError(
                "Azure DevOps work-item type field response must be a JSON object."
        )
        return response

    def retrieve_field(
        self,
        field_reference: str,
        *,
        personal_access_token: str,
    ) -> Mapping[str, Any]:
        """Retrieve global metadata for one approved compatibility field."""
        if (
            type(field_reference) is not str
            or field_reference not in _COMPATIBILITY_FIELD_REFERENCES
        ):
            raise ValueError("An approved field reference is required.")

        response = self.send_json_request(
            method="GET",
            path_segments=("_apis", "wit", "fields", field_reference),
            personal_access_token=personal_access_token,
        )
        if not isinstance(response, Mapping):
            raise AzureDevOpsResponseError(
                "Azure DevOps field response must be a JSON object."
            )
        return response


class _RejectRedirectHandler(HTTPRedirectHandler):
    """Reject redirects so authenticated requests are never reissued elsewhere."""

    def redirect_request(self, *args: object, **kwargs: object) -> None:
        return None


def _build_opener():
    """Return a fresh opener with proxy discovery and redirects disabled."""
    return build_opener(ProxyHandler({}), _RejectRedirectHandler())


def _basic_authorization(personal_access_token: str) -> str:
    try:
        credential = f":{personal_access_token}".encode("ascii")
    except UnicodeEncodeError:
        raise ValueError("Azure DevOps personal access token must use ASCII characters.") from None
    return f"Basic {base64.b64encode(credential).decode('ascii')}"


def _serialize_json_body(json_body: Any | None) -> bytes | None:
    if json_body is None:
        return None
    try:
        return json.dumps(json_body, ensure_ascii=False).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise AzureDevOpsResponseError(
            "Azure DevOps request body is not JSON serializable."
        ) from error


def _required_project_value(response: Mapping[str, Any], name: str) -> str:
    value = response.get(name)
    if not isinstance(value, str) or not value.strip():
        raise AzureDevOpsResponseError(
            f"Azure DevOps project response requires a non-empty string {name!r}."
        )
    return value


def _validate_lookup_candidate(candidate: WorkItemCandidate) -> None:
    if not isinstance(candidate, WorkItemCandidate):
        raise ValueError("A WorkItemCandidate is required.")
    if not isinstance(candidate.work_item_type, WorkItemType):
        raise ValueError("A supported WorkItemType is required.")
    if (
        type(candidate.source_identity) is not str
        or not _SOURCE_IDENTITY_MARKER_PATTERN.fullmatch(candidate.source_identity)
    ):
        raise ValueError("A valid source identity marker is required.")


def _build_identity_lookup_query(work_item_type: WorkItemType, source_identity: str) -> str:
    return (
        "SELECT [System.Id]\n"
        "FROM WorkItems\n"
        "WHERE [System.TeamProject] = @project\n"
        f"  AND [System.WorkItemType] = '{work_item_type.value}'\n"
        f"  AND [Custom.BacklogGeneratorSourceIdentity] = '{source_identity}'"
    )


def _work_item_ids_from_wiql_response(response: Any) -> tuple[int, ...]:
    if not isinstance(response, Mapping):
        raise AzureDevOpsResponseError("Azure DevOps WIQL response must be a JSON object.")
    work_items = response.get("workItems")
    if not isinstance(work_items, list):
        raise AzureDevOpsResponseError("Azure DevOps WIQL response requires a workItems array.")

    work_item_ids: list[int] = []
    for work_item in work_items:
        if not isinstance(work_item, Mapping):
            raise AzureDevOpsResponseError(
                "Azure DevOps WIQL workItems entries must be JSON objects."
            )
        work_item_id = work_item.get("id")
        if type(work_item_id) is not int:
            raise AzureDevOpsResponseError(
                "Azure DevOps WIQL workItems entries require numeric IDs."
            )
        if work_item_id in work_item_ids:
            raise AzureDevOpsResponseError(
                "Azure DevOps WIQL response contains duplicate work-item IDs."
            )
        work_item_ids.append(work_item_id)
    return tuple(work_item_ids)


def _work_item_evidence_from_response(response: Any) -> AzureDevOpsWorkItem:
    if not isinstance(response, Mapping):
        raise AzureDevOpsResponseError("Azure DevOps Work Item response must be a JSON object.")

    work_item_id = _required_work_item_integer(response, "id")
    revision = _required_work_item_integer(response, "rev")
    fields = response.get("fields")
    if not isinstance(fields, Mapping):
        raise AzureDevOpsResponseError("Azure DevOps Work Item response requires a fields object.")

    return AzureDevOpsWorkItem(
        id=work_item_id,
        revision=revision,
        project_name=_required_work_item_field(fields, "System.TeamProject"),
        work_item_type=_required_work_item_field(fields, "System.WorkItemType"),
        source_identity=_required_work_item_field(
            fields, "Custom.BacklogGeneratorSourceIdentity"
        ),
    )


def _required_work_item_integer(response: Mapping[str, Any], name: str) -> int:
    value = response.get(name)
    if type(value) is not int:
        raise AzureDevOpsResponseError(
            f"Azure DevOps Work Item response requires a numeric {name!r}."
        )
    return value


def _required_work_item_field(fields: Mapping[str, Any], name: str) -> str:
    value = fields.get(name)
    if not isinstance(value, str):
        raise AzureDevOpsResponseError(
            f"Azure DevOps Work Item response requires string field {name!r}."
        )
    return value


def _consume_response(response: Any) -> tuple[int, bytes]:
    try:
        return response.getcode(), response.read()
    except OSError as error:
        raise AzureDevOpsTransportError("Azure DevOps response transport failed.") from error
    finally:
        response.close()


def _consume_and_close(response: Any) -> None:
    try:
        response.read()
    except OSError:
        pass
    finally:
        response.close()
