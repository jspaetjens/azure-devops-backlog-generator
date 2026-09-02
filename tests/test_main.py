"""Tests for Application/Run composition."""

from pathlib import Path

import pytest

import azure_devops_backlog_generator.main as main_module
from azure_devops_backlog_generator.azure_devops.exceptions import AzureDevOpsTransportError
from azure_devops_backlog_generator.azure_devops.models import AzureDevOpsWorkItemRelationshipState
from azure_devops_backlog_generator.config.exceptions import ConfigurationFileError
from azure_devops_backlog_generator.config.models import (
    AzureDevOpsConfig,
    Configuration,
    DocumentationConfig,
    LoggingConfig,
)
from azure_devops_backlog_generator.documentation.exceptions import DocumentationReadError
from azure_devops_backlog_generator.generator.identity import (
    SourceIdentityValidationError,
    SourceIdentityValidationState,
)
from azure_devops_backlog_generator.generator.relationships import (
    ConflictingReusedChildRelationshipError,
    ReusedChildRelationshipClassification,
)
from azure_devops_backlog_generator.generator.resolution import ExistingWorkItemResolutionError

_SYNTHETIC_PAT = "slice-1-synthetic-pat"


class _SentinelError(Exception):
    pass


def test_run_process_returns_zero_after_one_successful_main_invocation(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    caplog: pytest.LogCaptureFixture,
) -> None:
    calls = 0

    def successful_main() -> None:
        nonlocal calls
        calls += 1

    monkeypatch.setattr(main_module, "main", successful_main)

    result = main_module.run_process()

    assert result == 0
    assert type(result) is int
    assert calls == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""
    assert caplog.records == []


@pytest.mark.parametrize(
    "error",
    [
        ConfigurationFileError(),
        DocumentationReadError(),
        AzureDevOpsTransportError(),
        SourceIdentityValidationError(SourceIdentityValidationState.DUPLICATE_LOGICAL_IDENTITY),
        ExistingWorkItemResolutionError(),
        ConflictingReusedChildRelationshipError(
            2,
            1,
            ReusedChildRelationshipClassification.CONFLICTING,
            AzureDevOpsWorkItemRelationshipState(revision=1, reverse_parent_ids=(3,)),
        ),
    ],
    ids=[
        "configuration",
        "documentation",
        "azure-devops-rest-client",
        "source-identity",
        "existing-work-item-resolution",
        "conflicting-reused-child-relationship",
    ],
)
def test_run_process_maps_each_controlled_failure_to_one(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    caplog: pytest.LogCaptureFixture,
    error: Exception,
) -> None:
    calls = 0

    def failing_main() -> None:
        nonlocal calls
        calls += 1
        raise error

    monkeypatch.setattr(main_module, "main", failing_main)

    result = main_module.run_process()

    assert result == 1
    assert type(result) is int
    assert calls == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""
    assert caplog.records == []


def test_run_process_propagates_the_exact_unexpected_exception(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    caplog: pytest.LogCaptureFixture,
) -> None:
    calls = 0
    error = _SentinelError()

    def failing_main() -> None:
        nonlocal calls
        calls += 1
        raise error

    monkeypatch.setattr(main_module, "main", failing_main)

    with pytest.raises(_SentinelError) as raised:
        main_module.run_process()

    assert raised.value is error
    assert calls == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""
    assert caplog.records == []


def _configuration(source_directory: Path) -> Configuration:
    return Configuration(
        azure_devops=AzureDevOpsConfig(organization="organization", project="project"),
        documentation=DocumentationConfig(source_directory=source_directory),
        logging=LoggingConfig(level="INFO", log_directory=Path("logs")),
        personal_access_token=_SYNTHETIC_PAT,
    )


def test_main_delegates_process_arguments_to_bootstrap_once(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    caplog: pytest.LogCaptureFixture,
) -> None:
    process_arguments = ["backlog-generator", "--config-file=config/custom.toml", "--literal"]
    expected_arguments = ["--config-file=config/custom.toml", "--literal"]
    received_arguments: list[list[str]] = []

    def coordinate_bootstrap(arguments_received: list[str]) -> None:
        received_arguments.append(arguments_received)

    monkeypatch.setattr(main_module.sys, "argv", process_arguments)
    monkeypatch.setattr(main_module, "coordinate_application_bootstrap", coordinate_bootstrap)

    assert main_module.main() is None
    assert received_arguments == [expected_arguments]
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""
    assert caplog.records == []


def test_main_propagates_bootstrap_failure_without_retry_or_exit_conversion(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    caplog: pytest.LogCaptureFixture,
) -> None:
    process_arguments = ["backlog-generator", "--config-file", "config/custom.toml"]
    expected_arguments = ["--config-file", "config/custom.toml"]
    error = _SentinelError()
    received_arguments: list[list[str]] = []

    def coordinate_bootstrap(arguments_received: list[str]) -> None:
        received_arguments.append(arguments_received)
        raise error

    monkeypatch.setattr(main_module.sys, "argv", process_arguments)
    monkeypatch.setattr(main_module, "coordinate_application_bootstrap", coordinate_bootstrap)

    with pytest.raises(_SentinelError) as raised:
        main_module.main()

    assert raised.value is error
    assert received_arguments == [expected_arguments]
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""
    assert caplog.records == []


def test_composes_application_bootstrap_with_the_exact_collaborator_values(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    arguments = ["--config-file", "config/config.toml"]
    configuration = _configuration(Path("documentation-input"))
    events: list[str] = []

    def load_configuration(arguments_received: object) -> Configuration:
        assert arguments_received is arguments
        events.append("loader")
        return configuration

    def coordinate_run(configuration_received: Configuration) -> None:
        assert configuration_received is configuration
        events.append("slice-1")

    monkeypatch.setattr(main_module, "load_configuration_from_cli", load_configuration)
    monkeypatch.setattr(main_module, "coordinate_application_run", coordinate_run)

    assert main_module.coordinate_application_bootstrap(arguments) is None
    assert events == ["loader", "slice-1"]
    assert all(_SYNTHETIC_PAT not in event for event in events)


def test_propagates_configuration_failure_without_invoking_slice_1(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    arguments = ["--config-file", "config/config.toml"]
    error = _SentinelError()
    events: list[str] = []

    def load_configuration(arguments_received: object) -> Configuration:
        assert arguments_received is arguments
        events.append("loader")
        raise error

    def unexpected_coordinate_run(*args: object) -> None:
        events.append("slice-1")
        raise AssertionError("Slice 1 must not be invoked")

    monkeypatch.setattr(main_module, "load_configuration_from_cli", load_configuration)
    monkeypatch.setattr(main_module, "coordinate_application_run", unexpected_coordinate_run)

    with pytest.raises(_SentinelError) as raised:
        main_module.coordinate_application_bootstrap(arguments)

    assert raised.value is error
    assert events == ["loader"]


def test_propagates_slice_1_failure_without_retry_or_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    arguments = ["--config-file", "config/config.toml"]
    configuration = _configuration(Path("documentation-input"))
    error = _SentinelError()
    events: list[str] = []

    def load_configuration(arguments_received: object) -> Configuration:
        assert arguments_received is arguments
        events.append("loader")
        return configuration

    def coordinate_run(configuration_received: Configuration) -> None:
        assert configuration_received is configuration
        events.append("slice-1")
        raise error

    monkeypatch.setattr(main_module, "load_configuration_from_cli", load_configuration)
    monkeypatch.setattr(main_module, "coordinate_application_run", coordinate_run)

    with pytest.raises(_SentinelError) as raised:
        main_module.coordinate_application_bootstrap(arguments)

    assert raised.value is error
    assert events == ["loader", "slice-1"]


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
