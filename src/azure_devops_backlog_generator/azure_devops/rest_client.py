"""Internal urllib transport foundation for Azure DevOps Services requests."""

from __future__ import annotations

import base64
import json
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
from azure_devops_backlog_generator.azure_devops.models import AzureDevOpsProject
from azure_devops_backlog_generator.documentation.models import WorkItemType

API_VERSION = "7.1"
REQUEST_TIMEOUT_SECONDS = 30
_ACCEPT_HEADER = "application/json"
_COMPATIBILITY_FIELD_REFERENCES = frozenset(
    {
        "System.Title",
        "System.Description",
        "Microsoft.VSTS.Common.AcceptanceCriteria",
        "System.Tags",
        "Custom.BacklogGeneratorSourceIdentity",
    }
)


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
