# Azure DevOps Backlog Generator

# Configuration Specification

> *This document defines the configuration architecture, configuration parameters and validation rules for Version 1.0 of the Azure DevOps Backlog Generator.*

**Version:** 1.2

**Status:** Approved Baseline

**Last Updated:** 2026-08-20

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

The configuration shall define all application settings required for execution.

This specification establishes the configuration mechanism but does not yet define the complete parameter schema. Parameter-level definitions, including names, data types, required or optional status, and default values, remain pending project decisions except where already stated in this specification or the approved documentation baseline.

Configuration parameters shall include, where applicable:

- Application settings.
- Azure DevOps organisation.
- Azure DevOps project.
- Authentication configuration.
- Documentation location.
- Logging configuration.
- Generator options.

Each configuration parameter shall define:

- Name.
- Purpose.
- Data type.
- Required or optional status.
- Default value where applicable.

Configuration parameters shall remain consistent with the approved Software Architecture Document.

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

Application execution shall not continue when required configuration validation fails.

Meaningful validation errors shall be presented to the user and recorded through the application's logging mechanism.

Unknown configuration sections or keys shall be validation errors. Validation shall fail before application execution when unknown configuration sections or keys are present.

Configuration errors, including missing configuration files, shall provide clear error messages without exposing sensitive information.

The following selected configuration-file conditions shall be configuration errors:

- The selected file does not exist.
- The selected path is not a file, including a directory path.
- The selected file cannot be read.
- The selected file contains malformed TOML.

CLI usage errors and configuration errors shall be reported through the application's error handling. Numeric exit-status mapping remains part of the future CLI and error-handling contract.

---

# 8. Environment Variables

Version 1.0 shall support environment variables only for sensitive configuration values and overrides explicitly documented by this specification.

Environment variables may be used for:

- Azure DevOps Personal Access Token (PAT), through `AZDO_PAT`.
- Explicitly documented environment-specific configuration overrides.

The PAT shall not be stored in the canonical configuration file. It shall be supplied through `AZDO_PAT` and shall not be accepted through the CLI.

Environment variables shall take precedence over TOML configuration-file values where explicitly supported, subject to the precedence defined in Section 5.3.

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

Default values shall be documented and maintained as part of the approved configuration specification. No parameter-level default values are established by this version.

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

This document becomes part of the approved documentation baseline following:

- Completion of the editorial review.
- Approval of Version 1.2.
- Creation of the Version 1.2 Approved Baseline.
- Commit to the project repository using the agreed Git workflow.

Subsequent modifications shall follow the established documentation governance process and be recorded through Version History.
