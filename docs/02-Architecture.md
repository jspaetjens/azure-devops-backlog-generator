# Azure DevOps Backlog Generator

# Software Architecture Document

> *This document defines the software architecture of the Azure DevOps Backlog Generator and describes the architectural principles, components and interactions that support Version 1.0.*

**Version:** 2.43

**Status:** Draft

**Last Updated:** 2026-09-12

**Target Release:** v1.0.0

**License:** MIT

**Author:** Jack Spaetjens

**Revision scope:** Revision 2.43 proposes the Gate-3 acceptance framework for owner review.
References below to revision 2.42 as Approved Baseline identify the preceding implementation
baseline, not approval of this Draft. Existing slice contracts and recorded results remain unchanged.

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
| 2.19 | 2026-08-29 | Approved Baseline | Jack Spaetjens | Synchronized implemented full preflight coordinator status through the mutation barrier. |
| 2.20 | 2026-08-30 | Approved Baseline | Jack Spaetjens | Corrected stale Full Preflight Coordinator implementation-status wording while preserving deferred hierarchy traversal. |
| 2.21 | 2026-08-30 | Approved Baseline | Jack Spaetjens | Synchronized implemented deterministic hierarchy traversal status while retaining final Generator entry composition before Review Gate 2. |
| 2.22 | 2026-08-30 | Approved Baseline | Jack Spaetjens | Synchronized implemented final Generator-owned preflight-to-traversal orchestration status. |
| 2.23 | 2026-08-30 | Approved Baseline | Jack Spaetjens | Recorded Review Gate 2 PASS with zero findings and no required remediation. |
| 2.24 | 2026-08-31 | Approved Baseline | Jack Spaetjens | Defined the approved Application/Run Slice 1 composition contract. |
| 2.25 | 2026-08-31 | Approved Baseline | Jack Spaetjens | Synchronized implemented Application/Run Slice 1 status while retaining incomplete wider application/run responsibilities. |
| 2.26 | 2026-08-31 | Approved Baseline | Jack Spaetjens | Defined the approved Application/Run Slice 2 configuration-bootstrap contract. |
| 2.27 | 2026-08-31 | Approved Baseline | Jack Spaetjens | Synchronized implemented Application/Run Slice 2 status while retaining incomplete wider application/run responsibilities. |
| 2.28 | 2026-09-01 | Approved Baseline | Jack Spaetjens | Defined the Application/Run Slice 3 Process Bootstrap Invocation contract. |
| 2.29 | 2026-09-02 | Approved Baseline | Jack Spaetjens | Synchronized implemented Application/Run Slice 3 Process Bootstrap Invocation status while retaining incomplete wider application/run responsibilities. |
| 2.30 | 2026-09-02 | Approved Baseline | Jack Spaetjens | Defined the Application/Run Slice 4 Controlled Application Outcome Mapping contract. |
| 2.31 | 2026-09-02 | Approved Baseline | Jack Spaetjens | Synchronized implemented Application/Run Slice 4 Controlled Application Outcome Mapping status while retaining incomplete wider application/run responsibilities. |
| 2.32 | 2026-09-03 | Approved Baseline | Jack Spaetjens | Defined the Application/Run Slice 5 Controlled Failure Reporting to Standard Error contract. |
| 2.33 | 2026-09-03 | Approved Baseline | Jack Spaetjens | Synchronized implemented Application/Run Slice 5 Controlled Failure Reporting to Standard Error status. |
| 2.34 | 2026-09-04 | Approved Baseline | Jack Spaetjens | Defined the approved but unimplemented Application/Run Slice 6 Runtime File Logging and Controlled-Failure Events contract. |
| 2.35 | 2026-09-04 | Approved Baseline | Jack Spaetjens | Synchronized implemented Application/Run Slice 6 Runtime File Logging and Controlled-Failure Events status. |
| 2.36 | 2026-09-06 | Approved Baseline | Jack Spaetjens | Defined the approved but unimplemented Application/Run Slice 7 Package Execution Adapter with Controlled Process Termination contract. |
| 2.37 | 2026-09-06 | Approved Baseline | Jack Spaetjens | Synchronized implemented Application/Run Slice 7 package execution status and preserved interim limitations. |
| 2.38 | 2026-09-06 | Approved Baseline | Jack Spaetjens | Defined the approved but unimplemented Application/Run Slice 8 lifecycle file-logging contract. |
| 2.39 | 2026-09-08 | Approved Baseline | Jack Spaetjens | Synchronized implemented Application/Run Slice 8 Process-Neutral Application Lifecycle File Logging status. |
| 2.40 | 2026-09-11 | Approved Baseline | Jack Spaetjens | Defined the owner-approved but unimplemented final unexpected-error handling and diagnostic-safety contract. |
| 2.41 | 2026-09-11 | Approved Baseline | Jack Spaetjens | Allocated the approved Final Unexpected-Error Handling and Diagnostic Safety contract as Application/Run Slice 9 without changing UE-D1–UE-D10. |
| 2.42 | 2026-09-11 | Approved Baseline | Jack Spaetjens | Synchronized implemented Application/Run Slice 9 Final Unexpected-Error Handling and Diagnostic Safety status. |
| 2.43 | 2026-09-12 | Draft | Jack Spaetjens | Proposed Review Gate 3 operational boundaries and dependencies on unresolved behavioural contracts. |

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
    - [7.1.1 Application/Run Slice 1](#711-applicationrun-slice-1)
    - [7.1.2 Application/Run Slice 2](#712-applicationrun-slice-2)
    - [7.1.3 Application/Run Slice 3 — Process Bootstrap Invocation](#713-applicationrun-slice-3--process-bootstrap-invocation)
    - [7.1.4 Application/Run Slice 4 — Controlled Application Outcome Mapping](#714-applicationrun-slice-4--controlled-application-outcome-mapping)
    - [7.1.5 Application/Run Slice 5 — Controlled Failure Reporting to Standard Error](#715-applicationrun-slice-5--controlled-failure-reporting-to-standard-error)
    - [7.1.6 Application/Run Slice 6 — Runtime File Logging and Controlled-Failure Events](#716-applicationrun-slice-6--runtime-file-logging-and-controlled-failure-events)
    - [7.1.7 Application/Run Slice 7 — Package Execution Adapter with Controlled Process Termination](#717-applicationrun-slice-7--package-execution-adapter-with-controlled-process-termination)
    - [7.1.8 Application/Run Slice 8 — Process-Neutral Application Lifecycle File Logging](#718-applicationrun-slice-8--process-neutral-application-lifecycle-file-logging)
    - [Application/Run Slice 9 — Final Unexpected-Error Handling and Diagnostic Safety](#applicationrun-slice-9--final-unexpected-error-handling-and-diagnostic-safety)
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
- [13. Review Gate 3 Operational Readiness Boundaries](#13-review-gate-3-operational-readiness-boundaries)
  - [13.1 Logging acceptance boundary](#131-logging-acceptance-boundary)
  - [13.2 HTTP reporting and execution-summary dependencies](#132-http-reporting-and-execution-summary-dependencies)
  - [13.3 Runtime, safety and recovery boundaries](#133-runtime-safety-and-recovery-boundaries)
- [14. Extensibility](#14-extensibility)
- [15. Architecture Traceability](#15-architecture-traceability)
- [16. Approval](#16-approval)

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

### 7.1.1 Application/Run Slice 1

Application/Run Slice 1 is an implemented callable composition layer located in `main.py`. It exposes exactly:

```python
coordinate_application_run(configuration: Configuration) -> None
```

It accepts an already-loaded and validated `Configuration`; configuration-file loading, TOML parsing,
configuration validation, runtime PAT acquisition and CLI argument parsing remain outside this slice.
The slice performs the following operations exactly once and in order:

1. Call `DocumentationProcessor().process(configuration.documentation.source_directory)` with the
   resolved `Path` unchanged.
2. Construct `AzureDevOpsRestClient(configuration.azure_devops.organization,
   configuration.azure_devops.project)`.
3. Call `coordinate_generator_orchestration` once with the returned
   `DocumentationHierarchy`, that REST client and
   `personal_access_token=configuration.personal_access_token`.
4. Return `None` after successful Generator completion.

The PAT shall not be passed to the REST-client constructor, altered, logged or represented in a result
object. The slice shall not perform documentation discovery, hierarchy or source-identity logic itself;
it shall not own REST base-address, API-version, timeout, proxy, redirect, authentication-construction or
retry policy; and it shall not invoke Generator preflight, traversal, lifecycle, resolution or persistence
operations directly.

Controlled and uncontrolled collaborator exceptions propagate unchanged. On documentation-processing
failure, the REST client shall not be constructed and the Generator shall not be invoked. On REST-client
construction failure, the Generator shall not be invoked. On Generator failure, the slice shall not retry,
fall back, catch and continue, translate the exception or invoke the Generator again.

Slice 1 does not implement CLI parsing, a `main()` process entry point, `__main__.py`, console-script
registration, logging/reporting, user-facing error formatting or process-exit mapping. Those remain required
future Version 1.0 responsibilities of the configuration/bootstrap, CLI, logging/reporting and process
layers; the callable `None` return does not replace the eventual process exit-status contract.

---

### 7.1.2 Application/Run Slice 2

Application/Run Slice 2 is an implemented callable configuration-bootstrap composition layer. It exposes
exactly, using `Sequence` from `collections.abc`:

```python
coordinate_application_bootstrap(arguments: Sequence[str]) -> None
```

It performs the following operations exactly once and in order:

1. Call `load_configuration_from_cli(arguments)` with the supplied `arguments` unchanged.
2. Receive the exact returned validated `Configuration`.
3. Call `coordinate_application_run(configuration)` once with that exact object.
4. Return `None` after successful Slice-1 completion.

`load_configuration_from_cli` remains responsible for configuration-file selection, including the existing
`--config-file PATH` and `--config-file=PATH` forms and default selection; argument validation; TOML loading;
configuration validation; source-directory resolution; configured logging-directory validation or creation;
runtime `AZDO_PAT` acquisition and validation; and `Configuration` construction. Slice 2 does not parse CLI
options, read the environment, call `validate_configuration` separately, or otherwise duplicate those
responsibilities.

The exact returned `Configuration` is passed unchanged into Slice 1. Slice 2 performs no direct
PAT handling, including reading, normalising, copying, logging or reporting `AZDO_PAT`. It does not construct
or invoke the Documentation Processor, REST Client or Generator, and does not directly coordinate Generator
preflight, the mutation barrier, traversal, resolution, lifecycle, persistence or relationship handling.

Controlled and uncontrolled failures from configuration selection, loading, validation, PAT validation and
Slice 1 propagate unchanged. A configuration failure prevents Slice-1 invocation. A Slice-1 failure
causes no retry, fallback, second invocation or later work. Slice 2 does not log, print, report, translate
or map failures to process exit status.

Slice 2 is configuration-file selection/bootstrap support, not the completed application CLI. It does not
implement `main()`, `__main__.py`, console-script registration, help, version output, new CLI options,
logging/reporting, user-facing error formatting or process-exit mapping. The process/CLI boundaries implemented
in Slices 3–7 remain separate from bootstrap.
The callable `None` return does not replace the implemented process-level exit-status behaviour.

---

### 7.1.3 Application/Run Slice 3 — Process Bootstrap Invocation

Application/Run Slice 3 is implemented. It introduces exactly the following process-facing callable in
`main.py`:

```python
main() -> None
```

Slice 3 composes the existing callable chain exactly as follows:

```text
sys.argv
→ sys.argv[1:]
→ coordinate_application_bootstrap(arguments)
→ existing Slice-2/Slice-1/Generator chain
→ None
```

`main()` reads the current process argument vector from `sys.argv`, excludes `sys.argv[0]`, and passes the
resulting `sys.argv[1:]` sequence directly to exactly one `coordinate_application_bootstrap(...)` invocation.
It performs no option parsing, normalisation, filtering, copying, validation or mutation of that sequence.
`coordinate_application_bootstrap(arguments: Sequence[str]) -> None` remains the explicit-arguments
configuration/bootstrap boundary, and `load_configuration_from_cli(...)` remains responsible for all CLI option
parsing and validation.

Slice 3 does not load or validate configuration; access the environment or PAT; process documentation;
construct a REST client; invoke a Generator API directly; retry; or fall back. It does not inspect,
normalise, copy, log, print or otherwise expose `AZDO_PAT` or `Configuration.personal_access_token`.
Successful bootstrap completion shall cause `main()` to return `None`.

Any controlled or uncontrolled exception raised by `coordinate_application_bootstrap(...)` propagates
unchanged through `main()`. Slice 3 does not catch, wrap, translate, retry, fall back, invoke bootstrap a
second time, log, report, map a process exit, call `sys.exit` or deliberately raise `SystemExit`. No subsequent
work shall occur after such a failure.

Slice 3 does not add a direct-execution guard, `__main__.py`, `[project.scripts]`, console-script registration,
packaging invocation semantics, stdout or stderr output, help or version output, logging configuration or
initialisation, execution reporting, traceback formatting, a controlled-exception catch set, or an
unexpected-exception policy. The later process/error layer remains responsible for controlled exception
classification, the approved `0`/`1` process-exit mapping, user-facing reporting, logging and executable
adapter decisions. Wider Application/Run therefore remains incomplete.

---

### 7.1.4 Application/Run Slice 4 — Controlled Application Outcome Mapping

Application/Run Slice 4 is implemented. It introduces exactly the following separate application/process wrapper
in `main.py`:

```python
run_process() -> int
```

It preserves the implemented Slice-3 callable:

```python
main() -> None
```

The Slice-4 flow is exactly:

```text
run_process()
→ main()
→ existing Slice-3/Slice-2/Slice-1/Generator chain
```

`run_process()` invokes `main()` exactly once. On successful `main()` completion it returns the exact integer
`0`. When `main()` raises a known controlled application exception, it catches that exception and returns the
exact integer `1`. It does not return `None` and does not re-raise a controlled failure.

The known controlled application exception set consists exactly of the existing `ConfigurationError`,
`DocumentationProcessingError` and `AzureDevOpsRestClientError` bases, and the existing explicit
Generator/domain classes `SourceIdentityValidationError`, `ExistingWorkItemResolutionError` and
`ConflictingReusedChildRelationshipError`. `AzureDevOpsHttpError`, including HTTP `401` and `403`, and
`AzureDevOpsResponseError`, including malformed-response failures, are controlled through the existing
`AzureDevOpsRestClientError` hierarchy. Slice 4 introduces no shared exception base and changes no existing
exception inheritance.

At the Slice-4 baseline, an exception outside that explicit set, including arbitrary `ValueError`, `TypeError`, untranslated `OSError`
or another arbitrary `Exception` subclass, propagates unchanged. Slice 4 does not catch `Exception`
generically, translate an unexpected exception to `1`, retry, fall back or invoke `main()` a second time.

Slice 4 maps callable outcomes only. It produces no stdout or stderr output, user-facing messages, error
formatting, sanitisation or traceback policy; does not initialise or call logging; does not raise or call
`SystemExit` or `sys.exit`; does not add a direct-execution guard, `__main__.py`, `[project.scripts]`,
console-script registration or executable packaging; and does not implement an execution summary. Generic direct
rendering of arbitrary exception messages remains unapproved. Implemented Slice 9 supplies the approved
fixed-message policy and supersedes Slice 4's unexpected propagation only at `run_process()`.

`main()` remains responsible only for acquiring `sys.argv[1:]` and delegating to
`coordinate_application_bootstrap(...)`; it does not map outcomes or terminate the process. CLI/process-specific
outcome, reporting and termination behaviour shall remain outside the shared Application Core. In consequence,
alternate presentation adapters, including a future GUI, may reuse typed application/core boundaries such as
`coordinate_application_run(configuration: Configuration) -> None` without process exit codes, `SystemExit`,
stdout/stderr behaviour or CLI-specific error formatting. This preserves architectural compatibility only; it
does not approve a GUI feature, implementation, framework or Version 1.0 scope.

The wider Application/Run phase remains incomplete. Slices 5–7 implement controlled-failure reporting,
logging and executable termination as described below; Slice 9 implements final unexpected handling and
bounded diagnostic safety. Broader logging, execution-summary content and presentation, broader integration/E2E,
Operational Readiness, Review Gate 3 and final release readiness remain future.
Console-script packaging remains conditional on separate approval.

---

### 7.1.5 Application/Run Slice 5 — Controlled Failure Reporting to Standard Error

Application/Run Slice 5 is implemented. It retains controlled-failure classification in the existing
`run_process() -> int` process adapter, which invokes `main()` exactly once. On a caught controlled failure, it
calls the private `_render_controlled_failure(error)`, writes the fixed category-only standard-error line and
returns the exact integer `1`. It does not change the return type, the existing controlled-failure classification
or the `0`/`1` application-outcome mapping.

The approved controlled categories shall render exactly one corresponding category-only line to `stderr`, followed
by exactly one newline: `ConfigurationError` hierarchy — `Configuration error.`;
`DocumentationProcessingError` hierarchy — `Documentation processing error.`;
`AzureDevOpsRestClientError` hierarchy — `Azure DevOps error.`;
`SourceIdentityValidationError` — `Source identity validation error.`;
`ExistingWorkItemResolutionError` — `Existing work item resolution error.`; and
`ConflictingReusedChildRelationshipError` — `Conflicting reused child relationship error.`. Each such controlled
failure returns the exact integer `1`, is not re-raised and leaves `stdout` empty.

The reporting is category-only. The implemented renderer exposes no data from an exception object: this expressly
excludes `str(exception)`, `repr(exception)`, exception arguments, CLI argument text, configuration paths,
documentation paths, source titles, source-derived arbitrary content, Azure DevOps URLs, response bodies, headers,
PAT values, Authorization values and arbitrary exception messages. The six fixed category strings are the complete
Slice-5 controlled-failure user-facing output. HTTP `401` and `403` remain controlled through the existing
`AzureDevOpsRestClientError` hierarchy and therefore render only `Azure DevOps error.`.
`AzureDevOpsTransportError`, `AzureDevOpsHttpError`, `AzureDevOpsResponseError` and other existing controlled
REST-client subclasses retain their lower-layer semantics. Slice 5 introduces no shared exception base and changes
no lower-layer or REST contract. The private renderer selects and writes fixed messages by approved exception type
only; no public reporting API or application-wide abstraction exists.

At the Slice-5 baseline, successful execution remains silent: after one successful `main()` invocation, `run_process()` returns the exact
integer `0` with no `stdout`, no `stderr`, no logging, no retry, no fallback and no process termination. An
unexpected exception remains outside the approved controlled set and propagates as the exact same object, unchanged
and without Slice-5 output, generic `Exception` catching, conversion to `1`, logging, retry, fallback or second
invocation. Slice 5 does not implement unexpected-exception reporting; implemented Slice 9 now owns that process-facing fallback.

`main() -> None` remains responsible only for `sys.argv`, `sys.argv[1:]` and one
`coordinate_application_bootstrap(...)` invocation; it shall not catch failures, render `stderr`, log or terminate.
`coordinate_application_bootstrap(...)`, `coordinate_application_run(...)`, Generator orchestration, REST
transport, configuration loading and documentation processing remain presentation-neutral. The process adapter owns
the stderr presentation, preserving alternate presentation adapters, including a future GUI, without leaking CLI
stderr behaviour into the shared Application Core. This is architectural compatibility only and does not approve a
GUI feature, implementation, framework or Version 1.0 scope.

Slice 5 does not introduce logging initialisation or calls, an execution summary, dynamic exception detail,
tracebacks, `sys.exit`, `SystemExit`, a direct-execution guard, `__main__.py`, `[project.scripts]`, console-script
packaging, an executable adapter, retries, fallback, new CLI options, dependencies or GUI implementation.
Slices 6–7 implement runtime controlled-failure logging and the executable boundary as described below.
Remaining logging beyond Slice 8, execution summaries, final unexpected-error handling and diagnostic safety,
broader integration/E2E, Operational Readiness, Review Gate 3 and final
release-readiness work remain future. The wider Application/Run phase remains incomplete.

---

### 7.1.6 Application/Run Slice 6 — Runtime File Logging and Controlled-Failure Events

Application/Run Slice 6 is implemented. It adds application-wide runtime
file logging for controlled process-terminating failures without changing the existing shared Application Core,
Generator, REST Client, Documentation Processor or domain result contracts.

At the beginning of each application/bootstrap invocation, before configuration loading, the application removes and
closes prior application-owned handlers and clears `_ACTIVE_LOG_HANDLER`; unrelated and root handlers remain
untouched. After configuration has loaded and validated successfully, and before downstream application work requiring
logging, the application/bootstrap boundary initialises one application-owned file handler for the current invocation.
The logger name is `azure_devops_backlog_generator`; it uses `propagate=False` and does not emit through root or
console handlers. The sole file is
`<validated logging.log_directory>/azure-devops-backlog-generator.log`, opened in append mode with UTF-8
encoding. It uses standard-library Python logging only, no rotation, no retention policy, and no external logging
dependency. The configured `logging.level` applies to the application logger and owned handler.

Each record shall contain exactly the logical fields timestamp, level, logger name and message, with format
`%(asctime)s %(levelname)s %(name)s %(message)s` and timestamp format `%Y-%m-%dT%H:%M:%S`. Slice-6 controlled
failure events shall use `CRITICAL`, so they remain visible for every permitted configured threshold. This level
expresses process-termination severity for this slice only and does not alter lower-layer exception semantics.

The process-facing `run_process() -> int` remains the owner of controlled classification, category-only stderr
rendering and integer outcome mapping. Slice 9 adds its generic unexpected fallback. For each controlled failure that reaches it
after logging has initialised for the current invocation, it makes exactly one application-owned `CRITICAL`
controlled-failure event-emission attempt. It creates a `LogRecord` using the named application logger and dispatches
it directly only to `_ACTIVE_LOG_HANDLER`; non-owned handlers attached to that same named logger receive no controlled
event. When the attempt succeeds, exactly one file record is written. The
event message shall be the same fixed category-only message rendered to stderr. No
dynamic exception detail may be logged, including `str(exception)`, `repr(exception)`, arguments, causes, paths,
source identities, titles, URLs, response bodies, headers, PAT values, Authorization values, arbitrary messages or
tracebacks. PAT and Authorization shall never be logged.

The seven controlled categories and exact messages shall be: `ConfigurationError` — `Configuration error.`;
`DocumentationProcessingError` — `Documentation processing error.`; `AzureDevOpsRestClientError` — `Azure DevOps
error.`; `SourceIdentityValidationError` — `Source identity validation error.`;
`ExistingWorkItemResolutionError` — `Existing work item resolution error.`;
`ConflictingReusedChildRelationshipError` — `Conflicting reused child relationship error.`; and the new dedicated
application-layer `ApplicationLoggingError` — `Application logging error.`. Slice 6 adds no shared/base exception
hierarchy. A valid configuration followed by runtime file-logging initialisation failure shall raise
`ApplicationLoggingError`. `run_process()` shall render exactly `Application logging error.` followed by one newline
to stderr, leave stdout empty, return exact integer `1`, and not re-raise, retry, fall back or use another logging
destination. As logging did not initialise, that error shall produce no file event. Logging infrastructure shall not
produce Python logging-internal diagnostics, a `Logging error` traceback, root-handler fallback or console output on
stdout or stderr.

File logging begins only after configuration loading, validation and logger initialisation succeed. A configuration
loading or validation `ConfigurationError` necessarily occurs before that point and retains the existing
`Configuration error.` stderr line and exact integer `1`, with no configured-file log attempt,
fallback/default/bootstrap file logger or alternate destination. Only controlled failures after successful
configuration loading, validation and runtime logging initialisation participate in the controlled-failure
event-emission contract. If their single emission attempt fails, the write failure is secondary: the original
controlled failure remains authoritative, its fixed stderr line and exact integer `1` remain unchanged, and stdout
remains empty. The application shall not retry, fall back, use another destination, emit another application event,
add stderr output, emit a logging traceback or Python logging-internal diagnostic, substitute
`ApplicationLoggingError`, or propagate the secondary logging error. `ApplicationLoggingError` applies only to
runtime logger initialisation failure before downstream execution.

Logging configuration is per invocation. At most one owned handler is active; repeated `run_process()` calls in one
interpreter do not duplicate handlers or events, and a prior owned handler is not reused as the active handler of a
later invocation. Partial initialisation is cleaned up. The application-owned handler suppresses only its own
logging-internal error diagnostics for secondary write failures; it does not change `logging.raiseExceptions` or
globally reconfigure logging.

Successful execution produces no Slice-6 success or lifecycle event. Slice 6 originally preserved same-object
unexpected propagation without reporting; implemented Slice 9 supersedes that process-facing behaviour
while direct lower-level propagation remains unchanged. Slice 6 does not add an execution summary, `sys.exit`, `SystemExit`,
direct-execution guard, `__main__.py`, console-script packaging, subprocess contract, new CLI option, retry,
fallback, rollback, compensation or GUI implementation. File logging is operational infrastructure, not a
presentation adapter; stdout, stderr, process outcomes and termination remain outside the presentation-neutral
shared Application Core so a future GUI may reuse the typed application/core boundaries.

---

### 7.1.7 Application/Run Slice 7 — Package Execution Adapter with Controlled Process Termination

Application/Run Slice 7 is implemented in PR #136 (implementation commit `468d98d`, merge `009ef71`),
following the contract in PR #134 and approval in PR #135. S7-D1 and S7-D2 remain approved owner decisions.
Application/Run Slices 1–9 are implemented; the wider Application/Run phase remains incomplete.

**S7-D1 — Executable invocation surface.** Slice 7 implements exactly one executable package surface:

```text
python -m azure_devops_backlog_generator
```

The production surface is `src/azure_devops_backlog_generator/__main__.py`. Its complete adapter is:

```python
"""Execute the application with controlled process termination."""

from azure_devops_backlog_generator.main import run_process

if __name__ == "__main__":
    raise SystemExit(run_process())
```

The executable path invokes `run_process()` exactly once and uses its returned integer directly as the
`SystemExit` code, without reinterpretation:

| Existing callable outcome | Executable adapter outcome | Operating-system process exit status |
|---------------------------|----------------------------|--------------------------------------|
| Exact integer `0` | `SystemExit(0)` | `0` |
| Exact integer `1` | `SystemExit(1)` | `1` |

The adapter does not call `main()` or `coordinate_application_bootstrap()` directly, inspect lower-layer
exceptions, add result mappings, classify failures, translate exceptions, retry or fall back. It emits no
stdout, stderr or logging and does not duplicate controlled reporting.

`SystemExit` ownership belongs exclusively to the executable adapter. The existing
`run_process() -> int`, `main() -> None`, `coordinate_application_bootstrap(...) -> None`,
`coordinate_application_run(...) -> None` and Generator orchestration/traversal `None` return contracts
remain unchanged. Neither those callables nor the Generator, REST Client, Documentation Processor
or domain models acquire executable termination responsibilities.

Import safety is implemented and tested for ordinary `import azure_devops_backlog_generator` and
`import azure_devops_backlog_generator.__main__`. Neither import executes the application, invokes
`run_process()`, `main()` or bootstrap, raises `SystemExit`, emits stdout/stderr or produces
adapter-controlled logging. The `if __name__ == "__main__":` guard in `__main__.py` restricts application
execution to executable entry semantics; ordinary import remains safe.

The adapter does not parse or alter CLI arguments. Existing `main()` behaviour continues to pass
`sys.argv[1:]` to bootstrap. In particular,
`python -m azure_devops_backlog_generator --config-file <path>` uses the existing configuration
loader semantics. No CLI option, positional argument, environment-variable meaning or configuration
field is added; `AZDO_PAT` remains the sole credential source.

Controlled success exits with status `0`, empty stdout and empty stderr, with no success/lifecycle event.
A controlled failure exits with status `1`, empty stdout and exactly the existing fixed category-only
stderr line followed by one newline, owned by `run_process()`. The adapter adds no traceback or duplicate
output. The seven categories/messages in Section 7.1.6 remain unchanged; no eighth unexpected-exception
category exists. Success subprocess evidence validates the adapter boundary, not successful application E2E.

Slice 7 preserves the approved D1–D5 runtime logging decisions and all Section 7.1.6 semantics:
logger `azure_devops_backlog_generator`, file
`<validated logging.log_directory>/azure-devops-backlog-generator.log`, append mode, UTF-8, configured
threshold, fixed formatter, `propagate=False`, controlled `CRITICAL` events, exactly one active
application-owned handler, stale owned-handler cleanup before configuration loading, owned-handler-only
dispatch and unchanged `logging.raiseExceptions`. The adapter does not initialise logging, add handlers
or emit duplicate, lifecycle or traceback events. `ApplicationLoggingError` remains runtime logger
initialisation-only; there is no root/console fallback. Under D5, a secondary controlled-event write
failure preserves the primary category, original stderr and returned integer `1`, without additional
output, retry, fallback or substitution with `ApplicationLoggingError`; the adapter translates that
integer directly into `SystemExit(1)`. Controlled stderr and category-only log-event secret-safety remain intact.

**S7-D2 — Interim unexpected-exception executable behaviour.** If `run_process()` raises unexpectedly,
the exact same exception object propagates out of the executable adapter. The adapter does not catch it,
introduce a generic `Exception` catch, classify it as controlled, render a fixed generic message,
sanitise or rewrite it, log a traceback, or manufacture a result. No integer has returned, so the adapter
does not construct controlled `SystemExit(0)` or `SystemExit(1)`.

The adapter's same-object propagation remains unchanged if `run_process()` itself raises. Slice 9 now
handles otherwise-unclassified application `Exception` instances inside `run_process()`, returning `1`
with fixed stderr and no native traceback on the supported handled-Exception package path. This resolves
that path's interim traceback limitation. Direct lower-level calls and adapter-only tests substituting
`run_process()` retain their separate propagation boundary; arbitrary Python invocation paths have no
traceback-suppression guarantee. Slice 7 adds no sanitisation policy.

Existing setuptools src-layout/package discovery includes `__main__.py`. Slice 7 changes no packaging
metadata, dependency or package version and adds no `[project.scripts]`, console script, installed launcher,
second executable surface or direct-execution guard in `main.py`. Direct execution of `main.py`, including
`python src/azure_devops_backlog_generator/main.py`, is not the supported interface. README invocation
documentation remains unchanged.

The executable adapter owns process-specific termination only; `run_process()` retains process
outcome/reporting ownership. Application-wide logging remains operational infrastructure and shared
Application Core remains presentation-neutral. Generator, REST, Documentation and domain layers remain
free of stdout/stderr, `SystemExit` and process-result semantics. A future GUI or alternate adapter may
reuse application/core functionality without using `__main__.py`; no GUI implementation, framework
or Version 1.0 GUI scope is approved.

Slice 7 excludes success/lifecycle logging, new logfile events, execution summaries, result models,
created/reused/repaired counts, Generator return-type changes, unexpected controlled handling, traceback
persistence or sanitisation, diagnostic allowlists, correlation/incident IDs, new controlled categories,
new CLI frameworks/options, retry, fallback, rollback, compensation, continuation after failure, alternate
credentials, PAT in CLI/TOML, dry-run, Generator toggles, dependencies and REST changes.
Execution-summary content and presentation remain future; typed execution-result/aggregation and
created/reused/repaired counts remain conditional on later summary requirements.
Broader integration/E2E, live Azure DevOps Services validation, Operational Readiness,
API Section 6.1 status-drift reconciliation before Review Gate 3, Gate 3 and final Version 1.0 release
readiness remain future. Console-script packaging requires separate approval; GUI implementation remains future.
The implemented package surface and controlled OS exit statuses support subprocess validation and operator
invocation without establishing readiness. Version 1.0 remains pre-release.

---

### 7.1.8 Application/Run Slice 8 — Process-Neutral Application Lifecycle File Logging

**IMPLEMENTED.** Application/Run Slice 8 was merged in PR #141 (implementation commit `378e2b1`,
merge `8560a89`), following contract PR #139 and approval PR #140. Slices 1–9 are implemented.
S8-D1, S8-D2 and S8-D3 below remain the approved, implemented owner decisions. The Slice-8 status-sync
revision 2.39 is Approved Baseline; revision 2.42 is Approved Baseline.

**S8-D1 — Lifecycle boundary and exact events.** Slice 8 shall add exactly two fixed-message lifecycle
events at the configured application-run boundary:

| Event | Exact message | Level | Timing |
|-------|---------------|-------|--------|
| START | `Application run started.` | INFO | After configuration load/validation and runtime logging initialisation succeed, immediately before `coordinate_application_run(configuration)`. |
| COMPLETION | `Application run completed successfully.` | INFO | Only after `coordinate_application_run(configuration)` returns normally, before bootstrap returns successfully to `main()`/`run_process()`. |

START means configured application execution is about to begin, not process startup. There is no separate
configuration-validation or logger-initialised event. Each invocation has at most one eligible START and
at most one eligible successful COMPLETION. For each eligible configured execution attempt, exactly one
START emission attempt shall occur when INFO passes the configured threshold; exactly one COMPLETION
emission attempt shall occur when INFO passes that threshold and application execution returns normally.
A successful write produces one corresponding record. Neither event contains dynamic values.
Completion establishes only normal return, not any created, reused, repaired, skipped or total item count.

**S8-D2 — Severity and filtering.** Both lifecycle events shall use INFO and normal existing
`logging.level` filtering before owned-handler delivery. At INFO (or DEBUG), the records are eligible;
at WARNING, ERROR or CRITICAL, lifecycle INFO records are filtered and no lifecycle write attempt is
required. INFO shall not be forced through a higher threshold. No special lifecycle threshold,
configuration field or logging-level semantic change is introduced. Existing controlled CRITICAL
event behaviour remains unchanged.

**S8-D3 — Lifecycle write-failure behaviour.** The two lifecycle events are best effort. A failed
START write shall still allow configured application execution; a failed COMPLETION write shall still
allow bootstrap to return normally. A lifecycle write failure shall not change the underlying
application outcome, `run_process()` result or adapter `SystemExit` status. It shall not raise or
substitute `ApplicationLoggingError`, convert success to controlled failure, propagate the secondary
write error, emit stdout/stderr, retry, fall back, use another logfile/destination, use root or console
logging, emit a second event, emit logging-internal diagnostics/tracebacks or expose exception details.
This does not suppress a later, independently eligible COMPLETION or an existing controlled-failure
event: those retain their own boundary semantics. `ApplicationLoggingError` remains initialisation-only.
Slice-6 D5 remains authoritative for secondary controlled-failure writes; S8-D3 extends best-effort
handling only to the two new lifecycle events.

Lifecycle ownership belongs to `coordinate_application_bootstrap(...)`, which uses the private
`_emit_lifecycle_event()` helper in `src/azure_devops_backlog_generator/main.py`; no public API was added.
The helper checks both logger INFO eligibility and the active owned handler's threshold before direct
delivery. It catches `Exception` only around lifecycle emission, outside configured application execution;
`KeyboardInterrupt` and `SystemExit` remain unsuppressed. The implemented path preserves the existing
sequence, with only the two approved observations added after logging initialisation:

```text
python -m azure_devops_backlog_generator
→ __main__.py → run_process() → main()
→ coordinate_application_bootstrap(sys.argv[1:])
→ deactivate previous owned logging
→ load/validate Configuration
→ initialise runtime file logging
→ eligible INFO START attempt
→ coordinate_application_run(configuration)
  → DocumentationProcessor → AzureDevOpsRestClient → Generator orchestration
→ eligible INFO COMPLETION attempt only after normal application return
→ normal bootstrap return
```

Lifecycle records shall be delivered only to the current invocation's active application-owned handler.
Normal logger propagation is not the delivery mechanism. Configured-level filtering must apply before
this owned-handler-only dispatch; root, unrelated and same-named non-owned handlers shall receive no
lifecycle records and remain untouched. Repeated invocations shall not reuse stale owned handlers or
produce duplicate lifecycle records.

| Failure boundary | Lifecycle behaviour | Preserved outcome |
|------------------|---------------------|-------------------|
| Configuration load/validation fails | No START, COMPLETION or lifecycle logfile attempt. | Existing `ConfigurationError` process behaviour; no fallback logger. |
| Runtime logging initialisation fails | No START or COMPLETION. | Existing initialisation-only `ApplicationLoggingError` behaviour; no fallback. |
| Controlled application failure after START | START may have been written if INFO was eligible; COMPLETION is absent. | Exactly the existing controlled CRITICAL attempt, fixed category-only stderr line, result `1` and adapter `SystemExit(1)`; no duplicate controlled event. |
| Unexpected application failure after START | START may have been written if INFO was eligible; COMPLETION is absent. | The exact same exception object propagates through bootstrap to its caller. At `run_process()`, implemented Slice 9 adds the best-effort CRITICAL unexpected event, fixed stderr and result `1`; the unchanged adapter produces `SystemExit(1)`. |

All Slice-6 D1–D5 semantics in Section 7.1.6 remain unchanged: standard-library logging only, logger
`azure_devops_backlog_generator`, file
`<validated logging.log_directory>/azure-devops-backlog-generator.log`, file-only append mode, UTF-8,
formatter `%(asctime)s %(levelname)s %(name)s %(message)s`, date format `%Y-%m-%dT%H:%M:%S`,
configured threshold, `propagate=False`, no root emission or console handler, one active owned handler
per invocation, stale owned-handler cleanup before configuration load, and removal/closure of only
owned handlers. Controlled category-only CRITICAL events, owned-handler dispatch, unchanged
`logging.raiseExceptions`, initialisation-only `ApplicationLoggingError`, and no retry, fallback or
alternate destination are preserved. The exact seven categories/messages in Section 7.1.6 remain
authoritative; lifecycle write failure introduces no eighth category.

`run_process() -> int` retains controlled classification, outcome mapping, stderr reporting and the
existing controlled-failure logging trigger. `main() -> None` retains argument delegation.
`coordinate_application_bootstrap(...) -> None`, `coordinate_application_run(...) -> None` and
Generator orchestration/traversal `None` contracts are unchanged. `__main__.py` remains the sole
executable adapter and exclusive `SystemExit` owner; the only supported executable surface remains
`python -m azure_devops_backlog_generator`. No lifecycle implementation is required in that adapter,
`run_process()`, Generator, REST Client, Documentation Processor or domain models. No
`[project.scripts]`, console script, installed launcher, `main.py` execution guard or second surface is added.

Successful stdout/stderr remain empty; controlled failures retain empty stdout and exactly the existing
category-only stderr line. Slice 8 adds no user-facing output or unexpected diagnostic event. Slice 9
now supplies the fixed unexpected report and suppresses native traceback output on the supported
handled-Exception `run_process()`/package path. Direct lower-level unexpected propagation remains unchanged.

The two lifecycle message strings shall contain no PAT, Authorization value, configuration value, path,
filename, document/work-item title, source identity, URL, Azure DevOps organisation/project, exception
string/repr, traceback, counter or arbitrary user content. Their fixed-message safety requires no dynamic
secret sanitisation and makes no claim about native unexpected traceback safety.

Shared Application Core remains presentation-neutral. Lifecycle file logging is process-neutral
operational infrastructure, independent of `SystemExit`, stdout, stderr, console UI and terminal
formatting. Future GUI/alternate adapters may reuse application/core behaviour without `__main__.py`
or `run_process()` where architecture permits; no GUI implementation or Version-1.0 GUI scope is added.

Generator remains unchanged: no result model, count aggregation, callbacks, per-item instrumentation,
traversal/preflight/relationship-lifecycle changes, or retry/fallback/rollback changes. REST remains
unchanged: no request/response, URL, response-body, Authorization or PAT logging. No configuration field,
environment variable, logging option, CLI change or dependency is added; `AZDO_PAT` remains the sole
credential source, with no PAT in CLI or TOML. No live Azure DevOps access is required.

Execution-summary content, destination and presentation remain future. Slice 8 defines no summary
message, application/Generator result type or created/reused/repaired/skipped/total counter.
Completion is not an execution summary. It adds no documentation-processing, Azure DevOps communication,
per-item creation/reuse/repair, configuration-validation, logger-initialised or summary events.
It does not complete the broader logging requirements in Section 12; existing controlled-failure
logging remains Slice 6, and other required logging topics remain future where not already implemented.
No unexpected-exception catch, generic stderr/category, exception/traceback logging or persistence,
diagnostic allowlist/model, incident ID or correlation ID is introduced.

Wider Application/Run remains incomplete and Version 1.0 remains pre-release. Remaining summary/logging,
broader integration/E2E, live Azure DevOps Services validation,
Operational Readiness checklist/evidence, Review Gate 3 and final release readiness remain future.
The preceding Approved Baseline did not contain a complete normative Gate-3 acceptance checklist;
Section 13 of this revision defines the Gate-3 framework. Gate 3 remains FUTURE / NOT YET PASSED.
Slice 8 contributes operational execution evidence without completing Gate-3 prerequisites.
Known pre-existing API Section 6.1 status
drift requires separate reconciliation before Review Gate 3; this contract does not edit the API.
Owner-approved G3-D3 places broader Operational Recovery / DR outside V1.0; existing Generator
later-run recovery remains unchanged and is not equivalent to Operational Recovery / DR.

---

### Application/Run Slice 9 — Final Unexpected-Error Handling and Diagnostic Safety

**IMPLEMENTED — APPROVED CONTRACT.** UE-D1–UE-D10 below remain owner-approved and are implemented.
Application/Run Slices 1–9 are implemented. Architecture revision 2.42 is Approved Baseline;
the approved contract remains authoritative and unchanged.

Slice 9 was implemented in PR #148 (implementation commit `738fdc3`, merge `4549eee`). Contract
provenance remains PR #144 (commit `2070425`, merge `4d80b58`) and approval PR #145 (commit `e3e190f`,
merge `fa158d9`); allocation remains PR #146 (commit `720bb68`, merge `e332c69`) and allocation approval
PR #147 (commit `1174bcb`, merge `ea37478`). Production changes are confined to
`src/azure_devops_backlog_generator/main.py`; validation is in `tests/test_main.py` and
`tests/test___main__.py`. Production `__main__.py` remains unchanged.

This section is authoritative for the bounded final process-facing unexpected-error contract.
The merged implementation replaces the earlier process-facing unexpected propagation and native-traceback
limitation only on the supported handled-Exception `run_process()`/package path. Direct lower-level
same-object exception propagation remains unchanged. No Slice 10 has been allocated; future capability
ordering beyond Slice 9 remains undefined.

**UE-D1 — Final catch boundary.** Only `run_process()` shall introduce the generic process-facing
catch for otherwise-unclassified `Exception` instances. It shall catch `Exception`, not `BaseException`,
after existing controlled exception handling. Direct calls to `main()`,
`coordinate_application_bootstrap(...)` and `coordinate_application_run(...)` shall retain normal,
same-object unexpected-exception propagation to their callers. The shared Application Core,
Generator, REST Client, DocumentationProcessor and `__main__.py` shall not gain this generic conversion.
This preserves lower-level reuse by alternate adapters without changing their contracts.

**UE-D2 — Process outcome.** An otherwise-unclassified `Exception` handled by `run_process()` shall
produce exactly integer `1`. The public model remains `0` for success and `1` for failure; no exit code
`2` or additional process-result code is introduced. The existing package adapter shall continue to
use the returned integer unchanged as its `SystemExit` code, yielding `SystemExit(1)` for this path.
`__main__.py` remains the sole application-owned `SystemExit` owner and requires no change.

**UE-D3 — User-facing stderr.** The handled unexpected failure shall produce exactly one fixed stderr
line, `Unexpected application error.`, followed by the normal newline. Stdout shall remain empty.
The message shall contain no dynamic interpolation: no exception type, message, string/repr, cause,
context, traceback, stack, path, source content, configuration value, PAT, Authorization, organisation,
project, URL, document/work-item title or arbitrary user input.

**UE-D4 — File logging.** If runtime logging has successfully initialised for the current invocation
before the unexpected failure, `run_process()` shall attempt exactly one `CRITICAL` logfile event
whose message is exactly `Unexpected application error.`. A successful write produces one record.
Delivery shall use only the active current-invocation application-owned handler. Root, unrelated and
same-named non-owned handlers shall receive nothing. No console fallback, new destination or alternate
logfile is authorised. If current-invocation logging has not successfully initialised, no unexpected-error
logfile event shall be attempted; UE-D3 remains the process-facing report. The existing configured
threshold applies; CRITICAL remains eligible at every supported logging level.

**UE-D5 — Native traceback policy.** An unexpected `Exception` handled by `run_process()` on the
supported package execution path shall not escape to produce native Python traceback output.
Neither stderr nor the application logfile shall contain its traceback. The observable failure shall
be the fixed stderr line, integer result `1` and, when runtime logging is active, the best-effort
CRITICAL event in UE-D4. The existing adapter then produces `SystemExit(1)`.
This contract replaces the interim native-traceback behaviour only for the supported process-facing
handled-Exception path. Direct lower-level callers still receive exceptions under UE-D1; no guarantee
of traceback suppression is made for arbitrary Python invocation paths. Merged implementation and
validation resolve the previous exposure for the supported handled-Exception path only.

**UE-D6 — Diagnostic content and secret safety.** For the final Version-1.0 process-facing generic
unexpected fallback, the fixed category message `Unexpected application error.` is the approved safe
operational diagnostic and fulfils the sufficient-diagnostic-information requirement in Section 11
for this bounded fallback. Arbitrary exception detail and tracebacks are intentionally excluded because
the repository does not define a safe redaction contract. No claim is made that such detail is safe.

Neither reporting nor logging shall include `str(exc)`, `repr(exc)`, exception class name, arguments,
cause/context, `exc_info`, traceback, stackframes, filesystem paths, configuration values, response
or request bodies, URLs, source identities, titles, user data or credentials, including PAT and
Authorization. The existing logfile timestamp, severity and logger-name fields remain unchanged;
the message contains no dynamic exception diagnostics. This capability defines no redaction algorithm,
sanitised traceback, debug-mode exception detail, diagnostic configuration option or second diagnostic channel.
The implemented fallback excludes arbitrary unexpected exception content and native traceback data
from the supported process-facing handled-Exception path; Testing Section 8 records synthetic
secret-safety and real package-fallback subprocess evidence for this bounded behaviour.

**UE-D7 — Unexpected log-event write failure.** The unexpected application failure is primary.
If its owned logfile emission raises an ordinary `Exception`, the primary unexpected classification
shall remain intact. The application shall still attempt the fixed stderr line and return integer `1`
when stderr delivery remains available. It shall not retry, fall back, use root or console logging,
emit a replacement logfile event, expose the logging exception or traceback, raise
`ApplicationLoggingError`, or create another controlled category. This best-effort rule applies only
to unexpected-error logfile emission and does not redefine Slice-6 controlled-event semantics.

No new stderr-sink recovery semantics are defined. If stderr itself cannot be written, existing
process-environment behaviour remains; no stderr retry or fallback is introduced. The fixed-line/result
guarantee does not authorise suppression or conversion of a separate stderr-delivery failure.

**UE-D8 — Process-control exceptions.** The generic fallback shall catch only `Exception`.
`KeyboardInterrupt`, `SystemExit`, `GeneratorExit` and other `BaseException` subclasses outside
`Exception` shall not be caught or converted. The ordinary-Exception best-effort boundary in UE-D7
does not absorb those process-control exceptions either.

**UE-D9 — Controlled taxonomy and precedence.** Exactly seven controlled process categories remain:

| Controlled category | Unchanged fixed message |
|---------------------|-------------------------|
| `ConfigurationError` | `Configuration error.` |
| `DocumentationProcessingError` | `Documentation processing error.` |
| `AzureDevOpsRestClientError` | `Azure DevOps error.` |
| `SourceIdentityValidationError` | `Source identity validation error.` |
| `ExistingWorkItemResolutionError` | `Existing work item resolution error.` |
| `ConflictingReusedChildRelationshipError` | `Conflicting reused child relationship error.` |
| `ApplicationLoggingError` | `Application logging error.` |

Their existing classification precedence, reporting and integer `1` outcomes shall remain unchanged.
The generic `Exception` fallback shall follow the existing specific controlled handling and shall not
absorb any of these categories. It is a process-facing fallback for otherwise-unclassified exceptions,
not an eighth controlled/domain exception category or a new shared exception hierarchy.

**UE-D10 — Scope and exclusions.** This capability requires no changes to Generator orchestration,
traversal or relationship lifecycle; REST contracts; configuration model or `AZDO_PAT` sourcing;
CLI arguments; DocumentationProcessor; result models; execution summaries; counters or aggregation;
retries or rollback; package launcher; console-script packaging; GUI or alternate adapters.
No created, reused, repaired, skipped or total counts, dependency, configuration field or environment
variable is introduced. The sole approved executable surface remains
`python -m azure_devops_backlog_generator`; no `[project.scripts]`, console script, installed launcher,
`main.py` execution guard or second executable surface is added.

**Composition and existing contracts.** The existing package → `run_process()` → `main()` → bootstrap
→ configuration validation → runtime logging initialisation → eligible START → configured application
run → COMPLETION on normal return → process result → adapter `SystemExit(result)` structure remains.
Only the `run_process()` unexpected-failure boundary gains generic process conversion.

| Condition | Implemented process-facing behaviour |
|-----------|-----------------------------------------|
| Controlled configuration failure | `Configuration error.` plus newline; result `1`; no pre-initialisation file event or generic reclassification. |
| Controlled logging-initialisation failure | Initialisation-only `ApplicationLoggingError`; `Application logging error.` plus newline; result `1`; no unexpected logfile event or generic reclassification. |
| Otherwise-unclassified Exception before logging becomes active | No unexpected logfile attempt; fixed unexpected stderr line; result `1`; adapter `SystemExit(1)`; no native traceback from the handled exception. |
| Otherwise-unclassified application Exception after logging becomes active | Eligible START may exist; no COMPLETION; one best-effort CRITICAL unexpected-event attempt, then fixed unexpected stderr line, result `1` and adapter `SystemExit(1)`; no native traceback from the handled exception. |
| Direct lower-level unexpected failure | Same exception object propagates to the caller; no generic process-facing conversion is added to that boundary. |

Slice 8 remains unchanged: `Application run started.` and
`Application run completed successfully.` are INFO, eligible at DEBUG/INFO and filtered at
WARNING/ERROR/CRITICAL, owned-handler-only and best effort. START follows successful configuration
validation and logger initialisation immediately before configured application execution; COMPLETION
follows only normal configured application return. A configured application failure does not imply COMPLETION.

Slice-6 D1–D5 remain authoritative: standard-library file logging, UTF-8 append mode, validated directory,
existing filename and formatter/date format, configured thresholds, `propagate=False`, owned-handler
isolation, stale-handler cleanup, controlled CRITICAL events, initialisation-only `ApplicationLoggingError`
and existing secondary-write precedence. No global logging setting or existing controlled message changes.

Broader Section-12 logging remains incomplete and separate. The execution summary remains required, undefined and not implemented; no result/count model exists.
The unexpected message is not a summary. No documentation-processing or Azure communication lifecycle
events, work-item creation events, warning taxonomy, richer authentication/authorisation or rate-limit
reporting, summary logging, timings or correlation IDs are defined. API Section 6.1 status reconciliation
remains separate and required before Gate 3; unresolved API reporting requirements remain future contract work.

Review Gates 1 and 2 remain PASS; Review Gates 3 and 4 remain future. Wider Application/Run remains
incomplete and Version 1.0 remains pre-release. This capability is required before final Version-1.0
readiness but does not establish Operational Readiness, a Gate-3 checklist, integration/E2E completion,
live Azure validation or RC readiness. Owner-approved G3-D3 places broader Operational Recovery / DR
outside V1.0; existing Generator recovery requirements remain unchanged. UE-D1–UE-D10 leave no unresolved owner decision
for this bounded Slice-9 capability; implementation is complete under the approved contract. Revision 2.42
is Approved Baseline.

Testing Section 8 records merged Slice-9 evidence: 84/84 combined focused application/package tests
(73 in `tests/test_main.py`, 11 in `tests/test___main__.py`), Ruff passed, 764/764 full pytest and
764/764 `pytest -W error`, each full run with zero failed, skipped, warnings, xfail or xpass. Coverage
is 95% across 1,394 statements with 64 missed; `main.py` is 110/0/100% and `__main__.py` is 3/0/100%.
No live Azure DevOps operations occurred. These are recorded implementation results, not new runs for
this documentation status sync.

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
- Providing complete non-root Parent-Child Relationship lifecycle coordination for an already-resolved candidate. Identity resolution remains upstream. For NEW resolution, the lifecycle coordinator performs persistent Create exactly once, uses the returned Work Item ID and Create revision for one immediate Parent-Child Relationship PATCH, and returns successfully only after that PATCH succeeds. The NEW branch performs no relationship-state GET, classification, reused-child gate call or post-PATCH reread. For REUSED resolution, the coordinator retrieves fresh relationship state exactly once, classifies it exactly once and invokes the existing reused-child descendant gate. CORRECT continues without relationship mutation, MISSING delegates to existing recovery using the fresh relationship-state revision, and CONFLICTING raises `ConflictingReusedChildRelationshipError`. Successful REUSED return occurs only after the gate succeeds. The coordinator returns only the eligible child Work Item ID because a revision may be stale after relationship PATCH; later descendant processing requires the eligible ID only. The non-root coordinator performs neither WIQL nor identity resolution, descendant processing, callbacks or recursive traversal. It introduces no retry, reread, rollback, deletion compensation or alternate credentials. If NEW Create succeeds and relationship PATCH fails, the invocation fails; a later source-identity resolution can discover the created Work Item as reused, then fresh relationship evidence and existing reused-child logic repair, continue or block as MISSING, CORRECT or CONFLICTING requires. This rerun safety arises from identity resolution plus fresh relationship evidence, not coordinator-level retry. Application/Run Slice 1 composes this coordinator without changing its responsibilities.
- Providing implemented root existing/new Work Item lifecycle coordination. The root-only coordinator invokes existing/new resolution once; for NEW it passes the exact supplied candidate and PAT to persistent Create once and returns the Create response ID, while for REUSED it returns the validated existing ID without Create. It returns no revision and performs no relationship-state GET, classification, gate, Parent-Child Relationship PATCH, descendant processing, validation-only Create or compatibility orchestration. Resolution and Create failures propagate without retry, fallback, reread, rollback, deletion compensation or other compensation. Application/Run Slice 1 composes this coordinator without changing its responsibilities.
- Preventing duplicate work item creation.
- Providing implemented full preflight coordination through the mutation barrier. `coordinate_full_preflight` first validates run-wide source identities, then constructs every candidate in deterministic source order, retrieves and retains canonical project evidence, retrieves required work-item-type and field metadata, evaluates structural Scrum compatibility, and submits every exact candidate through validation-only Create in that order. It returns immutable, slotted `PreflightState` evidence containing the original `DocumentationHierarchy`, the canonical `AzureDevOpsProject` and the exact candidate tuple. Source-identity failure occurs before REST activity; later preflight failures propagate unchanged, stop subsequent preflight operations and introduce no retry, fallback, rollback, compensation, credential switching or continuation. The final successful validation-only Create reaches the mutation barrier; no WIQL lookup, Work Item GET, persistent Create, relationship-state GET, relationship PATCH, lifecycle invocation or persistent hierarchy traversal occurs in this coordinator.
- Providing implemented deterministic hierarchy traversal and Generator composition. `coordinate_deterministic_hierarchy_traversal` first validates that the semantic-item sequence and retained `PreflightState` candidate tuple have equal cardinality and positionally matching source identities, before any persistent REST operation. It then processes documents, roots and descendants in deterministic depth-first preorder, using the exact validation-only checked candidates without reconstruction. Roots delegate exactly once to the root lifecycle coordinator; each non-root resolves exactly once and delegates to the non-root lifecycle coordinator with its eligible direct parent ID. Descendants begin only after eligibility. Failures propagate globally without retry, rollback, compensation or continuation; existing lower-level lifecycle behaviour composes later-run MISSING recovery, CORRECT continuation and CONFLICTING stop. Preflight project, metadata, compatibility and validation-only operations are not repeated. `coordinate_generator_orchestration` is the implemented final Generator-owned entry coordinator: it passes the exact `DocumentationHierarchy`, REST client and PAT to full preflight once, passes the exact returned `PreflightState`, REST client and PAT to traversal once, and returns `None`. Successful full preflight is the required mutation barrier before traversal; a preflight failure prevents traversal and persistence. Implemented full-orchestration coverage proves malformed-response, HTTP `401` and HTTP `403` propagation with no retry, alternate credential, PAT event leakage or later descendant, sibling, root, document or persistence operation. Generator Orchestration implementation and required pre-Review-Gate-2 composition coverage are complete. Review Gate 2 completed with PASS, zero findings and no required remediation. Application/Run Slice 1 is implemented and does not own this Generator-internal sequencing; the wider Application/Run phase remains incomplete and Review Gate 3 remains future.

---

## 7.5 Azure DevOps REST Client

The Azure DevOps REST Client manages communication with Azure DevOps.

Version 1.0 shall target Azure DevOps Services only and shall use the Azure DevOps Services organisation/project model. The Services REST base address shall be derived from the configured organisation according to the official Azure DevOps Services URL structure.

Azure DevOps Server instance, port, collection and Server-specific base-address handling are outside Version 1.0 architecture scope.

The REST Client Foundation shall provide a small internal, purpose-specific transport interface. It shall use `urllib` from the Python standard library and shall not introduce a third-party HTTP dependency. It shall own Azure DevOps Services URL construction, HTTP request construction and transmission, Basic authentication-header construction, required common headers, JSON transport mechanics, the fixed timeout, expected-status validation, redirect rejection, no-retry behaviour, controlled transport, network and response failures, and secret-safe diagnostics. It shall not be a general-purpose public HTTP abstraction.

Each request shall use the `urllib` request/response lifecycle independently. The response body shall be consumed and the response closed during request processing. The foundation shall not retain response objects, a persistent session, cookie state, redirect state, a connection pool or other persistent mutable request state. Endpoint-specific public operations include compatibility validation, WIQL, Work Item GET, Persistent Work Item Create, Parent-Child Relationship PATCH and reused-child relationship-state GET REST transport. Persistent Create reuses the approved JSON Patch builder and returns structurally validated `AzureDevOpsWorkItem` evidence; the REST Client remains transport-only. Parent-Child Relationship JSON Patch construction and HTTP PATCH transport are implemented. The transport reuses the approved JSON Patch builder and this REST Client foundation with the fixed `/rev` `test`, `/relations/-` `add`, `System.LinkTypes.Hierarchy-Reverse` relation and absolute organisation-scoped parent target URI. Its exact `200 OK` response has a non-empty valid UTF-8 JSON object body; no response property is required, unknown properties are ignored and the REST Client returns `None` after validation. The reused-child relationship-state GET requests `$expand=relations`, validates the child ID, fresh revision and relation structure, validates and parses exact reverse-hierarchy target URIs, and returns ordered duplicate-preserving reverse-parent IDs. Generator-level intended-parent comparison and relationship-state classification are implemented. The Backlog Generator, not the REST Client, owns sequencing and lifecycle policy; the REST Client only executes requested authenticated transport, serialization and response validation. The implemented `coordinate_generator_orchestration` composes full preflight through the mutation barrier into deterministic hierarchy traversal without changing REST endpoint contracts. Application/Run Slice 1 composes the REST client without changing its transport boundary.

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

Application/Run Slice 1 begins only after configuration loading, validation and PAT validation have
completed. Its composition sequence is documentation processing, REST-client construction, Generator
invocation and `None` return. Logging, reporting and process-exit behaviour remain outside this slice.

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

For the final Version-1.0 process-facing generic unexpected fallback, the owner-approved
[Application/Run Slice 9 — Final Unexpected-Error Handling and Diagnostic Safety](#applicationrun-slice-9--final-unexpected-error-handling-and-diagnostic-safety)
contract defines the fixed safe category message as the sufficient operational diagnostic. Dynamic
exception detail and tracebacks are intentionally excluded without a safe redaction contract.
This bounded policy is implemented for the supported handled-Exception `run_process()`/package path and does not change direct lower-level exception propagation.

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

# 13. Review Gate 3 Operational Readiness Boundaries

**DRAFT PROPOSAL - pending owner review; Gate 3 has not passed.** This section proposes
operational acceptance assignments for existing Version-1.0 requirements. It does not approve
new behavioural contracts. The authoritative acceptance matrix, decision register and PASS rules
are in [Release Section 8.1](07-Release.md#81-review-gate-3-operational-readiness-acceptance).
[Testing Section 9.1](06-Testing.md#91-review-gate-3-evidence-requirements) owns evidence requirements.

Gate 3 asks whether the application is operationally complete and sufficiently evidenced to enter
final release-candidate validation. It is not final Version-1.0 approval. Existing normative sources
remain PRD FR-001 to FR-010 and NFR-001 to NFR-007, this Architecture, API Sections 5 to 11,
Configuration Sections 5 to 8 and Testing Sections 5 to 9. Their assignment to Gate 3 is newly proposed
unless already explicit, notably API Section 6.1 status reconciliation before Gate 3. Owner-approved
G3-D1 to G3-D3 now settle summary/live-proof placement and broader DR exclusion; this document remains Draft.

## 13.1 Logging acceptance boundary

Before PASS, each applicable Section-12 topic shall have an approved interpretation and evidence
against that interpretation. Existing Slice-6/8/9 behaviour shall be credited without reimplementation.
Unresolved topics require separate behavioural contracts followed by any required implementation
and validation. No event is required merely because it is imaginable. Owner-approved G3-D1 requires
the complete summary contract, implementation, validation and evidence before Gate-3 PASS.

| Topic | Proposed Gate-3 acceptance rule | Current evidence / remaining definition |
|-------|---------------------------------|-----------------------------------------|
| Startup | Preserve configured-run START after successful configuration validation and logger initialisation. | SATISFIED: Slice 8; no earlier bootstrap event is implied. |
| Configuration validation | Preserve stderr-only pre-initialisation failure; approve whether START is sufficient evidence of successful validation. | DECISION REQUIRED: a separate success event is not yet required. |
| Documentation processing | Approve and evidence minimum processing observability under Section 12, including existing terminal failure reporting. | PARTIALLY SATISFIED: failure category exists; minimum successful processing evidence remains undefined. |
| Azure DevOps communication | Approve and evidence minimum communication/result observability consistent with API Sections 6, 9 and 10. | PARTIALLY SATISFIED: generic terminal failure exists; further event content and boundaries remain undefined. |
| Work-item creation | Approve creation-event granularity and safe evidence of successful creation. | NOT SATISFIED: per-item versus aggregate evidence remains undefined; no counts are mandated. |
| Warnings | Approve applicable warning conditions and their evidence, or explicitly justify that no distinct warning condition applies under current V1.0 contracts. | DECISION REQUIRED: no warning taxonomy exists; do not invent business rules. |
| Controlled errors | Preserve the seven approved categories, exact current reports and eligible owned-handler CRITICAL events until an approved reporting revision applies. | SATISFIED for Slice 6; HTTP reconciliation remains separate. |
| Unexpected errors | Preserve UE-D1 to UE-D10, fixed fallback and owned-handler best-effort CRITICAL event. | SATISFIED: Slice 9, including handled-Exception traceback suppression. |
| Successful completion | Preserve normal-return-only INFO COMPLETION and configured filtering. | SATISFIED: Slice 8; this is not an execution summary. |
| Execution summary | Complete the separately approved summary contract, implementation, validation and evidence before Gate-3 PASS under owner-approved G3-D1. | NOT SATISFIED: behaviour remains undefined and unimplemented; CONTRACT, IMPLEMENTATION and VALIDATION remain required. |
| Authentication/authorisation | Meet the reconciled API reporting contract in Section 13.2. | PARTIALLY SATISFIED: status retained, current terminal reporting generic. |
| Rate limiting | Meet API Section 11 through approved identifiable rate-limit logging, preserving fail/no-sleep/no-retry behaviour. | PARTIALLY SATISFIED: generic failure exists; reporting contract and event remain outstanding. |
| Diagnostic safety | Preserve safe existing messages and prove secret safety for every newly approved event. | PARTIALLY SATISFIED: existing fixed events evidenced; future content requires validation. |
| Destination | Preserve the validated directory, fixed UTF-8 append logfile, owned-handler isolation and no fallback destination. | SATISFIED: Slice 6 and Configuration Section 6.4. |
| Levels | Preserve configured thresholds, INFO lifecycle and CRITICAL terminal events; approve levels for any new events. | PARTIALLY SATISFIED: current levels evidenced; new-event levels undefined. |

Further logging contracts shall define trigger, timing, content, level, ownership, filtering and
write-failure behaviour. They shall state which existing event satisfies a topic and prevent duplicate
terminal reporting. File logging remains operational infrastructure; user-facing presentation and
process termination shall not move into the shared Application Core or Generator. Generator-owned
creation/reuse/relationship decisions shall not be inferred from a successful application return.

## 13.2 HTTP reporting and execution-summary dependencies

Before Gate-3 PASS, an Approved Baseline behavioural contract shall reconcile API Section 6.1
`401` authentication-failure reporting, `403` authorisation-failure reporting and Section 11 rate-limit
logging with the current generic `Azure DevOps error.` process/log event. Its required implementation
shall be merged and its evidence recorded. Exact messages, channels, levels and interaction with existing
reports require separate approval; this gate contract does not select them. HTTP status retention and
no-retry behaviour already exist. No new exception taxonomy is proven necessary. Optional safe
`Retry-After` diagnostics do not authorise sleep or retry. API Section 6.1 implementation-status
reconciliation remains mandatory separate documentation work before PASS; the API is not edited here.

The execution summary remains mandatory under Sections 8 and 12. G3-D1 is RESOLVED / OWNER APPROVED:
its contract, implementation, validation and evidence shall be complete before Gate-3 PASS. Unfinished
summary functionality shall not be deferred to Gate 4; final RC regression may repeat its validation. Its separate
contract shall settle content, destination, timing, success/failure applicability, partial-result
semantics, safety and delivery-failure behaviour. It shall decide whether counts and Generator outcome
information are necessary. No created/reused/repaired/skipped/total counts, typed result model or interface
change is mandated here. API Section 7.1's summary/completion wording shall be reconciled with the
mandatory summary requirement; Slice-8 COMPLETION shall not silently substitute for a summary.

## 13.3 Runtime, safety and recovery boundaries

G3-D2 is RESOLVED / OWNER APPROVED: minimum real Azure DevOps Services operational proof shall exist
before Gate-3 PASS; mock-only evidence is insufficient. Testing Section 9.1 defines the minimum scope.
The exact isolated environment and controlled procedure still require preparation before execution.
Final live-validation repetition and explicitly allocated remaining release scenarios belong to Gate 4.

Gate-3 acceptance shall preserve the approved package surface, configuration selection, integer outcomes,
exclusive adapter SystemExit ownership and direct lower-level propagation. It shall preserve `AZDO_PAT`
as the sole credential source, no PAT in TOML/CLI, no PAT or Authorization diagnostics, HTTPS,
redirect/proxy protections, fixed existing reports and bounded handled-Exception traceback suppression.
New logging/reporting/summary and live-test evidence shall be secret-safe; no redaction framework is
introduced. Process-control exceptions and existing stderr-delivery boundaries remain unchanged.

Acceptance shall preserve preflight before mutation, global fail-fast, accepted partial remote state,
identity-based reuse and fresh MISSING/CORRECT/CONFLICTING relationship handling. No automatic retry,
rollback, compensating mutation, credential switching or generic remote-state repair is authorised.
G3-D3 is RESOLVED / OWNER APPROVED: broader Operational Recovery / Disaster Recovery is OUTSIDE V1.0,
not deferred to Gate 4. V1.0 requires no new backup/restore or DR infrastructure, generic recovery
subsystem, logfile recovery/rotation capability or dedicated DR platform/service. Narrow Generator
rerun recovery remains unchanged and is not equivalent to operational DR. Operator guidance shall
explain the bounded failure/rerun model under Release row L; row J retains its validation obligations.
The scope decision does not establish completion of either row.

This proposal introduces no new configuration, environment variable, dependency, launcher, public
exception or result interface. It requires neither architectural refactoring nor test reorganisation.
No Slice 10 has been allocated. Broader behavioural definitions and gate acceptance remain separate
from the implemented, approved Slices 1-9.

---

# 14. Extensibility

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

# 15. Architecture Traceability

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

# 16. Approval

Approval of a document version requires:

- Completion of the editorial review.
- Approval of that document version.
- Creation of the corresponding Approved Baseline.
- Commit to the project repository using the agreed Git workflow.

The document metadata and Version History record whether the current version has completed this approval process.

Subsequent modifications shall follow the established documentation governance process and be recorded through Version History.
