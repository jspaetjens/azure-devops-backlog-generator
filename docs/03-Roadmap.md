# Azure DevOps Backlog Generator

# Development Roadmap

> *This document defines the phased implementation plan for Version 1.0 of the Azure DevOps Backlog Generator.*

**Version:** 1.29

**Status:** Draft

**Last Updated:** 2026-09-04

**Target Release:** v1.0.0

**License:** MIT

**Author:** Jack Spaetjens

---

# Version History

| Version | Date | Status | Author | Description |
|----------|------------|-------------------|-----------------|------------------------------------------------|
| 0.1 | 2026-07-31 | Draft | Jack Spaetjens | Initial Development Roadmap. |
| 1.0 | 2026-07-31 | Approved Baseline | Jack Spaetjens | Initial approved Development Roadmap baseline. |
| 1.1 | 2026-08-27 | Approved Baseline | Jack Spaetjens | Recorded the current implementation baseline and remaining Version 1.0 work. |
| 1.2 | 2026-08-27 | Approved Baseline | Jack Spaetjens | Recorded merged WIQL identity lookup and Work Item GET evidence retrieval in the current implementation baseline. |
| 1.3 | 2026-08-27 | Approved Baseline | Jack Spaetjens | Recorded merged existing/new Work Item resolution in the current implementation baseline. |
| 1.4 | 2026-08-28 | Approved Baseline | Jack Spaetjens | Recorded merged Persistent Work Item Create transport in the current implementation baseline. |
| 1.5 | 2026-08-28 | Approved Baseline | Jack Spaetjens | Recorded merged Parent-Child Relationship JSON Patch construction in the current implementation baseline. |
| 1.6 | 2026-08-28 | Approved Baseline | Jack Spaetjens | Recorded merged Parent-Child Relationship HTTP PATCH transport in the current implementation baseline. |
| 1.7 | 2026-08-28 | Approved Baseline | Jack Spaetjens | Recorded merged reused-child relationship-state GET and structural evidence parsing in the current implementation baseline. |
| 1.8 | 2026-08-28 | Approved Baseline | Jack Spaetjens | Recorded merged reused-child relationship-state classification in the current implementation baseline. |
| 1.9 | 2026-08-28 | Approved Baseline | Jack Spaetjens | Recorded completion of the missing-parent recovery ownership governance correction. |
| 1.10 | 2026-08-28 | Approved Baseline | Jack Spaetjens | Recorded merged MISSING missing-parent recovery coordination in the current implementation baseline. |
| 1.11 | 2026-08-29 | Approved Baseline | Jack Spaetjens | Recorded merged reused-child descendant gating, including CORRECT continuation and CONFLICTING blocking decisions. |
| 1.12 | 2026-08-29 | Approved Baseline | Jack Spaetjens | Recorded merged complete non-root Parent-Child Relationship lifecycle coordination and Full Repository Review Gate 1 as next. |
| 1.13 | 2026-08-29 | Approved Baseline | Jack Spaetjens | Synchronized implemented root existing/new Work Item lifecycle coordination status. |
| 1.14 | 2026-08-29 | Approved Baseline | Jack Spaetjens | Recorded approval of the Version 1.0 Generator Orchestration preflight, global fail-fast and composition-ownership contract. |
| 1.15 | 2026-08-29 | Approved Baseline | Jack Spaetjens | Synchronized implemented full preflight coordinator status and the deferred traversal/composition slice. |
| 1.16 | 2026-08-30 | Approved Baseline | Jack Spaetjens | Synchronized implemented deterministic hierarchy traversal while retaining final Generator entry composition before Review Gate 2. |
| 1.17 | 2026-08-30 | Approved Baseline | Jack Spaetjens | Synchronized complete Generator Orchestration implementation status before Review Gate 2. |
| 1.18 | 2026-08-30 | Approved Baseline | Jack Spaetjens | Recorded Generator Orchestration Review Gate 2 PASS with no required remediation. |
| 1.19 | 2026-08-31 | Approved Baseline | Jack Spaetjens | Defined the approved Application/Run Slice 1 implementation sequence. |
| 1.20 | 2026-08-31 | Approved Baseline | Jack Spaetjens | Synchronized implemented Application/Run Slice 1 status while retaining subsequent application/run, readiness and review work. |
| 1.21 | 2026-08-31 | Approved Baseline | Jack Spaetjens | Defined the approved Application/Run Slice 2 configuration-bootstrap contract. |
| 1.22 | 2026-08-31 | Approved Baseline | Jack Spaetjens | Synchronized implemented Application/Run Slice 2 status while retaining subsequent application/run, readiness and review work. |
| 1.23 | 2026-09-01 | Approved Baseline | Jack Spaetjens | Defined the approved Application/Run Slice 3 Process Bootstrap Invocation implementation slice. |
| 1.24 | 2026-09-02 | Approved Baseline | Jack Spaetjens | Synchronized implemented Application/Run Slice 3 Process Bootstrap Invocation status while retaining incomplete wider application/run responsibilities. |
| 1.25 | 2026-09-02 | Approved Baseline | Jack Spaetjens | Defined the Application/Run Slice 4 Controlled Application Outcome Mapping implementation contract. |
| 1.26 | 2026-09-02 | Approved Baseline | Jack Spaetjens | Synchronized implemented Application/Run Slice 4 Controlled Application Outcome Mapping status while retaining incomplete wider application/run responsibilities. |
| 1.27 | 2026-09-03 | Approved Baseline | Jack Spaetjens | Defined the Application/Run Slice 5 Controlled Failure Reporting to Standard Error implementation contract. |
| 1.28 | 2026-09-03 | Approved Baseline | Jack Spaetjens | Synchronized implemented Application/Run Slice 5 Controlled Failure Reporting to Standard Error status. |
| 1.29 | 2026-09-04 | Draft | Jack Spaetjens | Defined the approved but unimplemented Application/Run Slice 6 Runtime File Logging and Controlled-Failure Events contract. |

---

# Table of Contents
- [Azure DevOps Backlog Generator](#azure-devops-backlog-generator)
- [Development Roadmap](#development-roadmap)
- [Version History](#version-history)
- [Table of Contents](#table-of-contents)
- [1. Introduction](#1-introduction)
- [2. Purpose](#2-purpose)
- [3. Roadmap Objectives](#3-roadmap-objectives)
- [4. Development Principles](#4-development-principles)
- [5. Current Implementation Baseline](#5-current-implementation-baseline)
- [6. Development Phases](#6-development-phases)
  - [Phase 1 – Project Foundation](#phase-1--project-foundation)
  - [Phase 2 – Core Infrastructure](#phase-2--core-infrastructure)
  - [Phase 3 – Documentation Processing](#phase-3--documentation-processing)
  - [Phase 4 – Backlog Generation](#phase-4--backlog-generation)
  - [Phase 5 – Validation and Testing](#phase-5--validation-and-testing)
  - [Phase 6 – Release Preparation](#phase-6--release-preparation)
- [7. Phase Deliverables](#7-phase-deliverables)
- [8. Milestones](#8-milestones)
- [9. Dependencies](#9-dependencies)
- [10. Risks](#10-risks)
- [11. Success Criteria](#11-success-criteria)
- [12. Roadmap Traceability](#12-roadmap-traceability)
- [13. Approval](#13-approval)

---

# 1. Introduction

The Development Roadmap defines the planned implementation approach for Version 1.0 of the Azure DevOps Backlog Generator.

It translates the approved Product Requirements Document and Software Architecture Document into a structured sequence of development activities.

The roadmap provides implementation guidance while maintaining alignment with the approved documentation baseline.

---

# 2. Purpose

The purpose of this document is to describe the planned implementation phases for Version 1.0.

The roadmap establishes the order in which functionality will be implemented while supporting incremental development, testing and validation.

---

# 3. Roadmap Objectives

Version 1.0 shall achieve the following objectives:

- Implement all approved functional requirements.
- Follow the approved software architecture.
- Maintain complete traceability to approved documentation.
- Deliver functionality through logical implementation phases.
- Support continuous testing throughout development.
- Produce a maintainable and reusable software solution.

---

# 4. Development Principles

Development shall follow the following principles:

- Documentation-driven development.
- Incremental implementation.
- Modular software design.
- Continuous integration.
- Automated testing.
- Version-controlled development.
- Traceability between requirements and implementation.
- Compliance with the approved documentation baseline.

---

# 5. Current Implementation Baseline

The current implementation baseline includes configuration loading and validation; documentation
discovery, parsing and preparation; source identity and collision validation; the Azure DevOps
REST Client Foundation; project and compatibility metadata retrieval; structural Scrum
compatibility evaluation; Work Item Candidate construction; Work Item Create JSON Patch
construction; validation-only Work Item Create transport; WIQL identity lookup; and Work Item
GET evidence retrieval; existing/new Work Item resolution; Persistent Work Item Create REST transport; Parent-Child Relationship JSON Patch construction; Parent-Child Relationship HTTP PATCH transport; reused-child fresh relationship-state retrieval with structural relationship evidence validation and reverse-parent target-ID extraction; generator-level MISSING, CORRECT and CONFLICTING classification; MISSING recovery coordination using the existing Parent-Child Relationship PATCH with the fresh relationship-state revision; reused-child descendant gating; NEW Create → Parent-Child Relationship PATCH lifecycle sequencing; REUSED relationship-state GET → classify → gate lifecycle sequencing; successful eligibility return only after the relationship state is safe; and root existing/new Work Item lifecycle coordination, in which NEW creates once and REUSED returns the validated existing ID without relationship work.

The planned Relationship Lifecycle and Generator Orchestration implementation clusters are complete. Full preflight validates source identities before REST activity, constructs and validation-only checks every exact candidate in deterministic source order, retains canonical project evidence and returns immutable `PreflightState` evidence at the mutation barrier. The implemented final Generator-owned entry coordinator passes that exact successful `PreflightState` into deterministic hierarchy traversal, which validates the retained candidate/item association before persistence, processes documents, roots and descendants in depth-first source order, delegates roots to their lifecycle coordinator, resolves each non-root once before its lifecycle coordinator, and begins descendants only after parent eligibility. Complete Generator composition is globally fail-fast without retry or continuation across multiple roots and documents. Review Gate 2 completed with PASS, zero findings and no required remediation, including malformed-response and HTTP `401` and `403` full-orchestration failure coverage. Application/Run Slices 1, 2, 3 and 4 are implemented. Operational Readiness and Review Gate 3 remain future, while live end-to-end validation and final release-readiness validation remain incomplete.

Following the successful implementation merge, Application/Run Slice 2 is implemented; the preceding
implementation-plan status is superseded. Application/Run Slice 1 is implemented: an already-validated
`Configuration` is composed into documentation processing, one REST-client construction and one Generator
invocation, with `None` returned on success and unchanged exception propagation on failure. It does not implement
configuration bootstrap, CLI integration, logging/reporting or process-exit mapping.

Application/Run Slice 2 is implemented. It composes:

```text
arguments
-> configuration-file selection/bootstrap
-> validated Configuration
-> Slice 1
-> None
```

It uses the existing configuration-file selection/bootstrap capability and passes the exact returned
validated `Configuration` into Slice 1.

Application/Run Slice 3 — Process Bootstrap Invocation is implemented. It composes only:

```text
process argv
→ argv[1:]
→ existing bootstrap coordinator
→ None / unchanged exception propagation
```

It introduces `main() -> None` as the process-facing callable, acquires `sys.argv[1:]`, and delegates that
resulting sequence directly to `coordinate_application_bootstrap(...)` exactly once. It adds no
direct-execution guard, executable adapter, `__main__.py`, console-script registration, error handling,
process-exit mapping, output, logging or reporting. Controlled process exception classification, process exit-code mapping, user-facing error
reporting, stdout/stderr policy, logging initialisation and failure logging, execution reporting,
unexpected-exception/traceback policy, actual executable adapter, direct execution and/or package
`__main__.py`, console-script packaging if approved, integration/end-to-end validation, Operational Readiness,
Operational Recovery / DR, Review Gate 3 and final release readiness remain future. The wider Application/Run
phase is not yet complete.

Application/Run Slice 4 — Controlled Application Outcome Mapping is implemented. It introduces the separate
`run_process() -> int` wrapper above the implemented `main() -> None`:

```text
run_process()
→ main()
→ controlled application outcome classification
→ 0 or 1 return
```

Successful `main()` completion returns the exact integer `0`; an exception in the approved explicit known
controlled set returns the exact integer `1`; and an exception outside that set propagates unchanged. Slice 4
retains one `main()` invocation and introduces no retry, fallback, output, logging, `SystemExit` or executable
packaging. It preserves `main()` as the `sys.argv[1:]` acquisition and bootstrap-delegation callable, and keeps
CLI/process-specific outcome, reporting and termination behaviour outside the shared Application Core. This
preserves future alternate-interface compatibility without approving or implementing a GUI. User-facing
reporting, stdout/stderr policy, safe rendering, logging, unexpected-exception handling, traceback policy,
executable adaptation, `SystemExit` ownership, direct execution and/or package `__main__.py`, console-script
packaging if approved, integration/end-to-end validation, Operational Readiness, Operational Recovery / DR,
Review Gate 3 and final release readiness remain future.

Application/Run Slice 5 — Controlled Failure Reporting to Standard Error is implemented. It extends the existing
`run_process() -> int` process adapter only as follows:

```text
run_process()
→ controlled failure
→ _render_controlled_failure(error)
→ exact category-only stderr line
→ return 1
```

The six approved categories use only their fixed messages: `Configuration error.`,
`Documentation processing error.`, `Azure DevOps error.`, `Source identity validation error.`,
`Existing work item resolution error.` and `Conflicting reused child relationship error.` Each message is one stderr
line with one newline and contains no exception detail. The renderer exposes no `str(exception)`, `repr(exception)`,
exception arguments, CLI argument text, paths, source-derived content, Azure DevOps URLs, response bodies, headers,
PAT or Authorization values, or arbitrary exception messages. Focused tests prove synthetic sensitive-looking detail
is absent from stderr. Successful execution remains silent, with no stdout or stderr, and returns the exact integer
`0`. `main() -> None`, unchanged unexpected-exception propagation, presentation-neutral shared Application Core
boundaries and future alternate-interface compatibility are preserved. Slice 5 does not introduce logging,
execution summaries, unexpected-exception reporting, tracebacks, `sys.exit` or `SystemExit`, direct execution,
packaging or GUI implementation. Slices 1, 2, 3, 4 and 5 are implemented; the wider Application/Run phase remains
incomplete, and Operational Readiness, Operational Recovery / DR, Review Gate 3, integration/end-to-end and final
release-readiness work remain future.

Application/Run Slice 6 — Runtime File Logging and Controlled-Failure Events is approved but not yet implemented.
It shall initialise one configured application-owned UTF-8 append file handler after successful configuration
loading and validation, using `azure_devops_backlog_generator`, `propagate=False`, the fixed
`azure-devops-backlog-generator.log` filename, the configured logging threshold and a deterministic timestamp,
level, logger-name and message format. Each post-initialisation controlled process failure shall cause exactly one
category-only `CRITICAL` file-event emission attempt; when that attempt succeeds, exactly one record shall be
written. A secondary write failure shall not replace the primary controlled failure, its fixed stderr line or its
`1` outcome. It adds `ApplicationLoggingError` as a seventh controlled process category for logger-initialisation
failure; that error and pre-initialisation configuration failures produce no file event or fallback logging.
Dynamic diagnostics, PAT/Authorization, tracebacks, root/console output and logging-internal stderr diagnostics are
prohibited. Slices 1–5 remain implemented and the wider Application/Run phase remains incomplete. Success/lifecycle
logging, an execution-summary/result contract, unexpected-exception and traceback policy, executable
adapter/SystemExit ownership, packaging/direct execution, integration/E2E, Operational Readiness, Operational
Recovery / DR, Review Gate 3 and final Version 1.0 release readiness remain future.

---

# 6. Development Phases

Version 1.0 shall be implemented through the following development phases.

## Phase 1 – Project Foundation

Objectives:

- Establish the project repository.
- Approve the documentation baseline.
- Configure the development environment.
- Establish development standards.

---

## Phase 2 – Core Infrastructure

Objectives:

- Implement application configuration.
- Implement authentication.
- Establish Azure DevOps REST API connectivity.
- Implement logging.
- Implement error handling.

---

## Phase 3 – Documentation Processing

Objectives:

- Read approved project documentation.
- Interpret the documentation structure.
- Extract backlog information.
- Validate documentation input.

---

## Phase 4 – Backlog Generation

Objectives:

- Generate Azure DevOps work items.
- Create work item hierarchies.
- Populate work item attributes.
- Maintain traceability between documentation and generated work items.

---

## Phase 5 – Validation and Testing

Objectives:

- Execute automated tests.
- Validate generated work items.
- Validate parent-child relationships.
- Verify repeatable execution.

---

## Phase 6 – Release Preparation

Objectives:

- Finalise project documentation.
- Prepare Version 1.0 for release.
- Verify release readiness.
- Publish Version 1.0.

---

# 7. Phase Deliverables

Each development phase shall produce clearly defined deliverables.

| Phase | Deliverables |
|--------|--------------|
| Phase 1 | Documentation baseline, repository structure, development environment |
| Phase 2 | Core application infrastructure |
| Phase 3 | Documentation processing capability |
| Phase 4 | Azure DevOps backlog generation capability |
| Phase 5 | Tested and validated application |
| Phase 6 | Version 1.0 release |

Completion of each phase shall be verified before the next phase begins.

---

# 8. Milestones

The following milestones define the progression of Version 1.0.

| Milestone | Description |
|-----------|-------------|
| M1 | Documentation baseline approved |
| M2 | Development environment established |
| M3 | Azure DevOps connectivity established |
| M4 | Documentation processing completed |
| M5 | Backlog generation operational |
| M6 | Automated testing completed successfully |
| M7 | Version 1.0 approved for release |

Each milestone represents a measurable checkpoint within the development lifecycle and shall be completed before progressing to the next stage where applicable.

---

# 9. Dependencies

Version 1.0 depends upon:

- Approved Product Requirements Document.
- Approved Software Architecture Document.
- Approved Development Standards.
- Azure DevOps REST API availability.
- Azure DevOps project availability.
- Appropriate Azure DevOps permissions.
- Python development environment.
- GitHub repository availability.

Dependencies shall be satisfied before implementation activities that rely upon them commence.

---

# 10. Risks

The successful implementation of Version 1.0 depends upon managing the following project risks.

| ID | Risk | Impact | Mitigation |
|----|------|--------|------------|
| R-001 | Azure DevOps REST API changes | High | Monitor Microsoft API updates and validate compatibility throughout development. |
| R-002 | Incomplete or inconsistent project documentation | High | Maintain approved documentation baselines before implementation. |
| R-003 | Incorrect project configuration | Medium | Validate configuration before execution and testing. |
| R-004 | Insufficient Azure DevOps permissions | Medium | Verify permissions during environment setup. |
| R-005 | Integration defects | Medium | Apply automated testing throughout development. |

Project risks shall be monitored throughout the implementation of Version 1.0.

---

# 11. Success Criteria

The Development Roadmap shall be considered successfully executed when:

- All planned development phases have been completed.
- All approved functional requirements have been implemented.
- The implementation complies with the approved Software Architecture Document.
- Automated testing has been completed successfully.
- Complete traceability has been maintained between documentation, implementation and Azure DevOps.
- Version 1.0 has been approved for release.

---

# 12. Roadmap Traceability

This Development Roadmap translates the approved documentation baseline into an implementation plan.

Traceability shall be maintained between:

- Product Requirements Document
- Software Architecture Document
- Development Roadmap
- Azure DevOps Backlog
- Source Code
- Test Documentation

Implementation activities shall remain fully aligned with the approved documentation baseline throughout the software development lifecycle.

The Development Roadmap shall not introduce functionality that is not traceable to an approved requirement.

---

# 13. Approval

This document becomes part of the approved documentation baseline following:

- Completion of the editorial review.
- Approval of Version 1.0.
- Creation of the Version 1.0 Approved Baseline.
- Commit to the project repository using the agreed Git workflow.

Subsequent modifications shall follow the established documentation governance process and be recorded through Version History.
