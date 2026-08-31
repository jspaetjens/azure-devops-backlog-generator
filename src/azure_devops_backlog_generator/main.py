"""Application-level composition for a configured backlog-generation run."""

from azure_devops_backlog_generator.azure_devops.rest_client import AzureDevOpsRestClient
from azure_devops_backlog_generator.config.models import Configuration
from azure_devops_backlog_generator.documentation.processor import DocumentationProcessor
from azure_devops_backlog_generator.generator.orchestration import (
    coordinate_generator_orchestration,
)


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
