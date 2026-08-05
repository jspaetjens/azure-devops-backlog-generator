"""
Configuration data models.

These models define the strongly typed configuration objects used
throughout the Azure DevOps Backlog Generator.

Configuration values are loaded by the configuration loader and
validated by the configuration validator before application startup.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class ApplicationConfig:
    """
    General application configuration.
    """

    name: str
    version: str
    dry_run: bool


@dataclass(slots=True)
class AzureDevOpsConfig:
    """
    Azure DevOps connection configuration.
    """

    organization: str
    project: str
    personal_access_token: str


@dataclass(slots=True)
class DocumentationConfig:
    """
    Documentation input configuration.
    """

    source_directory: str


@dataclass(slots=True)
class LoggingConfig:
    """
    Logging configuration.
    """

    level: str
    log_directory: str


@dataclass(slots=True)
class GeneratorConfig:
    """
    Backlog generator configuration.
    """

    overwrite_existing: bool
    create_relationships: bool


@dataclass(slots=True)
class Configuration:
    """
    Root configuration object.
    """

    application: ApplicationConfig
    azure_devops: AzureDevOpsConfig
    documentation: DocumentationConfig
    logging: LoggingConfig
    generator: GeneratorConfig