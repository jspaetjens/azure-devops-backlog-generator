"""Validation helpers for the Version 1.0 TOML configuration schema."""

import os
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from azure_devops_backlog_generator.config.exceptions import ConfigurationValidationError
from azure_devops_backlog_generator.config.models import (
    AzureDevOpsConfig,
    Configuration,
    DocumentationConfig,
    LoggingConfig,
)

_ALLOWED_SECTIONS = frozenset(
    {"application", "azure_devops", "documentation", "logging", "generator"}
)
_SECTION_KEYS = {
    "application": frozenset(),
    "azure_devops": frozenset({"organization", "project"}),
    "documentation": frozenset({"source_directory"}),
    "logging": frozenset({"level", "log_directory"}),
    "generator": frozenset(),
}
_LOG_LEVELS = frozenset({"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"})


def validate_configuration(
    raw_configuration: Mapping[str, Any],
    configuration_directory: Path,
    personal_access_token: str | None,
) -> Configuration:
    """Validate raw TOML and return its resolved, effective configuration."""
    _validate_schema(raw_configuration)
    _validate_pat(personal_access_token)

    azure_devops = _required_table(raw_configuration, "azure_devops")
    documentation = _required_table(raw_configuration, "documentation")
    logging = _optional_table(raw_configuration, "logging")

    organization = _required_string(azure_devops, "azure_devops.organization")
    project = _required_string(azure_devops, "azure_devops.project")
    source_directory = _resolve_directory(
        _required_string(documentation, "documentation.source_directory"),
        configuration_directory,
        "documentation.source_directory",
        create=False,
    )
    level = _logging_level(logging.get("level", "INFO"))
    log_directory = _resolve_directory(
        _optional_string(logging, "log_directory", "../logs"),
        configuration_directory,
        "logging.log_directory",
        create=True,
    )

    return Configuration(
        azure_devops=AzureDevOpsConfig(organization=organization, project=project),
        documentation=DocumentationConfig(source_directory=source_directory),
        logging=LoggingConfig(level=level, log_directory=log_directory),
        personal_access_token=personal_access_token,
    )


def _validate_schema(raw_configuration: Mapping[str, Any]) -> None:
    unknown_sections = set(raw_configuration) - _ALLOWED_SECTIONS
    if unknown_sections:
        raise ConfigurationValidationError(
            f"Unknown configuration section: {_names(unknown_sections)}."
        )

    for section, allowed_keys in _SECTION_KEYS.items():
        if section not in raw_configuration:
            continue
        table = raw_configuration[section]
        if not isinstance(table, dict):
            raise ConfigurationValidationError(
                f"Configuration section [{section}] must be a TOML table."
            )
        unknown_keys = set(table) - allowed_keys
        if unknown_keys:
            raise ConfigurationValidationError(
                f"Unknown configuration key in [{section}]: {_names(unknown_keys)}."
            )


def _required_table(raw_configuration: Mapping[str, Any], name: str) -> Mapping[str, Any]:
    table = raw_configuration.get(name)
    if table is None:
        raise ConfigurationValidationError(f"Missing required configuration section [{name}].")
    return table


def _optional_table(raw_configuration: Mapping[str, Any], name: str) -> Mapping[str, Any]:
    return raw_configuration.get(name, {})


def _required_string(table: Mapping[str, Any], name: str) -> str:
    value = table.get(name.rsplit(".", maxsplit=1)[1])
    if type(value) is not str or not value.strip():
        raise ConfigurationValidationError(f"{name} must be a non-empty string.")
    return value


def _optional_string(table: Mapping[str, Any], key: str, default: str) -> str:
    value = table.get(key, default)
    if type(value) is not str:
        raise ConfigurationValidationError(f"logging.{key} must be a string.")
    return value


def _logging_level(value: Any) -> str:
    if type(value) is not str:
        raise ConfigurationValidationError("logging.level must be a string.")
    normalized = value.strip().upper()
    if normalized not in _LOG_LEVELS:
        raise ConfigurationValidationError(
            "logging.level must be DEBUG, INFO, WARNING, ERROR, or CRITICAL."
        )
    return normalized


def _resolve_directory(value: str, base_directory: Path, name: str, *, create: bool) -> Path:
    path = Path(value)
    resolved = (base_directory / path).resolve() if not path.is_absolute() else path.resolve()
    try:
        if create and not resolved.exists():
            resolved.mkdir()
    except OSError as error:
        raise ConfigurationValidationError(f"{name} could not be created.") from error

    if not resolved.is_dir():
        raise ConfigurationValidationError(f"{name} must identify a directory.")
    if not os.access(resolved, os.R_OK):
        raise ConfigurationValidationError(f"{name} must identify a readable directory.")
    if create and not os.access(resolved, os.W_OK):
        raise ConfigurationValidationError(f"{name} must identify a writable directory.")
    return resolved


def _validate_pat(personal_access_token: str | None) -> None:
    if type(personal_access_token) is not str or not personal_access_token.strip():
        raise ConfigurationValidationError("AZDO_PAT must be set to a non-empty value.")


def _names(values: set[str]) -> str:
    return ", ".join(sorted(values))
