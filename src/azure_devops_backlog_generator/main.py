"""Application-level composition for a configured backlog-generation run."""

import logging
import sys
from collections.abc import Sequence
from pathlib import Path

from azure_devops_backlog_generator.azure_devops.exceptions import AzureDevOpsRestClientError
from azure_devops_backlog_generator.azure_devops.rest_client import AzureDevOpsRestClient
from azure_devops_backlog_generator.config.exceptions import ConfigurationError
from azure_devops_backlog_generator.config.loader import load_configuration_from_cli
from azure_devops_backlog_generator.config.models import Configuration
from azure_devops_backlog_generator.documentation.exceptions import DocumentationProcessingError
from azure_devops_backlog_generator.documentation.processor import DocumentationProcessor
from azure_devops_backlog_generator.generator.identity import SourceIdentityValidationError
from azure_devops_backlog_generator.generator.orchestration import (
    coordinate_generator_orchestration,
)
from azure_devops_backlog_generator.generator.relationships import (
    ConflictingReusedChildRelationshipError,
)
from azure_devops_backlog_generator.generator.resolution import ExistingWorkItemResolutionError

_LOGGER_NAME = "azure_devops_backlog_generator"
_LOG_FILE_NAME = "azure-devops-backlog-generator.log"
_OWNED_HANDLER_ATTRIBUTE = "_azure_devops_backlog_generator_owned_handler"
_LOGGER = logging.getLogger(_LOGGER_NAME)
_ACTIVE_LOG_HANDLER: logging.Handler | None = None


class ApplicationLoggingError(Exception):
    """Raised when runtime file logging cannot be initialised."""


class _ApplicationFileHandler(logging.FileHandler):
    """File handler that keeps its own write failures silent."""

    def handleError(self, record: logging.LogRecord) -> None:
        """Suppress diagnostics for this application's secondary write failures."""


def _deactivate_runtime_logging() -> None:
    """Remove and close only application-owned handlers from a prior invocation."""
    global _ACTIVE_LOG_HANDLER

    for handler in tuple(_LOGGER.handlers):
        if getattr(handler, _OWNED_HANDLER_ATTRIBUTE, False):
            _LOGGER.removeHandler(handler)
            handler.close()
    _ACTIVE_LOG_HANDLER = None


def _initialise_runtime_logging(configuration: Configuration) -> None:
    """Create the current invocation's configured application-owned file handler."""
    global _ACTIVE_LOG_HANDLER

    handler: logging.Handler | None = None
    try:
        handler = _ApplicationFileHandler(
            Path(configuration.logging.log_directory) / _LOG_FILE_NAME,
            mode="a",
            encoding="utf-8",
        )
        setattr(handler, _OWNED_HANDLER_ATTRIBUTE, True)
        level = getattr(logging, configuration.logging.level)
        handler.setLevel(level)
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s %(name)s %(message)s",
                datefmt="%Y-%m-%dT%H:%M:%S",
            )
        )
        _LOGGER.setLevel(level)
        _LOGGER.propagate = False
        _LOGGER.addHandler(handler)
    except (OSError, ValueError):
        if handler is not None:
            handler.close()
        raise ApplicationLoggingError from None
    _ACTIVE_LOG_HANDLER = handler


def _controlled_failure_message(
    error: ConfigurationError
    | DocumentationProcessingError
    | AzureDevOpsRestClientError
    | SourceIdentityValidationError
    | ExistingWorkItemResolutionError
    | ConflictingReusedChildRelationshipError
    | ApplicationLoggingError,
) -> str:
    """Return the fixed category-only message for one controlled failure."""
    if isinstance(error, ConfigurationError):
        return "Configuration error."
    if isinstance(error, DocumentationProcessingError):
        return "Documentation processing error."
    if isinstance(error, AzureDevOpsRestClientError):
        return "Azure DevOps error."
    if isinstance(error, SourceIdentityValidationError):
        return "Source identity validation error."
    if isinstance(error, ExistingWorkItemResolutionError):
        return "Existing work item resolution error."
    if isinstance(error, ConflictingReusedChildRelationshipError):
        return "Conflicting reused child relationship error."
    return "Application logging error."


def _emit_controlled_failure(message: str) -> None:
    """Attempt one current-invocation controlled-failure file event."""
    handler = _ACTIVE_LOG_HANDLER
    if handler is not None:
        record = _LOGGER.makeRecord(
            _LOGGER.name,
            logging.CRITICAL,
            "",
            0,
            message,
            (),
            None,
        )
        handler.handle(record)


def run_process() -> int:
    """Run the application and map controlled failures to a process outcome."""
    try:
        main()
    except (
        ConfigurationError,
        DocumentationProcessingError,
        AzureDevOpsRestClientError,
        SourceIdentityValidationError,
        ExistingWorkItemResolutionError,
        ConflictingReusedChildRelationshipError,
        ApplicationLoggingError,
    ) as error:
        message = _controlled_failure_message(error)
        _emit_controlled_failure(message)
        _render_controlled_failure(message)
        return 1
    return 0


def _render_controlled_failure(message: str) -> None:
    """Write the fixed stderr message for one controlled application failure."""
    print(message, file=sys.stderr)


def main() -> None:
    """Coordinate application bootstrap with process arguments."""
    coordinate_application_bootstrap(sys.argv[1:])


def coordinate_application_bootstrap(arguments: Sequence[str]) -> None:
    """Load configuration and coordinate the configured application run."""
    _deactivate_runtime_logging()
    configuration = load_configuration_from_cli(arguments)
    _initialise_runtime_logging(configuration)
    coordinate_application_run(configuration)


def coordinate_application_run(configuration: Configuration) -> None:
    """Process configured documentation and coordinate backlog generation."""
    hierarchy = DocumentationProcessor().process(configuration.documentation.source_directory)
    rest_client = AzureDevOpsRestClient(
        configuration.azure_devops.organization,
        configuration.azure_devops.project,
    )
    coordinate_generator_orchestration(
        hierarchy,
        rest_client,
        personal_access_token=configuration.personal_access_token,
    )
