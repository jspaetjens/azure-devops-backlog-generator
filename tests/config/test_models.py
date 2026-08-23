"""Tests for effective configuration data models."""

from pathlib import Path

from azure_devops_backlog_generator.config.models import (
    AzureDevOpsConfig,
    Configuration,
    DocumentationConfig,
    LoggingConfig,
)


def test_configuration_keeps_the_runtime_pat_out_of_its_representation() -> None:
    configuration = Configuration(
        azure_devops=AzureDevOpsConfig(organization="organization", project="project"),
        documentation=DocumentationConfig(source_directory=Path("input")),
        logging=LoggingConfig(level="INFO", log_directory=Path("logs")),
        personal_access_token="secret-value",
    )

    assert "secret-value" not in repr(configuration)
    assert configuration.personal_access_token == "secret-value"


def test_obsolete_configuration_models_are_not_public() -> None:
    import azure_devops_backlog_generator.config.models as models

    assert not hasattr(models, "GeneratorConfig")
    assert not hasattr(models, "ApplicationConfig")
