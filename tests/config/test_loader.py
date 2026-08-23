"""Tests for Version 1.0 TOML configuration loading and validation."""

from pathlib import Path

import pytest

from azure_devops_backlog_generator.config.exceptions import (
    ConfigurationFileError,
    ConfigurationUsageError,
    ConfigurationValidationError,
)
from azure_devops_backlog_generator.config.loader import (
    load_configuration,
    load_configuration_from_cli,
)


def _write_configuration(tmp_path: Path, content: str) -> Path:
    path = tmp_path / "config.toml"
    path.write_text(content, encoding="utf-8")
    return path


def _valid_toml() -> str:
    return """[azure_devops]
organization = "organization"
project = "project"

[documentation]
source_directory = "input"
"""


def _environment() -> dict[str, str]:
    return {"AZDO_PAT": "runtime-secret"}


def test_loads_defaults_and_resolves_paths_from_the_selected_file(tmp_path: Path) -> None:
    (tmp_path / "input").mkdir()
    path = _write_configuration(tmp_path, _valid_toml())

    configuration = load_configuration(path, environment=_environment())

    assert configuration.azure_devops.organization == "organization"
    assert configuration.azure_devops.project == "project"
    assert configuration.documentation.source_directory == (tmp_path / "input").resolve()
    assert configuration.logging.level == "INFO"
    assert configuration.logging.log_directory == (tmp_path.parent / "logs").resolve()
    assert configuration.logging.log_directory.is_dir()


def test_uses_the_canonical_default_configuration_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    configuration_directory = tmp_path / "config"
    configuration_directory.mkdir()
    (configuration_directory / "input").mkdir()
    _write_configuration(configuration_directory, _valid_toml())
    monkeypatch.chdir(tmp_path)

    configuration = load_configuration(environment=_environment())

    expected_source_directory = (configuration_directory / "input").resolve()
    assert configuration.documentation.source_directory == expected_source_directory


def test_accepts_empty_application_and_generator_tables(tmp_path: Path) -> None:
    (tmp_path / "input").mkdir()
    path = _write_configuration(tmp_path, _valid_toml() + "\n[application]\n\n[generator]\n")

    assert load_configuration(path, environment=_environment()).azure_devops.project == "project"


@pytest.mark.parametrize(
    ("addition", "message"),
    [
        ("\n[application]\ndry_run = true\n", "Unknown configuration key"),
        ("\n[generator]\noverwrite_existing = true\n", "Unknown configuration key"),
        ('\n[extra]\nvalue = "x"\n', "Unknown configuration section"),
    ],
)
def test_rejects_unsupported_toml_configuration(
    tmp_path: Path, addition: str, message: str
) -> None:
    (tmp_path / "input").mkdir()
    path = _write_configuration(tmp_path, _valid_toml() + addition)

    with pytest.raises(ConfigurationValidationError, match=message) as error:
        load_configuration(path, environment=_environment())

    assert "secret" not in str(error.value)


def test_rejects_a_pat_toml_key_without_exposing_its_value(tmp_path: Path) -> None:
    (tmp_path / "input").mkdir()
    path = _write_configuration(
        tmp_path,
        _valid_toml().replace(
            'project = "project"', 'project = "project"\npersonal_access_token = "secret"'
        ),
    )

    with pytest.raises(ConfigurationValidationError, match="Unknown configuration key") as error:
        load_configuration(path, environment=_environment())

    assert "secret" not in str(error.value)


@pytest.mark.parametrize(
    "toml",
    [
        '[azure_devops]\nproject = "project"\n[documentation]\nsource_directory = "input"\n',
        (
            '[azure_devops]\norganization = "   "\nproject = "project"\n'
            '[documentation]\nsource_directory = "input"\n'
        ),
        (
            '[azure_devops]\norganization = "organization"\nproject = 1\n'
            '[documentation]\nsource_directory = "input"\n'
        ),
        (
            '[azure_devops]\norganization = "organization"\nproject = "project"\n'
            '[documentation]\nsource_directory = "missing"\n'
        ),
    ],
)
def test_rejects_invalid_required_values(tmp_path: Path, toml: str) -> None:
    (tmp_path / "input").mkdir()
    path = _write_configuration(tmp_path, toml)

    with pytest.raises(ConfigurationValidationError):
        load_configuration(path, environment=_environment())


@pytest.mark.parametrize("pat", [None, "", "  "])
def test_requires_a_non_empty_runtime_pat(tmp_path: Path, pat: str | None) -> None:
    (tmp_path / "input").mkdir()
    path = _write_configuration(tmp_path, _valid_toml())

    with pytest.raises(ConfigurationValidationError, match="AZDO_PAT") as error:
        load_configuration(path, environment={} if pat is None else {"AZDO_PAT": pat})

    if pat:
        assert pat not in str(error.value)


def test_normalizes_logging_level_and_validates_its_type(tmp_path: Path) -> None:
    (tmp_path / "input").mkdir()
    path = _write_configuration(tmp_path, _valid_toml() + '\n[logging]\nlevel = "warning"\n')

    assert load_configuration(path, environment=_environment()).logging.level == "WARNING"

    path = _write_configuration(tmp_path, _valid_toml() + "\n[logging]\nlevel = 1\n")
    with pytest.raises(ConfigurationValidationError, match="logging.level"):
        load_configuration(path, environment=_environment())


def test_reports_selected_file_failures_without_reading_a_directory(tmp_path: Path) -> None:
    with pytest.raises(ConfigurationFileError, match="does not exist"):
        load_configuration(tmp_path / "missing.toml", environment=_environment())
    with pytest.raises(ConfigurationFileError, match="identify a file"):
        load_configuration(tmp_path, environment=_environment())


def test_reports_malformed_toml(tmp_path: Path) -> None:
    path = _write_configuration(tmp_path, "[azure_devops\n")

    with pytest.raises(ConfigurationFileError, match="malformed TOML"):
        load_configuration(path, environment=_environment())


def test_loads_the_explicit_cli_configuration_file(tmp_path: Path) -> None:
    (tmp_path / "input").mkdir()
    path = _write_configuration(tmp_path, _valid_toml()).with_suffix(".configuration")
    (tmp_path / "config.toml").replace(path)

    assert load_configuration_from_cli(["--config-file", str(path)], environment=_environment())


@pytest.mark.parametrize(
    "arguments",
    [
        ["--config-file"],
        ["--config-file", ""],
        ["--config-file", "--another-option"],
        ["--config-file="],
        ["--config-file", "first.toml", "--config-file", "second.toml"],
    ],
)
def test_rejects_invalid_config_file_cli_usage(arguments: list[str]) -> None:
    with pytest.raises(ConfigurationUsageError):
        load_configuration_from_cli(arguments, environment=_environment())
