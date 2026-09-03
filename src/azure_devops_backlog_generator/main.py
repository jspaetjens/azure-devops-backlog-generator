"""Application-level composition for a configured backlog-generation run."""

import sys
from collections.abc import Sequence

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
    ) as error:
        _render_controlled_failure(error)
        return 1
    return 0


def _render_controlled_failure(
    error: ConfigurationError
    | DocumentationProcessingError
    | AzureDevOpsRestClientError
    | SourceIdentityValidationError
    | ExistingWorkItemResolutionError
    | ConflictingReusedChildRelationshipError,
) -> None:
    """Write the fixed stderr message for one controlled application failure."""
    if isinstance(error, ConfigurationError):
        message = "Configuration error."
    elif isinstance(error, DocumentationProcessingError):
        message = "Documentation processing error."
    elif isinstance(error, AzureDevOpsRestClientError):
        message = "Azure DevOps error."
    elif isinstance(error, SourceIdentityValidationError):
        message = "Source identity validation error."
    elif isinstance(error, ExistingWorkItemResolutionError):
        message = "Existing work item resolution error."
    else:
        message = "Conflicting reused child relationship error."
    print(message, file=sys.stderr)


def main() -> None:
    """Coordinate application bootstrap with process arguments."""
    coordinate_application_bootstrap(sys.argv[1:])


def coordinate_application_bootstrap(arguments: Sequence[str]) -> None:
    """Load configuration and coordinate the configured application run."""
    configuration = load_configuration_from_cli(arguments)
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
