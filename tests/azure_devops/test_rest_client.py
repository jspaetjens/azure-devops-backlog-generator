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
from azure_devops_backlog_generator.azure_devops.models import (
    AzureDevOpsWorkItem,
    AzureDevOpsWorkItemRelationshipState,
)
from azure_devops_backlog_generator.azure_devops.rest_client import (
    API_VERSION,
    REQUEST_TIMEOUT_SECONDS,
    AzureDevOpsRestClient,
    build_parent_child_relationship_json_patch,
    build_work_item_create_json_patch,
)
from azure_devops_backlog_generator.documentation.models import WorkItemType
from azure_devops_backlog_generator.generator.candidates import WorkItemCandidate


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


def _request(client: AzureDevOpsRestClient, personal_access_token: str = "secret-pat") -> object:
    return client.send_json_request(
        method="POST",
        path_segments=("_apis", "test", "Product Backlog Item"),
        personal_access_token=personal_access_token,
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


def test_http_403_is_controlled_without_retry_or_credential_disclosure(
    client: AzureDevOpsRestClient, opener: _Opener
) -> None:
    personal_access_token = "review-gate-403-pat"
    authorization = f"Basic {base64.b64encode(f':{personal_access_token}'.encode()).decode()}"
    error_response = _Response(status=403, body=b'{"message":"Forbidden"}')
    opener.response = HTTPError("https://dev.azure.com", 403, "Forbidden", None, error_response)

    with pytest.raises(AzureDevOpsHttpError) as error:
        _request(client, personal_access_token)

    assert error.value.status == 403
    assert len(opener.calls) == 1
    request, _ = opener.calls[0]
    assert request.get_header("Authorization") == authorization
    assert personal_access_token not in str(error.value)
    assert personal_access_token not in repr(error.value)
    assert authorization not in str(error.value)
    assert authorization not in repr(error.value)
    assert personal_access_token not in error.value.__dict__.values()
    assert authorization not in error.value.__dict__.values()
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
def test_retrieves_global_metadata_for_every_approved_field(
    client: AzureDevOpsRestClient,
    opener: _Opener,
    field_reference: str,
) -> None:
    metadata = {"referenceName": field_reference}
    opener.response = _Response(body=json.dumps(metadata).encode())

    returned_metadata = client.retrieve_field(
        field_reference,
        personal_access_token="secret-pat",
    )

    request, _ = opener.calls[0]
    assert request.get_method() == "GET"
    assert request.full_url == (
        "https://dev.azure.com/example%20organization/Example%20Project/"
        f"_apis/wit/fields/{field_reference}?api-version=7.1"
    )
    assert request.data is None
    assert request.get_header("Content-type") is None
    assert returned_metadata == metadata


def test_rejects_an_unsupported_global_field_reference_before_transmission(
    client: AzureDevOpsRestClient, opener: _Opener
) -> None:
    with pytest.raises(ValueError, match="approved field reference"):
        client.retrieve_field("System.State", personal_access_token="secret-pat")

    assert opener.calls == []


@pytest.mark.parametrize("body", [b"[]", b'"field"', b"1", b"null"])
def test_rejects_non_object_global_field_response(
    client: AzureDevOpsRestClient, opener: _Opener, body: bytes
) -> None:
    opener.response = _Response(body=body)

    with pytest.raises(AzureDevOpsResponseError, match="JSON object"):
        client.retrieve_field("System.Title", personal_access_token="secret-pat")


def test_global_field_retrieval_reuses_transport_failure_without_retry(
    client: AzureDevOpsRestClient, opener: _Opener
) -> None:
    opener.response = URLError("offline")

    with pytest.raises(AzureDevOpsTransportError):
        client.retrieve_field("System.Title", personal_access_token="secret-pat")

    assert len(opener.calls) == 1


def _candidate(
    work_item_type: WorkItemType = WorkItemType.EPIC,
    *,
    acceptance_criteria_html: str | None = None,
    tags_value: str | None = None,
    source_identity: str = "adbg:source-id:v1:sha256:" + "a" * 64,
) -> WorkItemCandidate:
    return WorkItemCandidate(
        work_item_type=work_item_type,
        title="Prepared title",
        description_html="<p>Prepared description</p>\n",
        acceptance_criteria_html=acceptance_criteria_html,
        tags_value=tags_value,
        source_identity=source_identity,
    )


def test_builds_the_exact_three_operation_work_item_create_json_patch() -> None:
    candidate = _candidate()

    assert build_work_item_create_json_patch(candidate) == [
        {"op": "add", "path": "/fields/System.Title", "value": candidate.title},
        {
            "op": "add",
            "path": "/fields/System.Description",
            "value": candidate.description_html,
        },
        {
            "op": "add",
            "path": "/fields/Custom.BacklogGeneratorSourceIdentity",
            "value": candidate.source_identity,
        },
    ]


def test_builds_the_exact_four_operation_json_patch_with_acceptance_criteria() -> None:
    candidate = _candidate(acceptance_criteria_html="<ul>\n<li>Criterion</li>\n</ul>\n")

    assert build_work_item_create_json_patch(candidate) == [
        {"op": "add", "path": "/fields/System.Title", "value": candidate.title},
        {
            "op": "add",
            "path": "/fields/System.Description",
            "value": candidate.description_html,
        },
        {
            "op": "add",
            "path": "/fields/Microsoft.VSTS.Common.AcceptanceCriteria",
            "value": candidate.acceptance_criteria_html,
        },
        {
            "op": "add",
            "path": "/fields/Custom.BacklogGeneratorSourceIdentity",
            "value": candidate.source_identity,
        },
    ]


def test_builds_the_exact_four_operation_json_patch_with_tags() -> None:
    candidate = _candidate(tags_value="platform; generator")

    assert build_work_item_create_json_patch(candidate) == [
        {"op": "add", "path": "/fields/System.Title", "value": candidate.title},
        {
            "op": "add",
            "path": "/fields/System.Description",
            "value": candidate.description_html,
        },
        {"op": "add", "path": "/fields/System.Tags", "value": candidate.tags_value},
        {
            "op": "add",
            "path": "/fields/Custom.BacklogGeneratorSourceIdentity",
            "value": candidate.source_identity,
        },
    ]


def test_builds_the_exact_five_operation_work_item_create_json_patch() -> None:
    candidate = _candidate(
        acceptance_criteria_html="<ul>\n<li>Criterion</li>\n</ul>\n",
        tags_value="platform; generator",
    )

    operations = build_work_item_create_json_patch(candidate)

    assert [operation["path"] for operation in operations] == [
        "/fields/System.Title",
        "/fields/System.Description",
        "/fields/Microsoft.VSTS.Common.AcceptanceCriteria",
        "/fields/System.Tags",
        "/fields/Custom.BacklogGeneratorSourceIdentity",
    ]
    assert all(operation["op"] == "add" for operation in operations)
    assert operations[-1]["value"] == candidate.source_identity


@pytest.mark.parametrize(
    "work_item_type",
    (WorkItemType.EPIC, WorkItemType.FEATURE, WorkItemType.PRODUCT_BACKLOG_ITEM),
)
def test_emits_acceptance_criteria_for_each_applicable_work_item_type(
    work_item_type: WorkItemType,
) -> None:
    candidate = _candidate(work_item_type, acceptance_criteria_html="<p>Criterion</p>\n")

    assert "/fields/Microsoft.VSTS.Common.AcceptanceCriteria" in [
        operation["path"] for operation in build_work_item_create_json_patch(candidate)
    ]


def test_never_emits_task_acceptance_criteria() -> None:
    candidate = _candidate(WorkItemType.TASK, acceptance_criteria_html="<p>Invalid</p>\n")

    assert "/fields/Microsoft.VSTS.Common.AcceptanceCriteria" not in [
        operation["path"] for operation in build_work_item_create_json_patch(candidate)
    ]


def test_empty_optional_values_are_not_treated_as_absent() -> None:
    candidate = _candidate(acceptance_criteria_html="", tags_value="")

    operations = build_work_item_create_json_patch(candidate)

    assert operations[2]["value"] == ""
    assert operations[3]["value"] == ""


def test_json_patch_construction_does_not_transmit_a_request(opener: _Opener) -> None:
    build_work_item_create_json_patch(_candidate())

    assert opener.calls == []


def test_builds_the_exact_parent_child_relationship_json_patch() -> None:
    patch = build_parent_child_relationship_json_patch("example organization", 11, 7)

    assert patch == [
        {"op": "test", "path": "/rev", "value": 7},
        {
            "op": "add",
            "path": "/relations/-",
            "value": {
                "rel": "System.LinkTypes.Hierarchy-Reverse",
                "url": "https://dev.azure.com/example%20organization/_apis/wit/workItems/11",
            },
        },
    ]


def test_parent_child_relationship_json_patch_target_has_no_project_or_query() -> None:
    patch = build_parent_child_relationship_json_patch("example", 11, 7)
    target_url = patch[1]["value"]

    assert isinstance(target_url, dict)
    assert target_url["url"] == "https://dev.azure.com/example/_apis/wit/workItems/11"
    assert "Example%20Project" not in target_url["url"]
    assert "api-version" not in target_url["url"]
    assert "?" not in target_url["url"]
    assert "#" not in target_url["url"]


def test_parent_child_relationship_json_patch_is_deterministic() -> None:
    first = build_parent_child_relationship_json_patch("example", 0, -1)
    second = build_parent_child_relationship_json_patch("example", 0, -1)

    assert first == second
    assert first[0]["value"] == -1
    relation = first[1]["value"]
    assert isinstance(relation, dict)
    assert relation["url"].endswith("/0")


@pytest.mark.parametrize("parent_work_item_id", [True, False, "11", 11.0, None, object()])
def test_rejects_non_integer_parent_work_item_id_for_relationship_patch(
    parent_work_item_id: object,
) -> None:
    with pytest.raises(ValueError, match="parent Work Item ID"):
        build_parent_child_relationship_json_patch(
            "example", parent_work_item_id, 7  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("child_revision", [True, False, "7", 7.0, None, object()])
def test_rejects_non_integer_child_revision_for_relationship_patch(
    child_revision: object,
) -> None:
    with pytest.raises(ValueError, match="child revision"):
        build_parent_child_relationship_json_patch(
            "example", 11, child_revision  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("child_work_item_id", [17, 0, -1])
def test_patches_parent_child_relationship_with_the_exact_endpoint_contract(
    client: AzureDevOpsRestClient,
    opener: _Opener,
    child_work_item_id: int,
) -> None:
    response = _Response(body=b"{}")
    opener.response = response

    assert (
        client.patch_parent_child_relationship(
            11,
            child_work_item_id,
            7,
            personal_access_token="secret-pat",
        )
        is None
    )

    request, timeout = opener.calls[0]
    assert request.get_method() == "PATCH"
    assert request.full_url == (
        "https://dev.azure.com/example%20organization/Example%20Project/"
        f"_apis/wit/workitems/{child_work_item_id}?api-version=7.1"
    )
    assert request.get_header("Content-type") == "application/json-patch+json"
    assert request.get_header("Accept") == "application/json"
    assert request.get_header("Authorization") == "Basic OnNlY3JldC1wYXQ="
    assert timeout == REQUEST_TIMEOUT_SECONDS
    assert json.loads(request.data.decode("utf-8")) == build_parent_child_relationship_json_patch(
        "example organization", 11, 7
    )
    assert "validateOnly" not in request.full_url
    assert "bypassRules" not in request.full_url
    assert "suppressNotifications" not in request.full_url
    assert "%24expand" not in request.full_url
    assert "fields" not in request.full_url
    assert len(opener.calls) == 1
    assert response.read_called
    assert response.closed


def test_parent_child_relationship_patch_ignores_unknown_response_properties(
    client: AzureDevOpsRestClient, opener: _Opener
) -> None:
    opener.response = _Response(
        body=b'{"id":17,"rev":8,"fields":{},"relations":[],"unexpected":"ignored"}'
    )

    assert (
        client.patch_parent_child_relationship(
            11, 17, 7, personal_access_token="secret-pat"
        )
        is None
    )


@pytest.mark.parametrize("child_work_item_id", [True, False, "17", 17.0, None, object()])
def test_rejects_non_integer_child_work_item_id_for_relationship_patch_before_transport(
    client: AzureDevOpsRestClient,
    opener: _Opener,
    child_work_item_id: object,
) -> None:
    with pytest.raises(ValueError, match=r"A numeric child Work Item ID is required\."):
        client.patch_parent_child_relationship(
            11,
            child_work_item_id,  # type: ignore[arg-type]
            7,
            personal_access_token="secret-pat",
        )

    assert opener.calls == []


@pytest.mark.parametrize(
    "body",
    [b"[]", b'"value"', b"17", b"1.5", b"true", b"false", b"null"],
)
def test_rejects_non_object_parent_child_relationship_patch_response(
    client: AzureDevOpsRestClient, opener: _Opener, body: bytes
) -> None:
    response = _Response(body=body)
    opener.response = response

    with pytest.raises(
        AzureDevOpsResponseError,
        match=r"Azure DevOps Parent-Child Relationship PATCH response must be a JSON object\.",
    ):
        client.patch_parent_child_relationship(11, 17, 7, personal_access_token="secret-pat")

    assert len(opener.calls) == 1
    assert response.read_called
    assert response.closed


@pytest.mark.parametrize("body", [b"", b"\xff", b"not json"])
def test_parent_child_relationship_patch_reuses_malformed_response_validation(
    client: AzureDevOpsRestClient, opener: _Opener, body: bytes
) -> None:
    response = _Response(body=body)
    opener.response = response

    with pytest.raises(AzureDevOpsResponseError):
        client.patch_parent_child_relationship(11, 17, 7, personal_access_token="secret-pat")

    assert response.read_called
    assert response.closed


def test_parent_child_relationship_patch_preserves_http_failure_without_retry(
    client: AzureDevOpsRestClient, opener: _Opener
) -> None:
    response = _Response(status=409)
    opener.response = response

    with pytest.raises(AzureDevOpsHttpError) as error:
        client.patch_parent_child_relationship(11, 17, 7, personal_access_token="secret-pat")

    assert error.value.status == 409
    assert len(opener.calls) == 1
    assert response.read_called
    assert response.closed


def test_parent_child_relationship_patch_preserves_transport_failure_without_retry(
    client: AzureDevOpsRestClient, opener: _Opener
) -> None:
    opener.response = URLError("offline")

    with pytest.raises(AzureDevOpsTransportError):
        client.patch_parent_child_relationship(11, 17, 7, personal_access_token="secret-pat")

    assert len(opener.calls) == 1


@pytest.mark.parametrize("child_work_item_id", [17, 0, -1])
def test_retrieves_work_item_relationship_state_with_the_exact_get_contract(
    client: AzureDevOpsRestClient,
    opener: _Opener,
    child_work_item_id: int,
) -> None:
    response = _Response(
        body=json.dumps(
            _relationship_state_response(child_work_item_id=child_work_item_id)
        ).encode()
    )
    opener.response = response

    result = client.retrieve_work_item_relationship_state(
        child_work_item_id, personal_access_token="secret-pat"
    )

    assert result == AzureDevOpsWorkItemRelationshipState(revision=3, reverse_parent_ids=())
    request, timeout = opener.calls[0]
    assert request.get_method() == "GET"
    assert request.full_url == (
        "https://dev.azure.com/example%20organization/Example%20Project/"
        f"_apis/wit/workitems/{child_work_item_id}?%24expand=relations&api-version=7.1"
    )
    assert request.get_header("Accept") == "application/json"
    assert request.get_header("Authorization") == "Basic OnNlY3JldC1wYXQ="
    assert request.get_header("Content-type") is None
    assert request.data is None
    assert timeout == REQUEST_TIMEOUT_SECONDS
    assert "fields" not in request.full_url
    assert len(opener.calls) == 1
    assert response.read_called
    assert response.closed


@pytest.mark.parametrize("child_work_item_id", [True, False, "17", 17.0, None, object()])
def test_rejects_non_integer_child_work_item_id_for_relationship_state_before_transport(
    client: AzureDevOpsRestClient,
    opener: _Opener,
    child_work_item_id: object,
) -> None:
    with pytest.raises(ValueError, match=r"A numeric child Work Item ID is required\."):
        client.retrieve_work_item_relationship_state(
            child_work_item_id,  # type: ignore[arg-type]
            personal_access_token="secret-pat",
        )

    assert opener.calls == []


@pytest.mark.parametrize(
    "body", [b"[]", b'"work item"', b"1", b"1.5", b"true", b"false", b"null"]
)
def test_rejects_non_object_work_item_relationship_state_response(
    client: AzureDevOpsRestClient, opener: _Opener, body: bytes
) -> None:
    opener.response = _Response(body=body)

    with pytest.raises(
        AzureDevOpsResponseError,
        match=r"Azure DevOps Work Item relationship-state response must be a JSON object\.",
    ):
        client.retrieve_work_item_relationship_state(17, personal_access_token="secret-pat")


@pytest.mark.parametrize(
    "response",
    [
        {"rev": 3},
        {"id": None, "rev": 3},
        {"id": True, "rev": 3},
        {"id": "17", "rev": 3},
        {"id": 17.0, "rev": 3},
    ],
)
def test_rejects_missing_or_invalid_relationship_state_response_id(
    client: AzureDevOpsRestClient, opener: _Opener, response: dict[str, object]
) -> None:
    opener.response = _Response(body=json.dumps(response).encode())

    with pytest.raises(AzureDevOpsResponseError, match="numeric"):
        client.retrieve_work_item_relationship_state(17, personal_access_token="secret-pat")


def test_rejects_mismatched_relationship_state_response_id(
    client: AzureDevOpsRestClient, opener: _Opener
) -> None:
    opener.response = _Response(body=json.dumps(_relationship_state_response(18)).encode())

    with pytest.raises(AzureDevOpsResponseError, match="does not match"):
        client.retrieve_work_item_relationship_state(17, personal_access_token="secret-pat")


@pytest.mark.parametrize(
    "revision", [None, True, False, "3", 3.0]
)
def test_rejects_invalid_relationship_state_revision(
    client: AzureDevOpsRestClient, opener: _Opener, revision: object
) -> None:
    opener.response = _Response(
        body=json.dumps(_relationship_state_response(revision=revision)).encode()
    )

    with pytest.raises(AzureDevOpsResponseError, match="numeric"):
        client.retrieve_work_item_relationship_state(17, personal_access_token="secret-pat")


def test_rejects_missing_relationship_state_revision(
    client: AzureDevOpsRestClient, opener: _Opener
) -> None:
    response = _relationship_state_response()
    response.pop("rev")
    opener.response = _Response(body=json.dumps(response).encode())

    with pytest.raises(AzureDevOpsResponseError, match="numeric"):
        client.retrieve_work_item_relationship_state(17, personal_access_token="secret-pat")


@pytest.mark.parametrize("revision", [0, -1])
def test_accepts_non_positive_relationship_state_revision(
    client: AzureDevOpsRestClient, opener: _Opener, revision: int
) -> None:
    opener.response = _Response(
        body=json.dumps(_relationship_state_response(revision=revision)).encode()
    )

    assert client.retrieve_work_item_relationship_state(
        17, personal_access_token="secret-pat"
    ).revision == revision


@pytest.mark.parametrize("relations", [None, []])
def test_accepts_relationship_state_zero_relation_representations(
    client: AzureDevOpsRestClient, opener: _Opener, relations: object
) -> None:
    response = _relationship_state_response()
    if relations is not None:
        response["relations"] = relations
    opener.response = _Response(body=json.dumps(response).encode())

    assert client.retrieve_work_item_relationship_state(
        17, personal_access_token="secret-pat"
    ).reverse_parent_ids == ()


@pytest.mark.parametrize("relations", [None, {}, "relations", 1, 1.5, True])
def test_rejects_invalid_relationship_state_relations_property(
    client: AzureDevOpsRestClient, opener: _Opener, relations: object
) -> None:
    opener.response = _Response(
        body=json.dumps(_relationship_state_response(relations=relations)).encode()
    )

    with pytest.raises(AzureDevOpsResponseError, match="relations array"):
        client.retrieve_work_item_relationship_state(17, personal_access_token="secret-pat")


@pytest.mark.parametrize(
    "relations",
    [
        ["relation"],
        [{"rel": "Related", "url": "https://example.test"}, 1],
        [{}],
        [{"rel": "", "url": "https://example.test"}],
        [{"rel": 1, "url": "https://example.test"}],
        [{"rel": "Related"}],
        [{"rel": "Related", "url": ""}],
        [{"rel": "Related", "url": 1}],
    ],
)
def test_rejects_malformed_relationship_state_relation_members(
    client: AzureDevOpsRestClient, opener: _Opener, relations: list[object]
) -> None:
    opener.response = _Response(
        body=json.dumps(_relationship_state_response(relations=relations)).encode()
    )

    with pytest.raises(AzureDevOpsResponseError):
        client.retrieve_work_item_relationship_state(17, personal_access_token="secret-pat")


def test_ignores_well_formed_unrelated_relationship_state_relations(
    client: AzureDevOpsRestClient, opener: _Opener
) -> None:
    relations = [
        {
            "rel": "System.LinkTypes.Hierarchy-Forward",
            "url": "https://example.test/forward",
            "attributes": {"name": "Child"},
            "unexpected": "ignored",
        },
        {"rel": "Related", "url": "https://example.test/related"},
    ]
    opener.response = _Response(
        body=json.dumps(_relationship_state_response(relations=relations)).encode()
    )

    assert client.retrieve_work_item_relationship_state(
        17, personal_access_token="secret-pat"
    ).reverse_parent_ids == ()


def test_returns_ordered_duplicate_preserving_reverse_parent_ids(
    client: AzureDevOpsRestClient, opener: _Opener
) -> None:
    relations = [
        _reverse_relation(11),
        {"rel": "Related", "url": "https://example.test/related"},
        _reverse_relation(12),
        _reverse_relation(11),
    ]
    opener.response = _Response(
        body=json.dumps(_relationship_state_response(relations=relations)).encode()
    )

    assert client.retrieve_work_item_relationship_state(
        17, personal_access_token="secret-pat"
    ) == AzureDevOpsWorkItemRelationshipState(revision=3, reverse_parent_ids=(11, 12, 11))


def test_rejects_case_altered_reverse_relationship_reference(
    client: AzureDevOpsRestClient, opener: _Opener
) -> None:
    opener.response = _Response(
        body=json.dumps(
            _relationship_state_response(
                relations=[
                    {
                        "rel": "system.linktypes.hierarchy-reverse",
                        "url": "https://example.test/ignored",
                    }
                ]
            )
        ).encode()
    )

    with pytest.raises(AzureDevOpsResponseError, match="case-altered"):
        client.retrieve_work_item_relationship_state(17, personal_access_token="secret-pat")


@pytest.mark.parametrize(
    "url",
    [
        "/example%20organization/_apis/wit/workItems/11",
        "http://dev.azure.com/example%20organization/_apis/wit/workItems/11",
        "https://example.test/example%20organization/_apis/wit/workItems/11",
        "https://dev.azure.com/other/_apis/wit/workItems/11",
        "https://dev.azure.com/_apis/wit/workItems/11",
        "https://dev.azure.com/example%20organization/_apis/wit/workitems/11",
        "https://dev.azure.com/example%20organization/Example%20Project/_apis/wit/workItems/11",
        "https://dev.azure.com/example%20organization/_apis/wit/workItems/11?x=1",
        "https://dev.azure.com/example%20organization/_apis/wit/workItems/11#fragment",
        "https://dev.azure.com/example%20organization/_apis/wit/workItems/11/extra",
        "https://dev.azure.com/example%20organization/_apis/wit/workItems",
        "https://dev.azure.com/example%20organization/_apis/wit/workItems/",
        "https://dev.azure.com/example%20organization/_apis/wit/workItems/abc",
        "https://dev.azure.com/example%20organization/_apis/wit/workItems/1a",
        "https://dev.azure.com/example%20organization/_apis/wit/workItems/+1",
        "https://dev.azure.com/example%20organization/_apis/wit/workItems/-1",
        "https://dev.azure.com/example%20organization/_apis/wit/workItems/0",
        "https://user@dev.azure.com/example%20organization/_apis/wit/workItems/11",
        "https://dev.azure.com:443/example%20organization/_apis/wit/workItems/11",
        "https://[::1/example%20organization/_apis/wit/workItems/11",
    ],
)
def test_rejects_invalid_reverse_parent_relationship_urls(
    client: AzureDevOpsRestClient, opener: _Opener, url: str
) -> None:
    opener.response = _Response(
        body=json.dumps(
            _relationship_state_response(
                relations=[{"rel": "System.LinkTypes.Hierarchy-Reverse", "url": url}]
            )
        ).encode()
    )

    with pytest.raises(AzureDevOpsResponseError, match="invalid reverse hierarchy"):
        client.retrieve_work_item_relationship_state(17, personal_access_token="secret-pat")


@pytest.mark.parametrize("body", [b"", b"\xff", b"not json"])
def test_relationship_state_reuses_malformed_response_validation(
    client: AzureDevOpsRestClient, opener: _Opener, body: bytes
) -> None:
    response = _Response(body=body)
    opener.response = response

    with pytest.raises(AzureDevOpsResponseError):
        client.retrieve_work_item_relationship_state(17, personal_access_token="secret-pat")

    assert response.read_called
    assert response.closed


def test_relationship_state_preserves_http_failure_without_retry(
    client: AzureDevOpsRestClient, opener: _Opener
) -> None:
    response = _Response(status=404)
    opener.response = response

    with pytest.raises(AzureDevOpsHttpError) as error:
        client.retrieve_work_item_relationship_state(17, personal_access_token="secret-pat")

    assert error.value.status == 404
    assert len(opener.calls) == 1
    assert response.read_called
    assert response.closed


def test_relationship_state_preserves_transport_failure_without_retry(
    client: AzureDevOpsRestClient, opener: _Opener
) -> None:
    opener.response = URLError("offline")

    with pytest.raises(AzureDevOpsTransportError):
        client.retrieve_work_item_relationship_state(17, personal_access_token="secret-pat")

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
def test_validates_work_item_create_with_the_exact_endpoint_contract(
    client: AzureDevOpsRestClient,
    opener: _Opener,
    work_item_type: WorkItemType,
    encoded_type: str,
) -> None:
    candidate = _candidate(work_item_type, tags_value="platform; generator")
    opener.response = _Response(body=b'{"validation":"accepted"}')

    assert client.validate_work_item_create(candidate, personal_access_token="secret-pat") is None

    request, _ = opener.calls[0]
    assert request.get_method() == "POST"
    assert request.full_url == (
        "https://dev.azure.com/example%20organization/Example%20Project/"
        f"_apis/wit/workitems/{encoded_type}?validateOnly=true&api-version=7.1"
    )
    assert request.get_header("Content-type") == "application/json-patch+json"
    assert request.get_header("Accept") == "application/json"
    assert request.get_header("Authorization") == "Basic OnNlY3JldC1wYXQ="
    assert json.loads(request.data.decode("utf-8")) == build_work_item_create_json_patch(candidate)
    assert "bypassRules" not in request.full_url
    assert "suppressNotifications" not in request.full_url
    assert "%24expand" not in request.full_url


def test_validation_only_create_uses_the_existing_controlled_http_failure(
    client: AzureDevOpsRestClient, opener: _Opener
) -> None:
    response = _Response(status=400)
    opener.response = response

    with pytest.raises(AzureDevOpsHttpError) as error:
        client.validate_work_item_create(_candidate(), personal_access_token="secret-pat")

    assert error.value.status == 400
    assert len(opener.calls) == 1
    assert response.read_called
    assert response.closed


@pytest.mark.parametrize("body", [b"", b"not json", b"\xff"])
def test_validation_only_create_reuses_response_validation(
    client: AzureDevOpsRestClient, opener: _Opener, body: bytes
) -> None:
    response = _Response(body=body)
    opener.response = response

    with pytest.raises(AzureDevOpsResponseError):
        client.validate_work_item_create(_candidate(), personal_access_token="secret-pat")

    assert response.read_called
    assert response.closed


def test_validation_only_create_reuses_transport_failure_without_retry(
    client: AzureDevOpsRestClient, opener: _Opener
) -> None:
    opener.response = URLError("offline")

    with pytest.raises(AzureDevOpsTransportError):
        client.validate_work_item_create(_candidate(), personal_access_token="secret-pat")

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
def test_creates_work_item_with_the_exact_persistent_endpoint_contract(
    client: AzureDevOpsRestClient,
    opener: _Opener,
    work_item_type: WorkItemType,
    encoded_type: str,
) -> None:
    candidate = _candidate(work_item_type, tags_value="platform; generator")
    opener.response = _Response(body=json.dumps(_work_item_response()).encode())

    result = client.create_work_item(candidate, personal_access_token="secret-pat")

    assert result == AzureDevOpsWorkItem(
        id=17,
        revision=3,
        project_name="Canonical Project",
        work_item_type="Epic",
        source_identity="adbg:source-id:v1:sha256:" + "a" * 64,
    )
    request, _ = opener.calls[0]
    assert request.get_method() == "POST"
    assert request.full_url == (
        "https://dev.azure.com/example%20organization/Example%20Project/"
        f"_apis/wit/workitems/{encoded_type}?api-version=7.1"
    )
    assert request.get_header("Content-type") == "application/json-patch+json"
    assert request.get_header("Accept") == "application/json"
    assert request.get_header("Authorization") == "Basic OnNlY3JldC1wYXQ="
    assert json.loads(request.data.decode("utf-8")) == build_work_item_create_json_patch(candidate)
    assert "validateOnly" not in request.full_url
    assert "bypassRules" not in request.full_url
    assert "suppressNotifications" not in request.full_url
    assert "%24expand" not in request.full_url


def test_persistent_create_ignores_unknown_response_properties_and_fields(
    client: AzureDevOpsRestClient, opener: _Opener
) -> None:
    response = _work_item_response(unexpected="ignored")
    fields = response["fields"]
    assert isinstance(fields, dict)
    fields["System.Title"] = "Ignored title"
    opener.response = _Response(body=json.dumps(response).encode())

    assert client.create_work_item(_candidate(), personal_access_token="secret-pat").id == 17


@pytest.mark.parametrize("body", [b"[]", b"", b"not json", b"\xff"])
def test_persistent_create_reuses_work_item_response_validation(
    client: AzureDevOpsRestClient, opener: _Opener, body: bytes
) -> None:
    opener.response = _Response(body=body)

    with pytest.raises(AzureDevOpsResponseError):
        client.create_work_item(_candidate(), personal_access_token="secret-pat")


def test_persistent_create_preserves_http_failure_without_retry(
    client: AzureDevOpsRestClient, opener: _Opener
) -> None:
    opener.response = _Response(status=409)

    with pytest.raises(AzureDevOpsHttpError) as error:
        client.create_work_item(_candidate(), personal_access_token="secret-pat")

    assert error.value.status == 409
    assert len(opener.calls) == 1


def test_persistent_create_preserves_transport_failure_without_retry(
    client: AzureDevOpsRestClient, opener: _Opener
) -> None:
    opener.response = URLError("offline")

    with pytest.raises(AzureDevOpsTransportError):
        client.create_work_item(_candidate(), personal_access_token="secret-pat")

    assert len(opener.calls) == 1


@pytest.mark.parametrize("work_item_type", tuple(WorkItemType))
def test_looks_up_work_item_ids_with_the_exact_wiql_endpoint_contract(
    client: AzureDevOpsRestClient,
    opener: _Opener,
    work_item_type: WorkItemType,
) -> None:
    candidate = _candidate(work_item_type)
    opener.response = _Response(body=b'{"workItems":[{"id":17}]}')

    assert client.lookup_work_item_ids(candidate, personal_access_token="secret-pat") == (17,)

    request, _ = opener.calls[0]
    assert request.get_method() == "POST"
    assert request.full_url == (
        "https://dev.azure.com/example%20organization/Example%20Project/"
        "_apis/wit/wiql?%24top=2&api-version=7.1"
    )
    assert request.get_header("Content-type") == "application/json"
    assert request.get_header("Accept") == "application/json"
    assert json.loads(request.data.decode("utf-8")) == {
        "query": (
            "SELECT [System.Id]\n"
            "FROM WorkItems\n"
            "WHERE [System.TeamProject] = @project\n"
            f"  AND [System.WorkItemType] = '{work_item_type.value}'\n"
            f"  AND [Custom.BacklogGeneratorSourceIdentity] = '{candidate.source_identity}'"
        )
    }
    assert len(opener.calls) == 1
    assert "/_apis/wit/workitems/" not in request.full_url


@pytest.mark.parametrize(
    ("work_items", "expected"),
    [
        ([], ()),
        ([{"id": 1}], (1,)),
        ([{"id": 1}, {"id": 2}], (1, 2)),
        ([{"id": 1}, {"id": 2}, {"id": 3}], (1, 2, 3)),
    ],
)
def test_returns_wiql_ids_as_immutable_lookup_evidence(
    client: AzureDevOpsRestClient,
    opener: _Opener,
    work_items: list[dict[str, int]],
    expected: tuple[int, ...],
) -> None:
    opener.response = _Response(body=json.dumps({"workItems": work_items}).encode())

    result = client.lookup_work_item_ids(_candidate(), personal_access_token="secret-pat")

    assert result == expected
    assert isinstance(result, tuple)


@pytest.mark.parametrize(
    "source_identity",
    [
        None,
        "",
        "adbg:source-id:v1:sha256:" + "A" * 64,
        "adbg:source-id:v1:sha256:" + "a" * 63,
        "adbg:source-id:v1:sha256:" + "a" * 64 + "' OR 1=1",
    ],
)
def test_rejects_invalid_source_identity_before_wiql_transmission(
    client: AzureDevOpsRestClient,
    opener: _Opener,
    source_identity: object,
) -> None:
    with pytest.raises(ValueError, match="source identity marker"):
        client.lookup_work_item_ids(
            _candidate(source_identity=source_identity),  # type: ignore[arg-type]
            personal_access_token="secret-pat",
        )

    assert opener.calls == []


def test_rejects_an_unsupported_work_item_type_before_wiql_transmission(
    client: AzureDevOpsRestClient, opener: _Opener
) -> None:
    with pytest.raises(ValueError, match="supported WorkItemType"):
        client.lookup_work_item_ids(
            _candidate("User Story"),  # type: ignore[arg-type]
            personal_access_token="secret-pat",
        )

    assert opener.calls == []


@pytest.mark.parametrize(
    "work_items",
    [
        [{"id": 1}, {"id": 1}],
        [{}],
        [{"id": None}],
        [{"id": "1"}],
        [{"id": 1.0}],
        [{"id": True}],
        [1],
    ],
)
def test_rejects_malformed_wiql_work_item_entries(
    client: AzureDevOpsRestClient, opener: _Opener, work_items: list[object]
) -> None:
    opener.response = _Response(body=json.dumps({"workItems": work_items}).encode())

    with pytest.raises(AzureDevOpsResponseError):
        client.lookup_work_item_ids(_candidate(), personal_access_token="secret-pat")


@pytest.mark.parametrize("body", [b"{}", b'{"workItems":null}', b'{"workItems":{}}', b"[]"])
def test_rejects_malformed_wiql_response_shape(
    client: AzureDevOpsRestClient, opener: _Opener, body: bytes
) -> None:
    opener.response = _Response(body=body)

    with pytest.raises(AzureDevOpsResponseError):
        client.lookup_work_item_ids(_candidate(), personal_access_token="secret-pat")


def _work_item_response(**additional_properties: object) -> dict[str, object]:
    response: dict[str, object] = {
        "id": 17,
        "rev": 3,
        "fields": {
            "System.TeamProject": "Canonical Project",
            "System.WorkItemType": "Epic",
            "Custom.BacklogGeneratorSourceIdentity": "adbg:source-id:v1:sha256:" + "a" * 64,
        },
    }
    response.update(additional_properties)
    return response


def _relationship_state_response(
    child_work_item_id: int = 17,
    revision: object = 3,
    **additional_properties: object,
) -> dict[str, object]:
    response: dict[str, object] = {"id": child_work_item_id, "rev": revision}
    response.update(additional_properties)
    return response


def _reverse_relation(parent_work_item_id: int) -> dict[str, str]:
    return {
        "rel": "System.LinkTypes.Hierarchy-Reverse",
        "url": (
            "https://dev.azure.com/example%20organization/_apis/wit/workItems/"
            f"{parent_work_item_id}"
        ),
    }


def test_retrieves_work_item_evidence_with_the_exact_get_endpoint_contract(
    client: AzureDevOpsRestClient, opener: _Opener
) -> None:
    opener.response = _Response(body=json.dumps(_work_item_response()).encode())

    result = client.retrieve_work_item(17, personal_access_token="secret-pat")

    assert result == AzureDevOpsWorkItem(
        id=17,
        revision=3,
        project_name="Canonical Project",
        work_item_type="Epic",
        source_identity="adbg:source-id:v1:sha256:" + "a" * 64,
    )
    request, _ = opener.calls[0]
    assert request.get_method() == "GET"
    assert request.full_url == (
        "https://dev.azure.com/example%20organization/Example%20Project/"
        "_apis/wit/workitems/17?fields=System.TeamProject%2CSystem.WorkItemType%2C"
        "Custom.BacklogGeneratorSourceIdentity&api-version=7.1"
    )
    assert request.get_header("Accept") == "application/json"
    assert request.get_header("Content-type") is None
    assert request.data is None
    assert len(opener.calls) == 1
    assert "/wiql" not in request.full_url
    assert "/workitems/Epic" not in request.full_url
    assert "/relations" not in request.full_url
    with pytest.raises(AttributeError):
        result.id = 18  # type: ignore[misc]


@pytest.mark.parametrize("work_item_id", [0, -1])
def test_does_not_apply_undocumented_work_item_id_positivity_validation(
    client: AzureDevOpsRestClient, opener: _Opener, work_item_id: int
) -> None:
    opener.response = _Response(body=json.dumps(_work_item_response()).encode())

    client.retrieve_work_item(work_item_id, personal_access_token="secret-pat")

    request, _ = opener.calls[0]
    assert f"/workitems/{work_item_id}?fields=" in request.full_url


@pytest.mark.parametrize("work_item_id", [True, "17", 17.0, None])
def test_rejects_non_integer_work_item_ids_before_transmission(
    client: AzureDevOpsRestClient, opener: _Opener, work_item_id: object
) -> None:
    with pytest.raises(ValueError, match="numeric Work Item ID"):
        client.retrieve_work_item(  # type: ignore[arg-type]
            work_item_id, personal_access_token="secret-pat"
        )

    assert opener.calls == []


@pytest.mark.parametrize("body", [b"[]", b'"work item"', b"1", b"null"])
def test_rejects_non_object_work_item_response(
    client: AzureDevOpsRestClient, opener: _Opener, body: bytes
) -> None:
    opener.response = _Response(body=body)

    with pytest.raises(AzureDevOpsResponseError, match="JSON object"):
        client.retrieve_work_item(17, personal_access_token="secret-pat")


@pytest.mark.parametrize(
    ("property_name", "value"),
    [
        ("id", None),
        ("id", "17"),
        ("id", 17.0),
        ("id", True),
        ("rev", None),
        ("rev", "3"),
        ("rev", 3.0),
        ("rev", True),
    ],
)
def test_rejects_missing_or_malformed_work_item_numeric_evidence(
    client: AzureDevOpsRestClient,
    opener: _Opener,
    property_name: str,
    value: object,
) -> None:
    response = _work_item_response()
    response.pop(property_name)
    opener.response = _Response(body=json.dumps(response).encode())

    with pytest.raises(AzureDevOpsResponseError, match="numeric"):
        client.retrieve_work_item(17, personal_access_token="secret-pat")

    response = _work_item_response(**{property_name: value})
    opener.response = _Response(body=json.dumps(response).encode())

    with pytest.raises(AzureDevOpsResponseError, match="numeric"):
        client.retrieve_work_item(17, personal_access_token="secret-pat")


@pytest.mark.parametrize("fields", [None, [], "fields"])
def test_rejects_missing_or_malformed_work_item_fields(
    client: AzureDevOpsRestClient, opener: _Opener, fields: object
) -> None:
    response = _work_item_response()
    response.pop("fields")
    opener.response = _Response(body=json.dumps(response).encode())

    with pytest.raises(AzureDevOpsResponseError, match="fields object"):
        client.retrieve_work_item(17, personal_access_token="secret-pat")

    response = _work_item_response(fields=fields)
    opener.response = _Response(body=json.dumps(response).encode())

    with pytest.raises(AzureDevOpsResponseError, match="fields object"):
        client.retrieve_work_item(17, personal_access_token="secret-pat")


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("System.TeamProject", None),
        ("System.TeamProject", 1),
        ("System.WorkItemType", None),
        ("System.WorkItemType", 1),
        ("Custom.BacklogGeneratorSourceIdentity", None),
        ("Custom.BacklogGeneratorSourceIdentity", 1),
    ],
)
def test_rejects_missing_or_non_string_required_work_item_fields(
    client: AzureDevOpsRestClient,
    opener: _Opener,
    field_name: str,
    value: object,
) -> None:
    response = _work_item_response()
    fields = response["fields"]
    assert isinstance(fields, dict)
    fields.pop(field_name)
    opener.response = _Response(body=json.dumps(response).encode())

    with pytest.raises(AzureDevOpsResponseError, match="string field"):
        client.retrieve_work_item(17, personal_access_token="secret-pat")

    response = _work_item_response()
    fields = response["fields"]
    assert isinstance(fields, dict)
    fields[field_name] = value
    opener.response = _Response(body=json.dumps(response).encode())

    with pytest.raises(AzureDevOpsResponseError, match="string field"):
        client.retrieve_work_item(17, personal_access_token="secret-pat")


def test_ignores_unknown_work_item_response_properties_and_fields(
    client: AzureDevOpsRestClient, opener: _Opener
) -> None:
    response = _work_item_response(unexpected="ignored")
    fields = response["fields"]
    assert isinstance(fields, dict)
    fields["System.Title"] = "Ignored title"
    opener.response = _Response(body=json.dumps(response).encode())

    assert client.retrieve_work_item(17, personal_access_token="secret-pat").id == 17


def test_work_item_get_preserves_a_404_http_failure(
    client: AzureDevOpsRestClient, opener: _Opener
) -> None:
    opener.response = _Response(status=404)

    with pytest.raises(AzureDevOpsHttpError) as error:
        client.retrieve_work_item(17, personal_access_token="secret-pat")

    assert error.value.status == 404
    assert len(opener.calls) == 1
