"""TOML configuration-file loading."""

import os
import tomllib
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from azure_devops_backlog_generator.config.exceptions import (
    ConfigurationFileError,
    ConfigurationUsageError,
)
from azure_devops_backlog_generator.config.models import Configuration
from azure_devops_backlog_generator.config.validator import validate_configuration

DEFAULT_CONFIGURATION_PATH = Path("config/config.toml")
PAT_ENVIRONMENT_VARIABLE = "AZDO_PAT"


def load_configuration(
    config_file: str | Path | None = None,
    *,
    environment: Mapping[str, str] | None = None,
) -> Configuration:
    """Load and validate exactly one TOML configuration file."""
    selected_path = _selected_path(config_file)
    raw_configuration = _read_toml(selected_path)
    values = os.environ if environment is None else environment
    return validate_configuration(
        raw_configuration,
        selected_path.parent,
        values.get(PAT_ENVIRONMENT_VARIABLE),
    )


def load_configuration_from_cli(
    arguments: Sequence[str],
    *,
    environment: Mapping[str, str] | None = None,
) -> Configuration:
    """Load configuration selected by the Version 1.0 CLI option."""
    return load_configuration(parse_config_file_argument(arguments), environment=environment)


def parse_config_file_argument(arguments: Sequence[str]) -> str | None:
    """Return the sole ``--config-file`` operand or the default selection."""
    config_file: str | None = None
    index = 0
    while index < len(arguments):
        argument = arguments[index]
        if argument == "--config-file":
            if config_file is not None:
                raise ConfigurationUsageError("--config-file may be supplied only once.")
            index += 1
            if index == len(arguments) or not arguments[index] or arguments[index].startswith("--"):
                raise ConfigurationUsageError("--config-file requires one non-empty file path.")
            config_file = arguments[index]
        elif argument.startswith("--config-file="):
            if config_file is not None:
                raise ConfigurationUsageError("--config-file may be supplied only once.")
            config_file = argument.removeprefix("--config-file=")
            if not config_file:
                raise ConfigurationUsageError("--config-file requires one non-empty file path.")
        else:
            raise ConfigurationUsageError(f"Unsupported configuration option: {argument}.")
        index += 1
    return config_file


def _selected_path(config_file: str | Path | None) -> Path:
    if config_file is None:
        return (Path.cwd() / DEFAULT_CONFIGURATION_PATH).resolve()
    if not str(config_file):
        raise ConfigurationFileError("The configuration-file path must not be empty.")
    path = Path(config_file)
    return (Path.cwd() / path).resolve() if not path.is_absolute() else path.resolve()


def _read_toml(path: Path) -> Mapping[str, Any]:
    if not path.exists():
        raise ConfigurationFileError(f"Configuration file does not exist: {path}.")
    if not path.is_file():
        raise ConfigurationFileError("The selected configuration path must identify a file.")
    try:
        with path.open("rb") as configuration_file:
            return tomllib.load(configuration_file)
    except PermissionError as error:
        raise ConfigurationFileError("Configuration file cannot be read.") from error
    except OSError as error:
        raise ConfigurationFileError("Configuration file cannot be read.") from error
    except tomllib.TOMLDecodeError as error:
        raise ConfigurationFileError("Configuration file contains malformed TOML.") from error
