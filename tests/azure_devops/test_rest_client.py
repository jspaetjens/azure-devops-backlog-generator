"""Tests for the Azure DevOps REST Client Foundation."""

from __future__ import annotations

import base64
import json
from collections.abc import Iterator
from urllib.error import HTTPError, URLError
from urllib.request import ProxyHandler

import pytest

import azure_devops_backlog_generator.azure_devops.rest_client as rest_client_module
from azure_devops_backlog_generator.azure_devops.exceptions import (
    AzureDevOpsHttpError,
    AzureDevOpsResponseError,
    AzureDevOpsTransportError,
)
from azure_devops_backlog_generator.azure_devops.rest_client import (
    API_VERSION,
    REQUEST_TIMEOUT_SECONDS,
    AzureDevOpsRestClient,
)
from azure_devops_backlog_generator.documentation.models import WorkItemType


class _Response:
    def __init__(self, status: int = 200, body: bytes = b'{"id": 1}') -> None:
        self.status = status
        self.body = body
        self.read_called = False
        self.closed = False

    def getcode(self) -> int:
        return self.status

    def read(self) -> bytes:
        self.read_called = True
        return self.body

    def close(self) -> None:
        self.closed = True


class _Opener:
    def __init__(self, response: _Response | Exception) -> None:
        self.response = response
        self.calls: list[tuple[object, int]] = []

    def open(self, request: object, *, timeout: int) -> _Response:
        self.calls.append((request, timeout))
        if isinstance(self.response, Exception):
            raise self.response
        return self.response


@pytest.fixture
def client() -> AzureDevOpsRestClient:
    return AzureDevOpsRestClient("example organization", "Example Project")


@pytest.fixture
def opener(monkeypatch: pytest.MonkeyPatch) -> Iterator[_Opener]:
    fake = _Opener(_Response())
    monkeypatch.setattr(rest_client_module, "_build_opener", lambda: fake)
    yield fake


def _request(client: AzureDevOpsRestClient) -> object:
    return client.send_json_request(
        method="POST",
        path_segments=("_apis", "test", "Product Backlog Item"),
        personal_access_token="secret-pat",
        query={"$top": "2"},
        json_body={"title": "Café"},
        content_type="application/json",
    )


def test_builds_services_urls_with_encoded_path_segments_and_fixed_api_version(
    client: AzureDevOpsRestClient,
) -> None:
    url = client.build_url(
        ("_apis", "wit", "workitems", "Product Backlog Item"), query={"$top": "2"}
    )

    assert url == (
        "https://dev.azure.com/example%20organization/Example%20Project/"
        "_apis/wit/workitems/Product%20Backlog%20Item?%24top=2&api-version=7.1"
    )
    assert API_VERSION == "7.1"
    with pytest.raises(ValueError, match="application controlled"):
        client.build_url(("_apis",), query={"api-version": "8.0"})


def test_uses_https_only_services_url(client: AzureDevOpsRestClient) -> None:
    assert client.build_url(("_apis",)).startswith("https://")


def test_constructs_basic_authentication_without_retaining_the_secret(
    client: AzureDevOpsRestClient, opener: _Opener
) -> None:
    assert _request(client) == {"id": 1}

    request, timeout = opener.calls[0]
    expected = base64.b64encode(b":secret-pat").decode("ascii")
    assert request.get_header("Authorization") == f"Basic {expected}"
    assert timeout == REQUEST_TIMEOUT_SECONDS == 30
    assert "secret-pat" not in repr(client)
    assert "secret-pat" not in client.__dict__.values()


def test_sets_required_headers_and_serializes_json_body(
    client: AzureDevOpsRestClient, opener: _Opener
) -> None:
    _request(client)

    request, _ = opener.calls[0]
    assert request.get_header("Accept") == "application/json"
    assert request.get_header("Content-type") == "application/json"
    assert json.loads(request.data.decode("utf-8")) == {"title": "Café"}


def test_rejects_json_body_without_endpoint_content_type(client: AzureDevOpsRestClient) -> None:
    with pytest.raises(ValueError, match="endpoint content type"):
        client.send_json_request(
            method="POST",
            path_segments=("_apis",),
            personal_access_token="secret-pat",
            json_body={},
        )


def test_builds_a_fresh_opener_that_disables_proxies_and_redirects(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    observed_handlers: tuple[object, ...] = ()

    def capture_handlers(*handlers: object) -> object:
        nonlocal observed_handlers
        observed_handlers = handlers
        return object()

    monkeypatch.setattr(rest_client_module, "build_opener", capture_handlers)

    assert rest_client_module._build_opener() is not None
    proxy_handler = next(
        handler for handler in observed_handlers if isinstance(handler, ProxyHandler)
    )
    redirect_handler = next(
        handler
        for handler in observed_handlers
        if isinstance(handler, rest_client_module._RejectRedirectHandler)
    )

    assert proxy_handler.proxies == {}
    assert redirect_handler.redirect_request(None, None, None, None, None, None, None, None) is None


@pytest.mark.parametrize("status", [201, 204, 301, 302])
def test_rejects_every_unexpected_success_or_redirect_status(
    client: AzureDevOpsRestClient, opener: _Opener, status: int
) -> None:
    response = _Response(status=status)
    opener.response = response

    with pytest.raises(AzureDevOpsHttpError) as error:
        _request(client)

    assert error.value.status == status
    assert response.read_called
    assert response.closed


def test_http_error_is_controlled_and_discards_the_error_body(
    client: AzureDevOpsRestClient, opener: _Opener
) -> None:
    error_response = _Response(status=401, body=b'{"message":"secret-pat"}')
    opener.response = HTTPError("https://dev.azure.com", 401, "Unauthorized", None, error_response)

    with pytest.raises(AzureDevOpsHttpError) as error:
        _request(client)

    assert error.value.status == 401
    assert "secret-pat" not in str(error.value)
    assert error_response.read_called
    assert error_response.closed


@pytest.mark.parametrize(
    "failure",
    [URLError("offline"), TimeoutError()],
)
def test_network_and_timeout_failures_are_controlled_without_retry(
    client: AzureDevOpsRestClient, opener: _Opener, failure: Exception
) -> None:
    opener.response = failure

    with pytest.raises(AzureDevOpsTransportError) as error:
        _request(client)

    assert "secret-pat" not in str(error.value)
    assert len(opener.calls) == 1


@pytest.mark.parametrize("body", [b"", b"not json", b"\xff"])
def test_rejects_missing_or_malformed_json_response_body(
    client: AzureDevOpsRestClient, opener: _Opener, body: bytes
) -> None:
    response = _Response(body=body)
    opener.response = response

    with pytest.raises(AzureDevOpsResponseError):
        _request(client)

    assert response.read_called
    assert response.closed


def test_closes_a_successful_response_after_consuming_its_body(
    client: AzureDevOpsRestClient, opener: _Opener
) -> None:
    response = _Response()
    opener.response = response

    assert _request(client) == {"id": 1}
    assert response.read_called
    assert response.closed


def test_retrieves_the_configured_project_through_the_organisation_endpoint(
    client: AzureDevOpsRestClient, opener: _Opener
) -> None:
    opener.response = _Response(body=b'{"id":"project-id","name":"Canonical Project"}')

    project = client.retrieve_project(personal_access_token="secret-pat")

    request, _ = opener.calls[0]
    assert request.get_method() == "GET"
    assert request.full_url == (
        "https://dev.azure.com/example%20organization/_apis/projects/Example%20Project"
        "?api-version=7.1"
    )
    assert request.data is None
    assert request.get_header("Content-type") is None
    assert project.id == "project-id"
    assert project.name == "Canonical Project"


def test_retrieves_an_identifier_style_configured_project(
    opener: _Opener,
) -> None:
    client = AzureDevOpsRestClient("example organization", "123e4567-e89b-12d3-a456-426614174000")
    opener.response = _Response(body=b'{"id":"canonical-id","name":"Canonical Project"}')

    client.retrieve_project(personal_access_token="secret-pat")

    request, _ = opener.calls[0]
    assert request.full_url == (
        "https://dev.azure.com/example%20organization/_apis/projects/"
        "123e4567-e89b-12d3-a456-426614174000?api-version=7.1"
    )


def test_retrieved_project_model_is_immutable(
    client: AzureDevOpsRestClient, opener: _Opener
) -> None:
    opener.response = _Response(body=b'{"id":"project-id","name":"Canonical Project"}')

    project = client.retrieve_project(personal_access_token="secret-pat")

    with pytest.raises(AttributeError):
        project.name = "Changed"  # type: ignore[misc]


@pytest.mark.parametrize(
    ("body", "field"),
    [
        (b'{"name":"Canonical Project"}', "id"),
        (b'{"id":null,"name":"Canonical Project"}', "id"),
        (b'{"id":"","name":"Canonical Project"}', "id"),
        (b'{"id":"   ","name":"Canonical Project"}', "id"),
        (b'{"id":1,"name":"Canonical Project"}', "id"),
        (b'{"id":"project-id"}', "name"),
        (b'{"id":"project-id","name":null}', "name"),
        (b'{"id":"project-id","name":""}', "name"),
        (b'{"id":"project-id","name":"   "}', "name"),
        (b'{"id":"project-id","name":1}', "name"),
    ],
)
def test_rejects_missing_or_invalid_required_project_evidence(
    client: AzureDevOpsRestClient, opener: _Opener, body: bytes, field: str
) -> None:
    opener.response = _Response(body=body)

    with pytest.raises(AzureDevOpsResponseError, match=field):
        client.retrieve_project(personal_access_token="secret-pat")


@pytest.mark.parametrize("body", [b"[]", b'"project"', b"1", b"null"])
def test_rejects_non_object_project_response(
    client: AzureDevOpsRestClient, opener: _Opener, body: bytes
) -> None:
    opener.response = _Response(body=body)

    with pytest.raises(AzureDevOpsResponseError, match="JSON object"):
        client.retrieve_project(personal_access_token="secret-pat")


def test_project_retrieval_reuses_the_transport_failure_without_retry(
    client: AzureDevOpsRestClient, opener: _Opener
) -> None:
    opener.response = URLError("offline")

    with pytest.raises(AzureDevOpsTransportError):
        client.retrieve_project(personal_access_token="secret-pat")

    assert len(opener.calls) == 1


@pytest.mark.parametrize(
    ("work_item_type", "encoded_type"),
    [
        (WorkItemType.EPIC, "Epic"),
        (WorkItemType.FEATURE, "Feature"),
        (WorkItemType.PRODUCT_BACKLOG_ITEM, "Product%20Backlog%20Item"),
        (WorkItemType.TASK, "Task"),
    ],
)
def test_retrieves_metadata_for_each_supported_work_item_type(
    client: AzureDevOpsRestClient,
    opener: _Opener,
    work_item_type: WorkItemType,
    encoded_type: str,
) -> None:
    metadata = {"name": work_item_type.value, "fields": []}
    opener.response = _Response(body=json.dumps(metadata).encode())

    returned_metadata = client.retrieve_work_item_type(
        work_item_type, personal_access_token="secret-pat"
    )

    request, _ = opener.calls[0]
    assert request.get_method() == "GET"
    assert request.full_url == (
        "https://dev.azure.com/example%20organization/Example%20Project/"
        f"_apis/wit/workitemtypes/{encoded_type}?api-version=7.1"
    )
    assert request.data is None
    assert request.get_header("Content-type") is None
    assert returned_metadata == metadata


def test_rejects_an_unsupported_work_item_type(
    client: AzureDevOpsRestClient,
) -> None:
    with pytest.raises(ValueError, match="supported WorkItemType"):
        client.retrieve_work_item_type("User Story", personal_access_token="secret-pat")  # type: ignore[arg-type]


@pytest.mark.parametrize("body", [b"[]", b'"Epic"', b"1", b"null"])
def test_rejects_non_object_work_item_type_response(
    client: AzureDevOpsRestClient, opener: _Opener, body: bytes
) -> None:
    opener.response = _Response(body=body)

    with pytest.raises(AzureDevOpsResponseError, match="JSON object"):
        client.retrieve_work_item_type(WorkItemType.EPIC, personal_access_token="secret-pat")


def test_work_item_type_retrieval_reuses_the_transport_failure_without_retry(
    client: AzureDevOpsRestClient, opener: _Opener
) -> None:
    opener.response = URLError("offline")

    with pytest.raises(AzureDevOpsTransportError):
        client.retrieve_work_item_type(WorkItemType.EPIC, personal_access_token="secret-pat")

    assert len(opener.calls) == 1


@pytest.mark.parametrize(
    ("work_item_type", "encoded_type"),
    [
        (WorkItemType.EPIC, "Epic"),
        (WorkItemType.FEATURE, "Feature"),
        (WorkItemType.PRODUCT_BACKLOG_ITEM, "Product%20Backlog%20Item"),
        (WorkItemType.TASK, "Task"),
    ],
)
@pytest.mark.parametrize(
    "field_reference",
    [
        "System.Title",
        "System.Description",
        "Microsoft.VSTS.Common.AcceptanceCriteria",
        "System.Tags",
        "Custom.BacklogGeneratorSourceIdentity",
    ],
)
def test_retrieves_metadata_for_every_approved_work_item_type_field_pair(
    client: AzureDevOpsRestClient,
    opener: _Opener,
    work_item_type: WorkItemType,
    encoded_type: str,
    field_reference: str,
) -> None:
    metadata = {"referenceName": field_reference}
    opener.response = _Response(body=json.dumps(metadata).encode())

    returned_metadata = client.retrieve_work_item_type_field(
        work_item_type,
        field_reference,
        personal_access_token="secret-pat",
    )

    request, _ = opener.calls[0]
    assert request.get_method() == "GET"
    assert request.full_url == (
        "https://dev.azure.com/example%20organization/Example%20Project/"
        f"_apis/wit/workitemtypes/{encoded_type}/fields/{field_reference}"
        "?%24expand=All&api-version=7.1"
    )
    assert request.data is None
    assert request.get_header("Content-type") is None
    assert returned_metadata == metadata


def test_rejects_an_unsupported_work_item_type_for_field_metadata(
    client: AzureDevOpsRestClient,
) -> None:
    with pytest.raises(ValueError, match="supported WorkItemType"):
        client.retrieve_work_item_type_field(  # type: ignore[arg-type]
            "User Story",
            "System.Title",
            personal_access_token="secret-pat",
        )


def test_rejects_an_unsupported_field_reference(
    client: AzureDevOpsRestClient,
) -> None:
    with pytest.raises(ValueError, match="approved field reference"):
        client.retrieve_work_item_type_field(
            WorkItemType.EPIC,
            "System.State",
            personal_access_token="secret-pat",
        )


@pytest.mark.parametrize("body", [b"[]", b'"field"', b"1", b"null"])
def test_rejects_non_object_work_item_type_field_response(
    client: AzureDevOpsRestClient, opener: _Opener, body: bytes
) -> None:
    opener.response = _Response(body=body)

    with pytest.raises(AzureDevOpsResponseError, match="JSON object"):
        client.retrieve_work_item_type_field(
            WorkItemType.EPIC,
            "System.Title",
            personal_access_token="secret-pat",
        )


def test_work_item_type_field_retrieval_reuses_transport_failure_without_retry(
    client: AzureDevOpsRestClient, opener: _Opener
) -> None:
    opener.response = URLError("offline")

    with pytest.raises(AzureDevOpsTransportError):
        client.retrieve_work_item_type_field(
            WorkItemType.EPIC,
            "System.Title",
            personal_access_token="secret-pat",
        )

    assert len(opener.calls) == 1
