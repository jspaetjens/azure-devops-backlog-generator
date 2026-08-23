"""Typed, effective configuration for the application."""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True, slots=True)
class AzureDevOpsConfig:
    """Azure DevOps Services identifiers from the configuration file."""

    organization: str
    project: str


@dataclass(frozen=True, slots=True)
class DocumentationConfig:
    """Resolved location of dedicated backlog-input documentation."""

    source_directory: Path


@dataclass(frozen=True, slots=True)
class LoggingConfig:
    """Effective file-logging settings."""

    level: str
    log_directory: Path


@dataclass(frozen=True, slots=True)
class Configuration:
    """Validated application configuration.

    The personal access token is runtime-only. It is intentionally omitted
    from the representation so it cannot be disclosed in diagnostics.
    """

    azure_devops: AzureDevOpsConfig
    documentation: DocumentationConfig
    logging: LoggingConfig
    personal_access_token: str = field(repr=False)
