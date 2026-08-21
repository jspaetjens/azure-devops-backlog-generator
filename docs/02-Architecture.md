# Azure DevOps Backlog Generator

# Software Architecture Document

> *This document defines the software architecture of the Azure DevOps Backlog Generator and describes the architectural principles, components and interactions that support Version 1.0.*

**Version:** 1.8

**Status:** Approved Baseline

**Last Updated:** 2026-08-21

**Target Release:** v1.0.0

**License:** MIT

**Author:** Jack Spaetjens

---

# Version History

| Version | Date | Status | Author | Description |
|----------|------------|-------------------|-----------------|------------------------------------------------|
| 0.1 | 2026-07-31 | Draft | Jack Spaetjens | Initial Software Architecture Document. |
| 1.0 | 2026-07-31 | Approved Baseline | Jack Spaetjens | Initial approved Software Architecture Document baseline. |
| 1.1 | 2026-08-20 | Approved Baseline | Jack Spaetjens | Clarified the Azure DevOps Services-only connection topology for Version 1.0. |
| 1.2 | 2026-08-20 | Approved Baseline | Jack Spaetjens | Defined architecture responsibilities and data flow for Scrum compatibility validation. |
| 1.3 | 2026-08-21 | Approved Baseline | Jack Spaetjens | Assigned the Documentation Input Specification contract to the Documentation Processor. |
| 1.4 | 2026-08-21 | Approved Baseline | Jack Spaetjens | Standardised the Approval section to remain valid across Draft and Approved Baseline states. |
| 1.5 | 2026-08-21 | Approved Baseline | Jack Spaetjens | Assigned fixed Description parsing, validation and rendering responsibilities to the Documentation Processor. |
| 1.6 | 2026-08-21 | Approved Baseline | Jack Spaetjens | Assigned Acceptance Criteria partitioning, validation and rendering responsibilities to the Documentation Processor. |
| 1.7 | 2026-08-21 | Approved Baseline | Jack Spaetjens | Assigned Tags partitioning, validation and prepared-field responsibilities to the Documentation Processor. |
| 1.8 | 2026-08-21 | Approved Baseline | Jack Spaetjens | Defined JSON Patch Create payload-construction ownership and transport responsibilities. |

---

# Table of Contents

- [Azure DevOps Backlog Generator](#azure-devops-backlog-generator)
- [Software Architecture Document](#software-architecture-document)
- [Version History](#version-history)
- [Table of Contents](#table-of-contents)
- [1. Introduction](#1-introduction)
- [2. Purpose](#2-purpose)
- [3. Architectural Goals](#3-architectural-goals)
- [4. Architectural Principles](#4-architectural-principles)
- [5. System Overview](#5-system-overview)
- [6. High-Level Architecture](#6-high-level-architecture)
- [7. Core Components](#7-core-components)
  - [7.1 Command-Line Interface](#71-command-line-interface)
  - [7.2 Configuration Manager](#72-configuration-manager)
  - [7.3 Documentation Processor](#73-documentation-processor)
  - [7.4 Backlog Generator](#74-backlog-generator)
  - [7.5 Azure DevOps REST Client](#75-azure-devops-rest-client)
  - [7.6 Logging Component](#76-logging-component)
  - [7.7 Error Handler](#77-error-handler)
- [8. Data Flow](#8-data-flow)
- [9. Configuration Management](#9-configuration-management)
- [10. Security Architecture](#10-security-architecture)
- [11. Error Handling](#11-error-handling)
- [12. Logging Strategy](#12-logging-strategy)
- [13. Extensibility](#13-extensibility)
- [14. Architecture Traceability](#14-architecture-traceability)
- [15. Approval](#15-approval)

---

# 1. Introduction

The Software Architecture Document describes the overall architecture of the Azure DevOps Backlog Generator.

It defines the structural organisation of the application, the interaction between its components and the architectural decisions that support Version 1.0.

The architecture provides the technical foundation for implementation while maintaining alignment with the approved Product Requirements Document.

---

# 2. Purpose

The purpose of this document is to define the architecture required to satisfy the approved functional and non-functional requirements.

The document provides the technical blueprint for implementation and establishes the architectural baseline from which development, testing and future enhancements shall be derived.

---

# 3. Architectural Goals

Version 1.0 shall achieve the following architectural goals:

- Provide a modular application architecture.
- Support reuse across multiple software projects.
- Separate configuration from application logic.
- Maintain clear separation of responsibilities between components.
- Support maintainability and extensibility.
- Enable automated testing.
- Support reliable communication with the Azure DevOps REST API.
- Maintain complete traceability to the approved documentation.

---

# 4. Architectural Principles

The architecture shall follow the following principles:

- Separation of Concerns.
- Single Responsibility Principle.
- Configuration over hard-coded values.
- Documentation-driven development.
- Reusability.
- Maintainability.
- Testability.
- Simplicity.
- Traceability.

---

# 5. System Overview

The Azure DevOps Backlog Generator is a command-line application written in Python.

The application reads approved project documentation and configuration, interprets the required backlog structure and communicates with Azure DevOps through the REST API to create and maintain work items.

The architecture is intentionally independent of any individual software project, allowing the application to be reused across multiple repositories.

---

# 6. High-Level Architecture

The Azure DevOps Backlog Generator is organised as a modular command-line application.

The architecture separates configuration management, documentation processing, backlog generation, Azure DevOps communication and application control into independent logical components.

The primary architectural layers are:

- Command-Line Interface (CLI)
- Configuration Management
- Documentation Processing
- Backlog Generation
- Azure DevOps REST Client
- Logging
- Error Handling

Each architectural layer has a clearly defined responsibility and communicates through well-defined interfaces, promoting maintainability, testability and future extensibility.

---

# 7. Core Components

Version 1.0 consists of the following logical components.

## 7.1 Command-Line Interface

The Command-Line Interface serves as the application's entry point.

Its responsibilities include:

- Starting the application.
- Reading command-line parameters.
- Initiating application execution.
- Returning execution status.

---

## 7.2 Configuration Manager

The Configuration Manager is responsible for loading and validating project configuration.

Responsibilities include:

- Reading configuration files.
- Validating required configuration.
- Providing configuration values to the application.

---

## 7.3 Documentation Processor

The Documentation Processor interprets approved backlog-input Markdown documents according to `09-Documentation-Input.md`.

Responsibilities include:

- Discovering backlog-input documents according to the approved source-directory contract.
- Parsing documents with `markdown-it-py==4.2.0` using `MarkdownIt("commonmark")`, with the approved fixed parser and default renderer configuration.
- Keeping the Markdown implementation, parser preset and renderer behaviour fixed rather than externally configurable.
- Validating parsed source nodes, including source structure, raw HTML, images and permitted link destinations, before persistent Azure DevOps operations.
- Deriving normalised source titles.
- Extracting each item's direct body, recognising the approved Tags and Acceptance Criteria constructs and partitioning Description, Tags and Acceptance Criteria content.
- Preparing each item's mandatory `System.Description` value, any applicable Acceptance Criteria value through the approved normative HTML rendering contract, and any applicable plain-text `System.Tags` value.
- Constructing deterministic source-side identities.
- Preserving deterministic source processing order.
- Producing the parsed Epic → Feature → Product Backlog Item → Task structure for downstream generation.
- Preparing candidate work item data for compatibility validation without constructing Azure DevOps HTTP or JSON Patch request representations.
- Maintaining traceability between documentation and generated work items.

---

## 7.4 Backlog Generator

The Backlog Generator converts processed documentation into Azure DevOps work items.

Responsibilities include:

- Creating work item structures.
- Creating parent-child relationships.
- Preparing work item attributes.
- Coordinating candidate work items for REST Client request construction and execution.
- Preventing duplicate work item creation.
- Initiating persistent backlog generation only after Scrum compatibility validation succeeds.

---

## 7.5 Azure DevOps REST Client

The Azure DevOps REST Client manages communication with Azure DevOps.

Version 1.0 shall target Azure DevOps Services only and shall use the Azure DevOps Services organisation/project model. The Services REST base address shall be derived from the configured organisation according to the official Azure DevOps Services URL structure.

Azure DevOps Server instance, port, collection and Server-specific base-address handling are outside Version 1.0 architecture scope.

Responsibilities include:

- Authentication.
- REST API communication.
- Retrieving required work-item type metadata for Scrum compatibility validation.
- Using validation-only creation requests when static metadata alone cannot establish candidate payload compatibility.
- Exclusively constructing Work Item Create JSON Patch request representations from prepared candidate values, using only the approved field paths and canonical operation order.
- Applying only JSON serialization escaping to prepared values and performing no semantic transformation, Markdown rendering, HTML transformation or Tags reinterpretation.
- Using the same logical candidate JSON Patch document for validation-only and persistent creation, with `validateOnly=true` as the only Create-payload contract difference.
- Sending work item requests.
- Receiving Azure DevOps responses.
- Reporting API errors.

---

## 7.6 Logging Component

The Logging Component records application execution.

Responsibilities include:

- Execution logging.
- Warning logging.
- Error logging.
- Diagnostic information.

---

## 7.7 Error Handler

The Error Handler manages application failures.

Responsibilities include:

- Detecting execution errors.
- Reporting failures.
- Supporting graceful application termination where recovery is not possible.

---

# 8. Data Flow

The application follows the logical execution sequence below.

1. The user starts the application.
2. Configuration is loaded.
3. Configuration is validated.
4. Approved backlog-input Markdown documents are discovered, parsed, validated, partitioned and rendered for mandatory Description values, optional applicable Acceptance Criteria values and optional Tags values according to `09-Documentation-Input.md` before persistent Azure DevOps operations.
5. Parsed backlog structures are generated.
6. Candidate Azure DevOps work items, including prepared Description values, applicable Acceptance Criteria values and applicable Tags values, are prepared.
7. Azure DevOps Scrum compatibility is validated through work-item type metadata and, where necessary, validation-only requests.
8. Persistent REST API requests are executed.
9. Results are logged.
10. Execution summary is presented.

Each stage shall complete successfully before the next stage begins.

---

# 9. Configuration Management

Application behaviour shall be controlled through external configuration.

Configuration shall include:

- Azure DevOps organisation.
- Azure DevOps project.
- Authentication settings.
- Documentation location.
- Logging configuration.
- Application options.

Configuration shall remain separate from application source code.

Scrum compatibility shall remain a fixed Version 1.0 product constraint. Configuration shall not introduce process mappings, work-item type mappings, field mappings or required-field overrides.

---

# 10. Security Architecture

Version 1.0 shall follow the following security principles:

- Sensitive information shall not be hard-coded.
- Personal Access Tokens shall be provided through configuration.
- Authentication credentials shall not be written to log files.
- Communication with Azure DevOps shall use secure HTTPS connections.
- Configuration files containing sensitive information shall be excluded from version control where appropriate.

---

# 11. Error Handling

Version 1.0 shall implement a consistent error handling strategy.

The application shall:

- Validate configuration before execution.
- Detect invalid input data.
- Validate source input before persistent Azure DevOps operations.
- Detect Azure DevOps communication failures.
- Detect Azure DevOps Scrum compatibility failures before persistent backlog generation.
- Report meaningful error messages.
- Record execution failures in the application log.
- Terminate gracefully when recovery is not possible.

Unexpected exceptions shall be handled in a controlled manner to prevent application crashes and to provide sufficient diagnostic information.

---

# 12. Logging Strategy

The application shall provide logging to support operational monitoring, troubleshooting and future maintenance.

The logging strategy shall include:

- Application startup.
- Configuration validation.
- Documentation processing.
- Azure DevOps communication.
- Work item creation.
- Warning messages.
- Error messages.
- Execution summary.

Logging shall provide sufficient information to diagnose issues without exposing sensitive information.

---

# 13. Extensibility

The architecture shall support future enhancements without requiring significant modification of the existing design.

Version 1.0 establishes an architectural foundation for future capabilities, including:

- Additional Azure DevOps work item types.
- Alternative authentication methods.
- Additional configuration options.
- Support for multiple backlog templates.
- Synchronisation of existing work items.
- Integration with additional project management platforms.

Future enhancements shall preserve the established architectural principles and maintain backward compatibility where practical.

---

# 14. Architecture Traceability

This Software Architecture Document provides the technical implementation framework for the approved Product Requirements Document.

Traceability shall be maintained between:

- Product Requirements Document
- Software Architecture Document
- Development Roadmap
- Azure DevOps Backlog
- Source Code
- Test Documentation

The Software Architecture Document shall remain consistent with the approved Product Requirements Document and shall not introduce functionality that is not traceable to an approved requirement.

---

# 15. Approval

Approval of a document version requires:

- Completion of the editorial review.
- Approval of that document version.
- Creation of the corresponding Approved Baseline.
- Commit to the project repository using the agreed Git workflow.

The document metadata and Version History record whether the current version has completed this approval process.

Subsequent modifications shall follow the established documentation governance process and be recorded through Version History.
