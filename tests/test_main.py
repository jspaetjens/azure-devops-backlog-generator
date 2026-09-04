"""Tests for Application/Run composition."""

import logging
from io import StringIO
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


@pytest.fixture(autouse=True)
def _reset_runtime_logging() -> None:
    main_module._deactivate_runtime_logging()
    yield
    main_module._deactivate_runtime_logging()


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
    ("error", "expected_stderr"),
    [
        (ConfigurationFileError(), "Configuration error.\n"),
        (DocumentationReadError(), "Documentation processing error.\n"),
        (AzureDevOpsTransportError(), "Azure DevOps error.\n"),
        (
            SourceIdentityValidationError(SourceIdentityValidationState.DUPLICATE_LOGICAL_IDENTITY),
            "Source identity validation error.\n",
        ),
        (ExistingWorkItemResolutionError(), "Existing work item resolution error.\n"),
        (
            ConflictingReusedChildRelationshipError(
                2,
                1,
                ReusedChildRelationshipClassification.CONFLICTING,
                AzureDevOpsWorkItemRelationshipState(revision=1, reverse_parent_ids=(3,)),
            ),
            "Conflicting reused child relationship error.\n",
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
    expected_stderr: str,
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
    assert captured.err == expected_stderr
    assert caplog.records == []


def test_run_process_does_not_render_controlled_failure_detail(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    caplog: pytest.LogCaptureFixture,
) -> None:
    detail = (
        "SYNTHETIC_PAT_DO_NOT_RENDER "
        "--config-file=C:\\secret\\config.toml https://example.invalid/private"
    )

    calls = 0

    def failing_main() -> None:
        nonlocal calls
        calls += 1
        raise ConfigurationFileError(detail)

    monkeypatch.setattr(main_module, "main", failing_main)

    assert main_module.run_process() == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "Configuration error.\n"
    assert detail not in captured.err
    assert calls == 1
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


def _configuration(source_directory: Path, log_directory: Path = Path("logs")) -> Configuration:
    return Configuration(
        azure_devops=AzureDevOpsConfig(organization="organization", project="project"),
        documentation=DocumentationConfig(source_directory=source_directory),
        logging=LoggingConfig(level="INFO", log_directory=log_directory),
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
    tmp_path: Path,
) -> None:
    arguments = ["--config-file", "config/config.toml"]
    configuration = _configuration(Path("documentation-input"), tmp_path)
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
    tmp_path: Path,
) -> None:
    arguments = ["--config-file", "config/config.toml"]
    configuration = _configuration(Path("documentation-input"), tmp_path)
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


@pytest.mark.parametrize("level", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
def test_runtime_logger_uses_validated_settings_and_records_critical_failures(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
    level: str,
) -> None:
    configuration = _configuration(tmp_path, tmp_path)
    configuration = Configuration(
        azure_devops=configuration.azure_devops,
        documentation=configuration.documentation,
        logging=LoggingConfig(level=level, log_directory=tmp_path),
        personal_access_token=configuration.personal_access_token,
    )

    monkeypatch.setattr(main_module, "load_configuration_from_cli", lambda _: configuration)

    def fail(_: Configuration) -> None:
        raise DocumentationReadError(
            "SYNTHETIC_PAT_DO_NOT_RENDER C:\\secret\\config.toml https://example.invalid/private"
        )

    monkeypatch.setattr(main_module, "coordinate_application_run", fail)
    log_file = tmp_path / "azure-devops-backlog-generator.log"
    log_file.write_text("prior invocation\n", encoding="utf-8")

    assert main_module.run_process() == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "Documentation processing error.\n"

    logger = logging.getLogger("azure_devops_backlog_generator")
    owned_handlers = [
        handler
        for handler in logger.handlers
        if getattr(handler, main_module._OWNED_HANDLER_ATTRIBUTE, False)
    ]
    assert logger.level == getattr(logging, level)
    assert logger.propagate is False
    assert len(owned_handlers) == 1
    assert owned_handlers[0].level == getattr(logging, level)
    assert owned_handlers[0].encoding == "utf-8"
    assert owned_handlers[0].baseFilename == str(tmp_path / "azure-devops-backlog-generator.log")
    assert owned_handlers[0].formatter is not None
    assert owned_handlers[0].formatter._fmt == "%(asctime)s %(levelname)s %(name)s %(message)s"
    assert owned_handlers[0].formatter.datefmt == "%Y-%m-%dT%H:%M:%S"
    contents = log_file.read_text(encoding="utf-8")
    assert contents.startswith("prior invocation\n")
    assert contents.count("Documentation processing error.") == 1
    assert " CRITICAL azure_devops_backlog_generator Documentation processing error.\n" in contents
    assert "SYNTHETIC_PAT_DO_NOT_RENDER" not in contents
    assert "C:\\secret\\config.toml" not in captured.out + captured.err + contents
    assert "https://example.invalid/private" not in captured.out + captured.err + contents


@pytest.mark.parametrize(
    ("error", "message"),
    [
        (AzureDevOpsTransportError("detail"), "Azure DevOps error."),
        (
            SourceIdentityValidationError(SourceIdentityValidationState.DUPLICATE_LOGICAL_IDENTITY),
            "Source identity validation error.",
        ),
        (ExistingWorkItemResolutionError("detail"), "Existing work item resolution error."),
        (
            ConflictingReusedChildRelationshipError(
                2,
                1,
                ReusedChildRelationshipClassification.CONFLICTING,
                AzureDevOpsWorkItemRelationshipState(revision=1, reverse_parent_ids=(3,)),
            ),
            "Conflicting reused child relationship error.",
        ),
    ],
)
def test_each_reachable_post_initialisation_controlled_failure_is_logged_once(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
    error: Exception,
    message: str,
) -> None:
    configuration = _configuration(tmp_path, tmp_path)
    monkeypatch.setattr(main_module, "load_configuration_from_cli", lambda _: configuration)
    monkeypatch.setattr(
        main_module,
        "coordinate_application_run",
        lambda _: (_ for _ in ()).throw(error),
    )

    assert main_module.run_process() == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == f"{message}\n"
    contents = (tmp_path / "azure-devops-backlog-generator.log").read_text(encoding="utf-8")
    assert contents.count(message) == 1
    assert f" CRITICAL azure_devops_backlog_generator {message}\n" in contents


def test_successful_run_is_silent_and_writes_no_lifecycle_record(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    configuration = _configuration(tmp_path, tmp_path)
    monkeypatch.setattr(main_module, "load_configuration_from_cli", lambda _: configuration)
    monkeypatch.setattr(main_module, "coordinate_application_run", lambda _: None)

    assert main_module.run_process() == 0
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""
    assert (tmp_path / "azure-devops-backlog-generator.log").read_text(encoding="utf-8") == ""


def test_configuration_error_has_no_file_event_and_deactivates_a_stale_handler(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    configuration = _configuration(tmp_path, tmp_path)
    calls = 0

    def load(_: object) -> Configuration:
        nonlocal calls
        calls += 1
        if calls == 1:
            return configuration
        raise ConfigurationFileError("SYNTHETIC_PAT_DO_NOT_RENDER C:\\secret\\config.toml")

    monkeypatch.setattr(main_module, "load_configuration_from_cli", load)
    monkeypatch.setattr(main_module, "coordinate_application_run", lambda _: None)

    assert main_module.run_process() == 0
    first_handler = main_module._ACTIVE_LOG_HANDLER
    assert first_handler is not None
    assert main_module.run_process() == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "Configuration error.\n"
    assert first_handler.stream is None
    assert main_module._ACTIVE_LOG_HANDLER is None
    assert (tmp_path / "azure-devops-backlog-generator.log").read_text(encoding="utf-8") == ""


def test_logging_initialisation_failure_is_a_controlled_application_error(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    configuration = _configuration(tmp_path, tmp_path)

    class FailingHandler:
        def __init__(self, *args: object, **kwargs: object) -> None:
            raise OSError("SYNTHETIC_PAT_DO_NOT_RENDER")

    monkeypatch.setattr(main_module, "load_configuration_from_cli", lambda _: configuration)
    monkeypatch.setattr(main_module, "_ApplicationFileHandler", FailingHandler)

    assert main_module.run_process() == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "Application logging error.\n"
    assert "SYNTHETIC_PAT_DO_NOT_RENDER" not in captured.err
    assert main_module._ACTIVE_LOG_HANDLER is None
    assert not (tmp_path / "azure-devops-backlog-generator.log").exists()


def test_partial_logging_initialisation_failure_closes_the_created_handler(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    configuration = _configuration(tmp_path, tmp_path)
    created_handlers: list[logging.FileHandler] = []
    original_handler = main_module._ApplicationFileHandler

    class TrackingHandler(original_handler):
        def __init__(self, *args: object, **kwargs: object) -> None:
            super().__init__(*args, **kwargs)
            created_handlers.append(self)

    def fail_to_attach(_: logging.Handler) -> None:
        raise OSError("SYNTHETIC_PAT_DO_NOT_RENDER")

    monkeypatch.setattr(main_module, "load_configuration_from_cli", lambda _: configuration)
    monkeypatch.setattr(main_module, "_ApplicationFileHandler", TrackingHandler)
    with monkeypatch.context() as initialisation_patch:
        initialisation_patch.setattr(main_module._LOGGER, "addHandler", fail_to_attach)
        result = main_module.run_process()

    assert result == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "Application logging error.\n"
    assert "SYNTHETIC_PAT_DO_NOT_RENDER" not in captured.err
    assert len(created_handlers) == 1
    assert created_handlers[0].stream is None
    assert main_module._ACTIVE_LOG_HANDLER is None
    assert not any(
        getattr(handler, main_module._OWNED_HANDLER_ATTRIBUTE, False)
        for handler in main_module._LOGGER.handlers
    )


def test_controlled_event_bypasses_non_owned_handler_on_the_named_logger(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    configuration = _configuration(tmp_path, tmp_path)
    stream = StringIO()

    class TrackingHandler(logging.StreamHandler):
        closed = False

        def close(self) -> None:
            self.closed = True
            super().close()

    named_handler = TrackingHandler(stream)
    root_handler = TrackingHandler(StringIO())
    main_module._LOGGER.addHandler(named_handler)
    logging.getLogger().addHandler(root_handler)
    monkeypatch.setattr(main_module, "load_configuration_from_cli", lambda _: configuration)
    monkeypatch.setattr(
        main_module,
        "coordinate_application_run",
        lambda _: (_ for _ in ()).throw(DocumentationReadError("detail")),
    )

    try:
        assert main_module.run_process() == 1
        captured = capsys.readouterr()
        assert captured.out == ""
        assert captured.err == "Documentation processing error.\n"
        assert named_handler in main_module._LOGGER.handlers
        assert named_handler.closed is False
        assert stream.getvalue() == ""
        assert root_handler in logging.getLogger().handlers
        assert root_handler.closed is False
        assert main_module._LOGGER.propagate is False
        contents = (tmp_path / "azure-devops-backlog-generator.log").read_text(encoding="utf-8")
        assert contents.count("Documentation processing error.") == 1
        assert (
            " CRITICAL azure_devops_backlog_generator Documentation processing error.\n"
            in contents
        )
    finally:
        main_module._LOGGER.removeHandler(named_handler)
        named_handler.close()
        logging.getLogger().removeHandler(root_handler)
        root_handler.close()


def test_secondary_log_write_failure_preserves_the_primary_controlled_failure(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    configuration = _configuration(tmp_path, tmp_path)
    attempts = 0

    class FailingStream:
        def write(self, _: str) -> int:
            raise OSError("write failure")

        def flush(self) -> None:
            pass

        def close(self) -> None:
            pass

    monkeypatch.setattr(main_module, "load_configuration_from_cli", lambda _: configuration)
    monkeypatch.setattr(
        main_module,
        "coordinate_application_run",
        lambda _: (_ for _ in ()).throw(DocumentationReadError("detail")),
    )
    def replace_stream() -> None:
        assert main_module._ACTIVE_LOG_HANDLER is not None
        assert main_module._ACTIVE_LOG_HANDLER.stream is not None
        main_module._ACTIVE_LOG_HANDLER.stream.close()
        main_module._ACTIVE_LOG_HANDLER.stream = FailingStream()
        original_handle = main_module._ACTIVE_LOG_HANDLER.handle

        def handle(record: logging.LogRecord) -> bool:
            nonlocal attempts
            attempts += 1
            return original_handle(record)

        monkeypatch.setattr(main_module._ACTIVE_LOG_HANDLER, "handle", handle)

    original_run = main_module.coordinate_application_run

    def fail_with_stream(configuration_received: Configuration) -> None:
        replace_stream()
        original_run(configuration_received)

    monkeypatch.setattr(main_module, "coordinate_application_run", fail_with_stream)

    assert main_module.run_process() == 1
    captured = capsys.readouterr()
    assert attempts == 1
    assert captured.out == ""
    assert captured.err == "Documentation processing error.\n"
    assert "Logging error" not in captured.err


def test_repeated_invocations_replace_only_owned_handlers_and_do_not_duplicate_records(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    configuration = _configuration(tmp_path, tmp_path)
    unrelated_logger = logging.getLogger("unrelated.application.logger")
    unrelated = logging.StreamHandler()
    root_handler = logging.StreamHandler()
    raise_exceptions = logging.raiseExceptions
    unrelated_logger.addHandler(unrelated)
    logging.getLogger().addHandler(root_handler)
    monkeypatch.setattr(main_module, "load_configuration_from_cli", lambda _: configuration)
    monkeypatch.setattr(
        main_module,
        "coordinate_application_run",
        lambda _: (_ for _ in ()).throw(DocumentationReadError("detail")),
    )

    assert main_module.run_process() == 1
    first_handler = main_module._ACTIVE_LOG_HANDLER
    assert main_module.run_process() == 1
    second_handler = main_module._ACTIVE_LOG_HANDLER
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "Documentation processing error.\nDocumentation processing error.\n"
    assert first_handler is not second_handler
    assert first_handler is not None and first_handler.stream is None
    assert unrelated in unrelated_logger.handlers
    assert root_handler in logging.getLogger().handlers
    assert logging.raiseExceptions is raise_exceptions
    contents = (tmp_path / "azure-devops-backlog-generator.log").read_text(encoding="utf-8")
    assert contents.count("Documentation processing error.") == 2
    logging.getLogger().removeHandler(root_handler)
    unrelated_logger.removeHandler(unrelated)


def test_unexpected_exception_remains_unlogged_after_logger_initialisation(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    configuration = _configuration(tmp_path, tmp_path)
    error = _SentinelError()
    monkeypatch.setattr(main_module, "load_configuration_from_cli", lambda _: configuration)
    monkeypatch.setattr(
        main_module,
        "coordinate_application_run",
        lambda _: (_ for _ in ()).throw(error),
    )

    with pytest.raises(_SentinelError) as raised:
        main_module.run_process()

    assert raised.value is error
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""
    assert (tmp_path / "azure-devops-backlog-generator.log").read_text(encoding="utf-8") == ""
