# Azure DevOps Backlog Generator

# Software Architecture Document

> *This document defines the software architecture of the Azure DevOps Backlog Generator and describes the architectural principles, components and interactions that support Version 1.0.*

**Version:** 2.18

**Status:** Approved Baseline

**Last Updated:** 2026-08-29

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
| 1.9 | 2026-08-21 | Approved Baseline | Jack Spaetjens | Defined parent-child relationship orchestration, ownership and failure-handling responsibilities. |
| 2.0 | 2026-08-23 | Approved Baseline | Jack Spaetjens | Defined persisted source-identity and resolve-or-create responsibilities. |
| 2.1 | 2026-08-23 | Approved Baseline | Jack Spaetjens | Defined reused-child relationship inspection, recovery and descendant-gating responsibilities. |
| 2.2 | 2026-08-25 | Draft | Jack Spaetjens | Defined run-level duplicate logical identity and persisted-marker collision validation responsibilities. |
| 2.3 | 2026-08-25 | Approved Baseline | Jack Spaetjens | Defined the internal REST Client Foundation boundary and urllib transport responsibilities. |
| 2.4 | 2026-08-25 | Approved Baseline | Jack Spaetjens | Defined the Version 1.0 REST Client Foundation proxy boundary. |
| 2.5 | 2026-08-27 | Approved Baseline | Jack Spaetjens | Clarified Scrum compatibility evidence, mandatory validation-only coverage and execution ordering responsibilities. |
| 2.6 | 2026-08-27 | Approved Baseline | Jack Spaetjens | Clarified the PAT runtime-secret input boundary. |
| 2.7 | 2026-08-27 | Approved Baseline | Jack Spaetjens | Synchronised WIQL identity lookup and Work Item GET evidence retrieval implementation status. |
| 2.8 | 2026-08-28 | Approved Baseline | Jack Spaetjens | Recorded Persistent Work Item Create transport as implemented in the current architecture baseline. |
| 2.9 | 2026-08-28 | Approved Baseline | Jack Spaetjens | Recorded Parent-Child Relationship JSON Patch construction as implemented. |
| 2.10 | 2026-08-28 | Approved Baseline | Jack Spaetjens | Defined successful Parent-Child Relationship PATCH response-validation and no-evidence return semantics. |
| 2.11 | 2026-08-28 | Approved Baseline | Jack Spaetjens | Recorded Parent-Child Relationship HTTP PATCH transport as implemented. |
| 2.12 | 2026-08-28 | Approved Baseline | Jack Spaetjens | Recorded reused-child Parent-Child Relationship state GET transport and structural evidence parsing as implemented. |
| 2.13 | 2026-08-28 | Approved Baseline | Jack Spaetjens | Recorded generator-level reused-child relationship-state classification as implemented. |
| 2.14 | 2026-08-28 | Approved Baseline | Jack Spaetjens | Recorded generator-level MISSING missing-parent recovery coordination as implemented. |
| 2.15 | 2026-08-29 | Approved Baseline | Jack Spaetjens | Recorded merged reused-child descendant-gating implementation status. |
| 2.16 | 2026-08-29 | Approved Baseline | Jack Spaetjens | Synchronized merged complete non-root Parent-Child Relationship lifecycle coordination status. |
| 2.17 | 2026-08-29 | Approved Baseline | Jack Spaetjens | Synchronized implemented root existing/new Work Item lifecycle coordination status. |
| 2.18 | 2026-08-29 | Approved Baseline | Jack Spaetjens | Approved the Version 1.0 Generator Orchestration preflight, global fail-fast and composition-ownership contract. |

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
- Loading and validating configuration, acquiring the runtime PAT, constructing the REST Client, discovering and processing documentation, invoking the Backlog Generator, logging/reporting and mapping the result to a process exit status.
- Not independently coordinating structural compatibility, validation-only sequencing, hierarchy lifecycle sequencing or persistence decisions.

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
- Producing each item's canonical relative source path and complete ordered normalised semantic-heading hierarchy, including heading levels, under the authority of `09-Documentation-Input.md`.
- Preparing candidate work item data for compatibility validation without constructing Azure DevOps HTTP or JSON Patch request representations.
- Not computing the persisted source-identity digest, constructing WIQL or interpreting Azure DevOps lookup results.
- Not performing run-level duplicate logical identity or persisted-marker collision validation.
- Not constructing Azure DevOps relation URLs or relationship JSON Patch payloads.
- Maintaining traceability between documentation and generated work items.

---

## 7.4 Backlog Generator

The Backlog Generator converts processed documentation into Azure DevOps work items.

Responsibilities include:

- Creating work item structures.
- Creating parent-child relationships.
- Preparing work item attributes.
- Coordinating candidate work items for REST Client request construction and execution.
- Maintaining the resolved candidate parent-child hierarchy and resolving created or reused source items to Azure DevOps numeric work-item IDs.
- Serialising each approved logical source identity using the Version 1.0 binary framing, computing its SHA-256 digest and formatting the persisted identity marker.
- Validating run-wide logical identity uniqueness and detecting persisted-marker collisions across every semantic item from all parsed documents. The Backlog Generator shall fail deterministically before compatibility validation or REST activity when two or more items have the same logical identity, or when distinct logical identities produce the same complete marker.
- Owning the complete compatibility-to-persistence domain operation: following successful run-wide source-identity validation, constructing every WorkItemCandidate in deterministic source order; retrieving and retaining canonical project evidence; retrieving required work-item-type and global/type-specific field metadata; evaluating structural Scrum compatibility; and submitting every candidate through validation-only Create in deterministic source order.
- Treating validation-only Create as candidate-specific evidence: every actual WorkItemCandidate shall be validated with the same approved JSON Patch contract intended for persistent Create. Equivalent work-item type, optional-field presence or JSON Patch shape shall not allow one candidate to represent another.
- Establishing the explicit preflight/persistence mutation barrier only after every validation-only Create succeeds. No WIQL lookup, Work Item GET, persistent Create, relationship-state GET or Parent-Child Relationship PATCH may begin before that barrier.
- Coordinating deterministic hierarchy processing only after the barrier, using retained canonical project evidence for existing/new resolution, invoking the root lifecycle coordinator for roots and the non-root lifecycle coordinator for non-root items, and beginning descendant processing only after parent or root eligibility is established.
- Applying global fail-fast across preflight and hierarchy processing. The first controlled or uncontrolled failure terminates the complete invocation and prevents later document, root, sibling, descendant, candidate or Azure DevOps generator operation. No retry, rollback, deletion, compensation, alternate credential, downgrade or continuation is introduced; accepted remote state remains legitimate partial state for recovery through a later normal invocation.
- Coordinating resolve-or-create processing only after the preflight/persistence mutation barrier and interpreting zero, one and multiple lookup outcomes.
- Associating source items with created or reused Azure DevOps numeric IDs and retaining the current numeric revision returned for reused items.
- Preventing Create after successful existing-item resolution and not inferring permission to compare or update ordinary fields.
- Coordinating parent resolution-or-creation before child persistent creation and the immediate child-to-parent relationship request after successful child creation.
- Supplying the parent ID, child ID and current child revision to the REST Client for each non-root child relationship.
- Coordinating relationship-state inspection for every reused non-root child after successful identity resolution.
- Comparing parsed reverse-hierarchy target IDs with the intended numeric parent ID and classifying the reused-child state as MISSING, CORRECT or CONFLICTING. This pure classification is implemented.
- Coordinating MISSING missing-parent recovery by invoking the approved Parent-Child Relationship PATCH with the fresh relationship-state revision. This purpose-specific coordination is implemented.
- Providing complete non-root Parent-Child Relationship lifecycle coordination for an already-resolved candidate. Identity resolution remains upstream. For NEW resolution, the lifecycle coordinator performs persistent Create exactly once, uses the returned Work Item ID and Create revision for one immediate Parent-Child Relationship PATCH, and returns successfully only after that PATCH succeeds. The NEW branch performs no relationship-state GET, classification, reused-child gate call or post-PATCH reread. For REUSED resolution, the coordinator retrieves fresh relationship state exactly once, classifies it exactly once and invokes the existing reused-child descendant gate. CORRECT continues without relationship mutation, MISSING delegates to existing recovery using the fresh relationship-state revision, and CONFLICTING raises `ConflictingReusedChildRelationshipError`. Successful REUSED return occurs only after the gate succeeds. The coordinator returns only the eligible child Work Item ID because a revision may be stale after relationship PATCH; later descendant processing requires the eligible ID only. The non-root coordinator performs neither WIQL nor identity resolution, descendant processing, callbacks or recursive traversal. It introduces no retry, reread, rollback, deletion compensation or alternate credentials. If NEW Create succeeds and relationship PATCH fails, the invocation fails; a later source-identity resolution can discover the created Work Item as reused, then fresh relationship evidence and existing reused-child logic repair, continue or block as MISSING, CORRECT or CONFLICTING requires. This rerun safety arises from identity resolution plus fresh relationship evidence, not coordinator-level retry. Complete generator/run orchestration remains deferred.
- Providing implemented root existing/new Work Item lifecycle coordination. The root-only coordinator invokes existing/new resolution once; for NEW it passes the exact supplied candidate and PAT to persistent Create once and returns the Create response ID, while for REUSED it returns the validated existing ID without Create. It returns no revision and performs no relationship-state GET, classification, gate, Parent-Child Relationship PATCH, descendant processing, validation-only Create or compatibility orchestration. Resolution and Create failures propagate without retry, fallback, reread, rollback, deletion compensation or other compensation. Hierarchy traversal and application/run orchestration remain deferred.
- Preventing duplicate work item creation.
- Initiating deterministic hierarchy processing only after all preflight operations succeed. The full preflight coordinator and complete hierarchy traversal are not implemented yet; the implemented root and non-root lifecycle coordinators remain lower-level capabilities invoked by the future complete orchestration.

---

## 7.5 Azure DevOps REST Client

The Azure DevOps REST Client manages communication with Azure DevOps.

Version 1.0 shall target Azure DevOps Services only and shall use the Azure DevOps Services organisation/project model. The Services REST base address shall be derived from the configured organisation according to the official Azure DevOps Services URL structure.

Azure DevOps Server instance, port, collection and Server-specific base-address handling are outside Version 1.0 architecture scope.

The REST Client Foundation shall provide a small internal, purpose-specific transport interface. It shall use `urllib` from the Python standard library and shall not introduce a third-party HTTP dependency. It shall own Azure DevOps Services URL construction, HTTP request construction and transmission, Basic authentication-header construction, required common headers, JSON transport mechanics, the fixed timeout, expected-status validation, redirect rejection, no-retry behaviour, controlled transport, network and response failures, and secret-safe diagnostics. It shall not be a general-purpose public HTTP abstraction.

Each request shall use the `urllib` request/response lifecycle independently. The response body shall be consumed and the response closed during request processing. The foundation shall not retain response objects, a persistent session, cookie state, redirect state, a connection pool or other persistent mutable request state. Endpoint-specific public operations include compatibility validation, WIQL, Work Item GET, Persistent Work Item Create, Parent-Child Relationship PATCH and reused-child relationship-state GET REST transport. Persistent Create reuses the approved JSON Patch builder and returns structurally validated `AzureDevOpsWorkItem` evidence; the REST Client remains transport-only. Parent-Child Relationship JSON Patch construction and HTTP PATCH transport are implemented. The transport reuses the approved JSON Patch builder and this REST Client foundation with the fixed `/rev` `test`, `/relations/-` `add`, `System.LinkTypes.Hierarchy-Reverse` relation and absolute organisation-scoped parent target URI. Its exact `200 OK` response has a non-empty valid UTF-8 JSON object body; no response property is required, unknown properties are ignored and the REST Client returns `None` after validation. The reused-child relationship-state GET requests `$expand=relations`, validates the child ID, fresh revision and relation structure, validates and parses exact reverse-hierarchy target URIs, and returns ordered duplicate-preserving reverse-parent IDs. Generator-level intended-parent comparison and relationship-state classification are implemented. The Backlog Generator, not the REST Client, owns sequencing and lifecycle policy; the REST Client only executes requested authenticated transport, serialization and response validation. Complete preflight orchestration and hierarchy traversal remain deferred to later capability slices.

The foundation shall explicitly disable `urllib` proxy handling and shall not inherit ambient or system proxy state. Proxy configuration, proxy authentication, proxy credentials, PAC support, system-proxy integration and environment-proxy support are outside Version 1.0 and remain deferred to a future approved capability.

Responsibilities include:

- Authentication.
- REST API communication.
- Retrieving required work-item type metadata for Scrum compatibility validation.
- Retrieving type-specific work-item field metadata and global field metadata as separate compatibility evidence sources.
- Verifying the fixed `Custom.BacklogGeneratorSourceIdentity` reference name, `Backlog Generator Source Identity` display name, String/single-line-text type, applicability, writability and optional process status during compatibility validation.
- Distinguishing structural metadata compatibility from final candidate acceptance, without treating global field metadata as proof of work-item-type applicability.
- Using mandatory non-persisting validation-only creation requests for every occurring work-item type after structural compatibility succeeds.
- Exclusively constructing Work Item Create JSON Patch request representations from prepared candidate values, using only the approved field paths and canonical operation order.
- Holding the custom identity-field reference as a fixed API constant, constructing and transmitting the fixed project/type/marker WIQL request, retrieving the sole candidate work item and validating transport and response structure.
- Returning the required candidate ID, revision, project, type and identity-field state without computing logical source identity or deciding business-field updates.
- Applying only JSON serialization escaping to prepared values and performing no semantic transformation, Markdown rendering, HTML transformation or Tags reinterpretation.
- Using the same logical candidate JSON Patch document for validation-only and persistent creation, with `validateOnly=true` as the only Create-payload contract difference.
- Constructing and sending Parent-Child Relationship PATCH requests with the canonical parent relation target URL, the relationship-specific `/rev` `test` operation and the `/relations/-` `add` operation; validating only the approved successful response object shape and returning `None` without relationship-state interpretation.
- Constructing and sending the reused-child relationship-state GET using API version `7.1` and `$expand=relations`.
- Validating the returned work-item ID, fresh revision and relation collection and member structure, including the approved omitted-or-empty zero-state representations.
- Strictly parsing reverse-hierarchy relation target URIs, validating their fixed Azure DevOps Services structure and extracting numeric target work-item IDs.
- Reusing the approved Parent-Child Relationship PATCH unchanged for missing-parent recovery with the fresh relationship-state revision.
- Applying only JSON serialization and JSON-required escaping to relationship payload values.
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
5. Parsed `DocumentationHierarchy` structures are generated and supplied with the REST Client and runtime PAT to the Backlog Generator.
6. The Backlog Generator performs deterministic run-wide source-identity collision validation across all parsed documents.
7. The Backlog Generator constructs every WorkItemCandidate in deterministic source order.
8. The Backlog Generator retrieves the configured project and retains canonical project evidence, retrieves required work-item-type and global/type-specific field metadata, and evaluates structural Scrum compatibility.
9. The Backlog Generator submits every candidate through validation-only Create in deterministic source order, using that candidate's approved persistent-Create JSON Patch contract.
10. The final successful validation-only Create establishes the explicit preflight/persistence mutation barrier. Before it, no WIQL, Work Item GET, persistent Create, relationship-state GET or Parent-Child Relationship PATCH may occur.
11. Only after the barrier, deterministic document, root and sibling hierarchy processing begins. For every source item in deterministic source order, the Backlog Generator requests an existing-item lookup scoped to the canonical configured project, exact supported type and exact marker.
12. Zero candidates cause Work Item Create using the approved five-field contract. Exactly one candidate causes Work Item GET, validation of its canonical project name, exact type and ordinal marker, and reuse of its numeric ID and revision without Create. Multiple, malformed or conflicting candidates stop processing before Create.
13. For a newly created non-root child, the parent shall be created or resolved before the child, and the child-to-parent relationship PATCH shall occur immediately after successful child creation using the child ID and revision returned by Create.
14. For a reused non-root child, the REST Client retrieves its fresh relationship state, validates the response and reverse-hierarchy target URI structure, and returns the fresh revision and parsed target IDs. The Backlog Generator compares those IDs with the intended parent ID and classifies the state as MISSING, CORRECT or CONFLICTING.
15. MISSING causes the approved Parent-Child Relationship PATCH using the fresh relationship-state revision; CORRECT causes no PATCH; and CONFLICTING stops processing without remote mutation.
16. Descendants become eligible for persistent processing only after a newly created child's relationship PATCH succeeds, a reused child is observed as CORRECT or a reused child's MISSING relationship is successfully repaired.
17. Root Epic items require neither relationship-state retrieval nor a parent relationship PATCH.
18. Any controlled or uncontrolled failure causes a global stop: no later document, root, sibling, descendant, candidate or Azure DevOps generator operation begins. No retry, rollback, deletion, compensation or alternate credential is attempted.
19. Results are logged.
20. Execution summary is presented.

This flow permits deterministic recovery when an earlier execution created a child but its immediate relationship PATCH failed: the later execution resolves the parent and child, observes MISSING using a fresh relationship-state GET, repairs the relationship using the fresh revision and continues only after success.

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
- Personal Access Tokens are runtime secrets supplied exclusively through `AZDO_PAT` and remain outside TOML configuration.
- Authentication credentials shall not be written to log files.
- Communication with Azure DevOps shall use secure HTTPS connections.
- Configuration files containing sensitive information shall be excluded from version control where appropriate.
- Caller-supplied WIQL structure shall not be accepted. Identity lookup shall use application-controlled fields, operators and type literals, the `@project` macro and a marker validated against the fixed Version 1.0 format before query construction.
- Source-derived titles, paths and headings shall not be interpolated into WIQL. PATs, Authorization headers, full remote response bodies by default and raw logical source identities without necessity shall not be logged.

---

# 11. Error Handling

Version 1.0 shall implement a consistent error handling strategy.

The application shall:

- Validate configuration before execution.
- Detect invalid input data.
- Validate source input before persistent Azure DevOps operations.
- Detect Azure DevOps communication failures.
- Detect Azure DevOps Scrum compatibility failures before persistent backlog generation.
- Stop before Create on identity lookup failure, local or remote marker ambiguity, malformed result IDs, candidate retrieval failure, or conflicting project, type or marker evidence. A rejected candidate shall not be reinterpreted as zero matches.
- On a parent-child relationship PATCH failure, stop further persistent backlog generation immediately, report the failure clearly and do not create later work items or relationships.
- Fail on reused-child relationship-state GET failure, child-ID mismatch, missing or non-numeric revision, malformed relation data, malformed reverse-hierarchy target URI, wrong parent, multiple parents or duplicate parent relationships.
- On a missing-parent recovery PATCH or `/rev` conflict, stop further persistent backlog generation immediately and block descendants.
- Do not automatically re-read, retry, roll back, delete, remove or replace Azure DevOps relationship state after a failure; already-created work items and relationships shall remain as accepted partial persistent state.
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
