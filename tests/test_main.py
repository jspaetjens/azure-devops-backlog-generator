"""Tests for Application/Run Slice-1 composition."""

from pathlib import Path

import pytest

import azure_devops_backlog_generator.main as main_module
from azure_devops_backlog_generator.config.models import (
    AzureDevOpsConfig,
    Configuration,
    DocumentationConfig,
    LoggingConfig,
)

_SYNTHETIC_PAT = "slice-1-synthetic-pat"


class _SentinelError(Exception):
    pass


def _configuration(source_directory: Path) -> Configuration:
    return Configuration(
        azure_devops=AzureDevOpsConfig(organization="organization", project="project"),
        documentation=DocumentationConfig(source_directory=source_directory),
        logging=LoggingConfig(level="INFO", log_directory=Path("logs")),
        personal_access_token=_SYNTHETIC_PAT,
    )


def test_composes_the_configured_application_run_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source_directory = Path("documentation-input")
    configuration = _configuration(source_directory)
    hierarchy = object()
    rest_client = object()
    events: list[str] = []

    class Processor:
        def __init__(self) -> None:
            events.append("processor-init")

        def process(self, directory: Path) -> object:
            assert directory is source_directory
            events.append("process")
            return hierarchy

    def construct_rest_client(organization: str, project: str) -> object:
        assert organization == "organization"
        assert project == "project"
        events.append("rest-client-init")
        return rest_client

    def coordinate_generator(
        received_hierarchy: object,
        received_rest_client: object,
        *,
        personal_access_token: str,
    ) -> None:
        assert received_hierarchy is hierarchy
        assert received_rest_client is rest_client
        assert personal_access_token is configuration.personal_access_token
        events.append("generator")

    monkeypatch.setattr(main_module, "DocumentationProcessor", Processor)
    monkeypatch.setattr(main_module, "AzureDevOpsRestClient", construct_rest_client)
    monkeypatch.setattr(main_module, "coordinate_generator_orchestration", coordinate_generator)

    assert main_module.coordinate_application_run(configuration) is None
    assert events == ["processor-init", "process", "rest-client-init", "generator"]
    assert all(_SYNTHETIC_PAT not in event for event in events)


def test_propagates_documentation_failure_without_constructing_other_collaborators(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    error = _SentinelError()
    events: list[str] = []

    class Processor:
        def process(self, directory: Path) -> object:
            events.append("process")
            raise error

    def unexpected_rest_client(*args: object) -> None:
        events.append("rest-client-init")
        raise AssertionError("REST client must not be constructed")

    def unexpected_generator(*args: object, **kwargs: object) -> None:
        events.append("generator")
        raise AssertionError("Generator must not be invoked")

    monkeypatch.setattr(main_module, "DocumentationProcessor", Processor)
    monkeypatch.setattr(main_module, "AzureDevOpsRestClient", unexpected_rest_client)
    monkeypatch.setattr(main_module, "coordinate_generator_orchestration", unexpected_generator)

    with pytest.raises(_SentinelError) as raised:
        main_module.coordinate_application_run(_configuration(Path("documentation-input")))

    assert raised.value is error
    assert events == ["process"]


def test_propagates_rest_client_construction_failure_without_invoking_generator(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    error = _SentinelError()
    events: list[str] = []

    class Processor:
        def process(self, directory: Path) -> object:
            events.append("process")
            return object()

    def construct_rest_client(*args: object) -> None:
        events.append("rest-client-init")
        raise error

    def unexpected_generator(*args: object, **kwargs: object) -> None:
        events.append("generator")
        raise AssertionError("Generator must not be invoked")

    monkeypatch.setattr(main_module, "DocumentationProcessor", Processor)
    monkeypatch.setattr(main_module, "AzureDevOpsRestClient", construct_rest_client)
    monkeypatch.setattr(main_module, "coordinate_generator_orchestration", unexpected_generator)

    with pytest.raises(_SentinelError) as raised:
        main_module.coordinate_application_run(_configuration(Path("documentation-input")))

    assert raised.value is error
    assert events == ["process", "rest-client-init"]


def test_propagates_generator_failure_without_retry_or_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    error = _SentinelError()
    hierarchy = object()
    rest_client = object()
    events: list[str] = []

    class Processor:
        def process(self, directory: Path) -> object:
            events.append("process")
            return hierarchy

    def construct_rest_client(*args: object) -> object:
        events.append("rest-client-init")
        return rest_client

    def coordinate_generator(*args: object, **kwargs: object) -> None:
        events.append("generator")
        raise error

    monkeypatch.setattr(main_module, "DocumentationProcessor", Processor)
    monkeypatch.setattr(main_module, "AzureDevOpsRestClient", construct_rest_client)
    monkeypatch.setattr(main_module, "coordinate_generator_orchestration", coordinate_generator)

    with pytest.raises(_SentinelError) as raised:
        main_module.coordinate_application_run(_configuration(Path("documentation-input")))

    assert raised.value is error
    assert events == ["process", "rest-client-init", "generator"]
