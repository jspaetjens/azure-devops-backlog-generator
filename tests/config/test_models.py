"""Unit tests for the configuration data models."""

from azure_devops_backlog_generator.config.models import (
    ApplicationConfig,
    AzureDevOpsConfig,
    Configuration,
    DocumentationConfig,
    GeneratorConfig,
    LoggingConfig,
)


def test_application_config() -> None:
    config = ApplicationConfig(
        name="test-application",
        version="1.0.0",
        dry_run=True,
    )

    assert config.name == "test-application"
    assert config.version == "1.0.0"
    assert config.dry_run is True


def test_azure_devops_config() -> None:
    config = AzureDevOpsConfig(
        organization="test-organization",
        project="test-project",
        personal_access_token="test-token",
    )

    assert config.organization == "test-organization"
    assert config.project == "test-project"
    assert config.personal_access_token == "test-token"


def test_documentation_config() -> None:
    config = DocumentationConfig(
        source_directory="docs",
    )

    assert config.source_directory == "docs"


def test_logging_config() -> None:
    config = LoggingConfig(
        level="INFO",
        log_directory="logs",
    )

    assert config.level == "INFO"
    assert config.log_directory == "logs"


def test_generator_config() -> None:
    config = GeneratorConfig(
        overwrite_existing=False,
        create_relationships=True,
    )

    assert config.overwrite_existing is False
    assert config.create_relationships is True


def test_configuration() -> None:
    application = ApplicationConfig(
        name="test-application",
        version="1.0.0",
        dry_run=True,
    )

    azure_devops = AzureDevOpsConfig(
        organization="test-organization",
        project="test-project",
        personal_access_token="test-token",
    )

    documentation = DocumentationConfig(
        source_directory="docs",
    )

    logging = LoggingConfig(
        level="INFO",
        log_directory="logs",
    )

    generator = GeneratorConfig(
        overwrite_existing=False,
        create_relationships=True,
    )

    config = Configuration(
        application=application,
        azure_devops=azure_devops,
        documentation=documentation,
        logging=logging,
        generator=generator,
    )

    assert config.application is application
    assert config.azure_devops is azure_devops
    assert config.documentation is documentation
    assert config.logging is logging
    assert config.generator is generator