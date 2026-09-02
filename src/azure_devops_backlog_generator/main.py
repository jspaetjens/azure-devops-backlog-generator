"""Application-level composition for a configured backlog-generation run."""

import sys
from collections.abc import Sequence

from azure_devops_backlog_generator.azure_devops.rest_client import AzureDevOpsRestClient
from azure_devops_backlog_generator.config.loader import load_configuration_from_cli
from azure_devops_backlog_generator.config.models import Configuration
from azure_devops_backlog_generator.documentation.processor import DocumentationProcessor
from azure_devops_backlog_generator.generator.orchestration import (
    coordinate_generator_orchestration,
)


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
