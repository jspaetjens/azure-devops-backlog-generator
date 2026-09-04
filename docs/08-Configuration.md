# Azure DevOps Backlog Generator

# Configuration Specification

> *This document defines the configuration architecture, configuration parameters and validation rules for Version 1.0 of the Azure DevOps Backlog Generator.*

**Version:** 1.9

**Status:** Draft

**Last Updated:** 2026-09-04

**Target Release:** v1.0.0

**License:** MIT

**Author:** Jack Spaetjens

---

# Version History

| Version | Date | Status | Author | Description |
|----------|------------|-------------------|-----------------|------------------------------------------------|
| 0.1 | 2026-08-04 | Draft | Jack Spaetjens | Initial Configuration Specification. |
| 1.0 | 2026-08-04 | Approved Baseline | Jack Spaetjens | Initial approved Configuration Specification baseline. |
| 1.1 | 2026-08-20 | Approved Baseline | Jack Spaetjens | Documented the approved Version 1.0 configuration mechanism and identified the pending parameter schema and CLI argument name. |
| 1.2 | 2026-08-20 | Approved Baseline | Jack Spaetjens | Documented the approved CLI configuration-file contract. |
| 1.3 | 2026-08-20 | Approved Baseline | Jack Spaetjens | Documented the approved complete Version 1.0 external configuration schema. |
| 1.4 | 2026-08-20 | Approved Baseline | Jack Spaetjens | Clarified the Azure DevOps Services-only configuration scope for Version 1.0. |
| 1.5 | 2026-08-21 | Approved Baseline | Jack Spaetjens | Clarified the dedicated backlog-input source-directory contract. |
| 1.6 | 2026-08-21 | Approved Baseline | Jack Spaetjens | Standardised the Approval section to remain valid across Draft and Approved Baseline states. |
| 1.7 | 2026-08-23 | Approved Baseline | Jack Spaetjens | Aligned the Version 1.0 process exit-status boundary with the approved REST operational contract. |
| 1.8 | 2026-08-27 | Approved Baseline | Jack Spaetjens | Defined the Version 1.0 configuration bootstrap template convention. |
| 1.9 | 2026-09-04 | Draft | Jack Spaetjens | Defined approved but unimplemented Slice-6 runtime file-logging configuration and bootstrap semantics. |

---

# Table of Contents

- [Azure DevOps Backlog Generator](#azure-devops-backlog-generator)
- [Configuration Specification](#configuration-specification)
- [Version History](#version-history)
- [Table of Contents](#table-of-contents)
- [1. Introduction](#1-introduction)
- [2. Purpose](#2-purpose)
- [3. Configuration Objectives](#3-configuration-objectives)
- [4. Configuration Principles](#4-configuration-principles)
- [5. Configuration Structure](#5-configuration-structure)
  - [5.1 Configuration File Format](#51-configuration-file-format)
  - [5.2 Configuration File Selection and Discovery](#52-configuration-file-selection-and-discovery)
  - [5.3 Configuration Sources and Precedence](#53-configuration-sources-and-precedence)
  - [5.4 Relative Path Resolution](#54-relative-path-resolution)
  - [5.5 Configuration File Composition](#55-configuration-file-composition)
- [6. Configuration Parameters](#6-configuration-parameters)
  - [6.1 Application](#61-application)
  - [6.2 Azure DevOps](#62-azure-devops)
  - [6.3 Documentation](#63-documentation)
  - [6.4 Logging](#64-logging)
  - [6.5 Generator](#65-generator)
  - [6.6 Complete External Schema](#66-complete-external-schema)
- [7. Configuration Validation](#7-configuration-validation)
- [8. Environment Variables](#8-environment-variables)
- [9. Default Values](#9-default-values)
- [10. Configuration Traceability](#10-configuration-traceability)
- [11. Approval](#11-approval)


---

# 1. Introduction

This document defines the configuration architecture for Version 1.0 of the Azure DevOps Backlog Generator.

It describes the configuration model, supported configuration parameters and validation rules required for application execution while maintaining alignment with the approved documentation baseline.

The Configuration Specification establishes the configuration contract between the application and its operating environment.

---

# 2. Purpose

The purpose of this document is to define how the application shall be configured.

The Configuration Specification establishes the standards for configuration management, validation and application behaviour while ensuring configuration remains separate from the application source code.

---

# 3. Configuration Objectives

Version 1.0 shall achieve the following configuration objectives:

- Provide a centralised configuration model.
- Separate configuration from application logic.
- Support secure handling of sensitive information.
- Validate configuration before application execution.
- Support environment-specific configuration.
- Maintain complete traceability to the approved documentation baseline.

---

# 4. Configuration Principles

Configuration management shall follow the following principles:

- Configuration shall remain external to the application source code.
- Sensitive information shall not be stored in source code.
- Configuration shall be validated before execution.
- Required configuration shall be explicitly defined.
- Optional configuration shall provide sensible defaults.
- Configuration shall support maintainability and extensibility.
- Configuration changes shall remain traceable to the approved documentation baseline.

---

# 5. Configuration Structure

Version 1.0 shall use a structured configuration model to separate application settings from implementation logic.

The configuration shall be organised into the following logical sections:

- Application
- Azure DevOps
- Documentation
- Logging
- Generator

Each configuration section shall contain only settings related to its defined responsibility.

The configuration structure shall support future expansion without requiring modification of existing configuration sections.

## 5.1 Configuration File Format

Version 1.0 shall use TOML as the supported configuration-file format.

Configuration files shall be parsed using the Python standard-library `tomllib` module. No third-party TOML parser dependency is required.

## 5.2 Configuration File Selection and Discovery

The canonical configuration-file path shall be `config/config.toml`.

`config/config.toml` shall be local, user-specific runtime configuration and shall not be
tracked by the repository. The repository shall provide the tracked bootstrap template
`config/config.example.toml`. Before use, users shall copy that template to
`config/config.toml` and edit the required non-secret values for their target environment.
The template shall contain no secrets. A PAT shall remain exclusively supplied through
`AZDO_PAT`.

The optional `--config-file` CLI option shall supply an explicit configuration-file path. No short alias shall be supported in Version 1.0. The option shall accept exactly one file-path operand.

When `--config-file` is supplied, the application shall use the supplied file and shall not perform default configuration discovery. When `--config-file` is omitted, the application shall use `config/config.toml`.

A relative path supplied through `--config-file` shall resolve relative to the process current working directory. This rule applies only to the `--config-file` operand. Relative paths defined inside the selected TOML configuration file shall resolve relative to the directory containing that file, as defined in Section 5.4.

Supplying `--config-file` more than once shall be a CLI usage error. A missing or empty `--config-file` operand shall be a CLI usage error and shall not fall back to `config/config.toml`.

The selected configuration file shall not be required to use a `.toml` filename extension. Its validity shall be determined by accessibility and valid TOML content.

The `--config-file` option shall identify a configuration file only. It shall not accept a PAT or other secret. PAT input shall remain exclusively through `AZDO_PAT`.

A missing explicitly supplied configuration file shall be an immediate configuration error. A missing default `config/config.toml` file shall also be a configuration error.

## 5.3 Configuration Sources and Precedence

The effective configuration precedence shall be:

1. Supported CLI values.
2. Supported environment-variable values.
3. TOML configuration-file values.
4. Documented defaults.

Only settings explicitly documented as supporting CLI or environment-variable overrides may be overridden through those sources. Supported CLI values shall override supported environment-variable values. Supported environment-variable values shall override TOML configuration-file values. TOML configuration-file values shall override documented defaults.

## 5.4 Relative Path Resolution

Relative paths defined inside a configuration file shall resolve relative to the directory containing the loaded configuration file.

## 5.5 Configuration File Composition

Exactly one TOML configuration file shall be selected for each execution.

Configuration overlays and configuration-file merging are not supported in Version 1.0.

---

# 6. Configuration Parameters

The Version 1.0 external configuration schema consists only of the parameters defined in this section. No other TOML keys are permitted.

## 6.1 Application

Version 1.0 defines no externally configurable application parameters. The `[application]` TOML table may be omitted. An explicitly present empty `[application]` table is equivalent to omission. Any key inside `[application]` shall be an unknown-key validation error.

Application name and application version shall be derived from application or package metadata. Dry-run behaviour is not supported in Version 1.0.

This fulfils the Architecture's logical Application configuration category without introducing an external application option that is not approved for Version 1.0.

## 6.2 Azure DevOps

The `[azure_devops]` TOML table shall contain the following required parameters:

| Key | Purpose | TOML type | Default | Environment override | CLI override |
|-----|---------|-----------|---------|----------------------|--------------|
| `organization` | Identifies the target Azure DevOps Services organisation. | String | None | Not supported | Not supported |
| `project` | Identifies the target Azure DevOps project. | String | None | Not supported | Not supported |

`azure_devops.organization` and `azure_devops.project` shall be validated as strings that are not empty after trimming whitespace for validation purposes. This version shall not define stricter Azure DevOps character or naming rules. The original configured values shall not be normalised unless separately approved.

Version 1.0 does not support Azure DevOps Server connection configuration. No Version 1.0 configuration parameters exist for server hostname, port, collection, base URL or deployment type.

There shall be no PAT TOML key. A PAT shall be supplied exclusively through `AZDO_PAT`, shall be required at runtime and shall not be accepted through the CLI. An absent or whitespace-only `AZDO_PAT` value shall be a configuration error. Whitespace inspection shall be used only to validate presence; the original secret value shall not be modified.

Azure DevOps API version shall not be an external Version 1.0 configuration parameter. It shall be an application-controlled API-contract constant that users cannot override through TOML, environment variables or CLI. The concrete value shall be selected and documented in the API Specification before REST-client implementation.

## 6.3 Documentation

The `[documentation]` TOML table shall contain the following required parameter:

| Key | Purpose | TOML type | Default | Environment override | CLI override |
|-----|---------|-----------|---------|----------------------|--------------|
| `source_directory` | Identifies the dedicated directory containing approved backlog-input Markdown documents governed by `09-Documentation-Input.md`. | String representing a filesystem path | None | Not supported | Not supported |

`documentation.source_directory` shall not be empty. Relative values shall resolve according to the configuration-file-relative path rule in Section 5.4. The resolved path shall exist, be a directory and be readable.

`documentation.source_directory` shall not identify the general project documentation directory or a mixed directory containing arbitrary Markdown documents. It shall identify only the dedicated backlog-input directory governed by `09-Documentation-Input.md`.

This section defines filesystem validity only. Documentation-content validation remains the responsibility of documentation processing.

## 6.4 Logging

The `[logging]` TOML table may omit either or both of the following optional parameters:

| Key | Purpose | TOML type | Default | Environment override | CLI override |
|-----|---------|-----------|---------|----------------------|--------------|
| `level` | Defines the minimum logging severity. | String | `INFO` | Not supported | Not supported |
| `log_directory` | Defines the directory used for file logging. | String representing a filesystem path | `../logs` | Not supported | Not supported |

`logging.level` shall accept the following values case-insensitively: `DEBUG`, `INFO`, `WARNING`, `ERROR` and `CRITICAL`. The effective runtime value shall be normalised to uppercase. Any other value shall be a configuration validation error. Treatment of surrounding whitespace is not defined by this specification and remains an implementation-detail decision.

`logging.log_directory` shall resolve according to the configuration-file-relative path rule in Section 5.4. With the canonical `config/config.toml` file, the default `../logs` resolves to the root-level `logs/` directory.

If the resolved logging directory does not exist, the application shall create it before file logging begins. If creation fails, execution shall stop with a configuration or startup error. If the path exists, it shall be a directory and the effective directory shall be usable and writable for logging. Failure to use the resolved directory shall stop execution with a configuration or startup error. The application shall not silently fall back to another logging directory.

Parent-directory creation semantics for arbitrary nested logging paths are not defined by this specification.

The approved but unimplemented Application/Run Slice 6 runtime logger shall use no additional configuration key.
After successful configuration loading and validation, it shall configure the application logger threshold and file
handler threshold from the effective uppercase `logging.level`. Controlled process-termination category events shall
use `CRITICAL`, which remains visible for every allowed threshold. The logger shall write UTF-8 append records to
`azure-devops-backlog-generator.log` inside the validated `logging.log_directory`; rotation, retention, console
logging, filename, format and bootstrap-location configuration are not supported.

Configured file logging can begin only after configuration load and validation make the validated logging directory
available and runtime logger initialisation succeeds. A configuration loading or validation failure necessarily
precedes runtime logger initialisation and shall retain the approved fixed `Configuration error.` stderr-only process
boundary and exact integer `1`; it shall make no configured-file log attempt and use no fallback/default/bootstrap
logger or alternate destination. If valid configuration is followed by runtime file-logger initialisation failure,
the application shall raise the dedicated controlled `ApplicationLoggingError`; it shall not be treated as
`ConfigurationError`, and no file-log event or fallback destination shall be used. Later controlled failures may use
the controlled-failure emission contract; a secondary file-write failure preserves the primary controlled failure.

## 6.5 Generator

Version 1.0 defines no externally configurable generator parameters. The `[generator]` TOML table may be omitted. An explicitly present empty `[generator]` table is equivalent to omission. Any key inside `[generator]` shall be an unknown-key validation error.

Parent-child relationship creation, duplicate prevention and repeatability, traceability, and the supported work-item types Epic, Feature, Product Backlog Item and Task shall remain fixed mandatory Version 1.0 behaviour. `overwrite_existing`, `create_relationships` and equivalent generator toggles shall not be exposed as configuration parameters.

## 6.6 Complete External Schema

The only permitted Version 1.0 TOML keys are:

```toml
[azure_devops]
organization = "..."
project = "..."

[documentation]
source_directory = "..."

[logging]
level = "..."
log_directory = "..."
```

The `[application]` and `[generator]` tables are optional and, when present, shall be empty. No other TOML keys are permitted.

---

# 7. Configuration Validation

Configuration shall be validated before application execution.

Validation shall verify:

- Presence of all required configuration values.
- Correct data types.
- Valid configuration formats.
- Valid file and directory references.
- Valid Azure DevOps configuration.
- Internal configuration consistency.
- Absence of unknown configuration sections and keys.
- Presence and non-empty validation of `AZDO_PAT` without exposing or altering its secret value.
- Valid logging-level values.
- Valid documentation source-directory and logging-directory references.

Application execution shall not continue when required configuration validation fails.

Meaningful validation errors shall be presented through the application's approved process boundary. Configuration
loading and validation failures occur before configured runtime logging can initialise, so they remain stderr-only;
no configured-file log attempt or fallback logging destination is authorised.

Unknown configuration sections or keys shall be validation errors. Validation shall fail before application execution when unknown configuration sections or keys are present.

A PAT TOML key and all other keys not permitted by Section 6.6 shall be validation errors.

Configuration errors, including missing configuration files, shall provide clear error messages without exposing sensitive information.

The following selected configuration-file conditions shall be configuration errors:

- The selected file does not exist.
- The selected path is not a file, including a directory path.
- The selected file cannot be read.
- The selected file contains malformed TOML.

CLI usage errors and configuration errors shall be reported through the application's error handling. Version 1.0 defines the fixed process exit-status mapping: controlled successful execution shall exit with status `0`, and controlled application failure shall exit with status `1`. This mapping is application behaviour and shall not be configurable through TOML, environment variables or CLI configuration options. A differentiated numeric exit-code taxonomy beyond `0` and `1` remains future work.

---

# 8. Environment Variables

`AZDO_PAT` shall be the only supported Version 1.0 environment configuration input. No TOML setting shall be overridden through another environment variable.

The PAT shall not be stored in the canonical configuration file. It shall be supplied through `AZDO_PAT` and shall not be accepted through the CLI.

Environment variables shall take precedence over TOML configuration-file values where explicitly supported, subject to the precedence defined in Section 5.3. In Version 1.0, `AZDO_PAT` is the only supported environment input.

Sensitive information supplied through environment variables shall not be written to application logs. PATs and other secrets shall never be logged, exposed in validation messages, exceptions or diagnostics. Secret values shall be masked whenever provenance or diagnostics are reported.

---

# 9. Default Values

Version 1.0 shall provide default values for optional configuration parameters where appropriate. Defaults are permitted only where they are explicitly defined in this Configuration Specification.

Default values shall:

- Reduce required configuration.
- Promote consistent application behaviour.
- Support predictable execution.
- Simplify initial deployment.

Required configuration parameters shall not define default values or receive undocumented implicit defaults.

The Version 1.0 defaults are:

| Parameter | Default value |
|-----------|---------------|
| `logging.level` | `INFO` |
| `logging.log_directory` | `../logs` |

No other Version 1.0 configuration parameter has a default value.

---

# 10. Configuration Traceability

This Configuration Specification defines the configuration model supporting implementation of the approved documentation baseline.

Traceability shall be maintained between:

- Product Requirements Document
- Software Architecture Document
- Development Roadmap
- Development Standards
- API Specification
- Testing Strategy
- Release Management
- Configuration Specification
- Azure DevOps Backlog
- Source Code
- Test Documentation

Configuration implementation shall remain aligned with the approved documentation baseline and shall not introduce functionality that is not traceable to an approved requirement.

---

# 11. Approval

Approval of a document version requires:

- Completion of the editorial review.
- Approval of that document version.
- Creation of the corresponding Approved Baseline.
- Commit to the project repository using the agreed Git workflow.

The document metadata and Version History record whether the current version has completed this approval process.

Subsequent modifications shall follow the established documentation governance process and be recorded through Version History.
