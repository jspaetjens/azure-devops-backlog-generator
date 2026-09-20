# Azure DevOps Backlog Generator

# Testing Strategy

> *This document defines the testing approach, quality assurance strategy and validation processes for Version 1.0 of the Azure DevOps Backlog Generator.*

**Version:** 2.39

**Status:** Draft

**Last Updated:** 2026-09-20

**Target Release:** v1.0.0

**License:** MIT

**Author:** Jack Spaetjens

**Revision scope:** This Draft records the Gate-3 application/integration evidence mapping and
historical applicability assessment at `661102d64180417629ee7a96d36ad5bd40ac5a03` in Section 9.4.
The governing Approved Baseline is Architecture 2.48, Roadmap 1.43, API 2.28, Testing 2.38 and
Release 1.37. Existing automated evidence is sufficient for the mandatory application/integration
scenarios; no missing mandatory automated test has been identified. Required live Azure DevOps
Services validation remains pending. This reconciliation awaits document review and baseline promotion.
G3-OWN-D01 to G3-OWN-D14, G3-REC-R01, G3-D1 to G3-D3 and G3-SUM-D1 to G3-SUM-D9 remain unchanged.
[Architecture Section 13.5](02-Architecture.md#135-gate-3-owner-approved-closure-decisions)
retains behavioural authority. Historical slice contracts, return values, exclusions and execution
results retain their original boundaries; Sections 9.2 and 9.3 preserve PR #157 and PR #162 evidence.
Earlier statements of pending implementation or evidence describe their historical baselines;
Section 9.4 records current automated applicability without rewriting those results.
Slices 1–9 remain IMPLEMENTED + APPROVED; Slice 10 remains IMPLEMENTED + AUTOMATED VALIDATION
COMPLETE + Approved Baseline. No Release A–O status changes. Gate 3 remains NOT PASSED,
Gate 4 FUTURE and Version 1.0 PRE-RELEASE. No Slice 11, new behaviour, new test execution or live
operation is introduced or authorised. GUI governance and the G3-D3 exclusion of broader DR are unchanged.

---

# Version History

| Version | Date | Status | Author | Description |
|----------|------------|-------------------|-----------------|------------------------------------------------|
| 0.1 | 2026-07-31 | Draft | Jack Spaetjens | Initial Testing Strategy. |
| 1.0 | 2026-07-31 | Approved Baseline | Jack Spaetjens | Initial approved Testing Strategy baseline. |
| 1.1 | 2026-08-20 | Approved Baseline | Jack Spaetjens | Clarified the Azure DevOps Services-only integration and system-test target for Version 1.0. |
| 1.2 | 2026-08-20 | Approved Baseline | Jack Spaetjens | Defined test coverage for Scrum compatibility validation. |
| 1.3 | 2026-08-21 | Approved Baseline | Jack Spaetjens | Defined test coverage for the Documentation Input Specification contract. |
| 1.4 | 2026-08-21 | Approved Baseline | Jack Spaetjens | Standardised the Approval section to remain valid across Draft and Approved Baseline states. |
| 1.5 | 2026-08-21 | Approved Baseline | Jack Spaetjens | Defined test coverage for the Description Mapping and normative Markdown rendering contract. |
| 1.6 | 2026-08-21 | Approved Baseline | Jack Spaetjens | Defined test coverage for the Acceptance Criteria Mapping contract. |
| 1.7 | 2026-08-21 | Approved Baseline | Jack Spaetjens | Defined test coverage for the Tags Mapping contract. |
| 1.8 | 2026-08-21 | Approved Baseline | Jack Spaetjens | Defined test coverage for the Version 1.0 Work Item Create payload contract. |
| 1.9 | 2026-08-21 | Approved Baseline | Jack Spaetjens | Defined test coverage for the Version 1.0 Parent-Child Relationship contract. |
| 2.0 | 2026-08-23 | Approved Baseline | Jack Spaetjens | Defined test coverage for source identity, lookup and existing-item resolution. |
| 2.1 | 2026-08-23 | Approved Baseline | Jack Spaetjens | Defined test coverage for reused-child relationship-state inspection and recovery. |
| 2.2 | 2026-08-25 | Draft | Jack Spaetjens | Defined test coverage for run-level duplicate logical identity and persisted-marker collision validation. |
| 2.3 | 2026-08-25 | Approved Baseline | Jack Spaetjens | Defined test coverage for the urllib REST Client Foundation and redirect behaviour. |
| 2.4 | 2026-08-25 | Approved Baseline | Jack Spaetjens | Defined test coverage for the REST Client Foundation proxy contract. |
| 2.5 | 2026-08-27 | Approved Baseline | Jack Spaetjens | Clarified test coverage for Scrum compatibility evidence and mandatory validation-only candidate checks. |
| 2.6 | 2026-08-28 | Approved Baseline | Jack Spaetjens | Defined test coverage for successful Parent-Child Relationship PATCH response validation. |
| 2.7 | 2026-08-28 | Approved Baseline | Jack Spaetjens | Defined authorization-failure and least-privilege test coverage for Version 1.0. |
| 2.8 | 2026-08-29 | Approved Baseline | Jack Spaetjens | Synchronized implemented root existing/new Work Item lifecycle composition coverage. |
| 2.9 | 2026-08-29 | Approved Baseline | Jack Spaetjens | Approved future Generator Orchestration test obligations for preflight, global fail-fast and composition ownership. |
| 2.10 | 2026-08-29 | Approved Baseline | Jack Spaetjens | Synchronized implemented full preflight coordinator coverage and latest validation metrics. |
| 2.11 | 2026-08-30 | Approved Baseline | Jack Spaetjens | Synchronized implemented deterministic hierarchy traversal composition coverage and validation metrics. |
| 2.12 | 2026-08-30 | Approved Baseline | Jack Spaetjens | Synchronized complete Generator Orchestration composition coverage and validation metrics. |
| 2.13 | 2026-08-30 | Approved Baseline | Jack Spaetjens | Recorded Review Gate 2 PASS validation evidence with zero findings and no required remediation. |
| 2.14 | 2026-08-31 | Approved Baseline | Jack Spaetjens | Defined mandatory Application/Run Slice 1 composition coverage. |
| 2.15 | 2026-08-31 | Approved Baseline | Jack Spaetjens | Synchronized implemented Application/Run Slice 1 composition coverage and validation evidence. |
| 2.16 | 2026-08-31 | Approved Baseline | Jack Spaetjens | Defined mandatory Application/Run Slice 2 configuration-bootstrap composition coverage. |
| 2.17 | 2026-08-31 | Approved Baseline | Jack Spaetjens | Synchronized implemented Application/Run Slice 2 composition coverage and validation evidence. |
| 2.18 | 2026-09-01 | Approved Baseline | Jack Spaetjens | Defined mandatory Application/Run Slice 3 Process Bootstrap Invocation composition coverage. |
| 2.19 | 2026-09-02 | Approved Baseline | Jack Spaetjens | Synchronized implemented Application/Run Slice 3 Process Bootstrap Invocation composition coverage and validation evidence. |
| 2.20 | 2026-09-02 | Approved Baseline | Jack Spaetjens | Defined mandatory Application/Run Slice 4 Controlled Application Outcome Mapping coverage. |
| 2.21 | 2026-09-02 | Approved Baseline | Jack Spaetjens | Synchronized implemented Application/Run Slice 4 Controlled Application Outcome Mapping coverage and validation evidence. |
| 2.22 | 2026-09-03 | Approved Baseline | Jack Spaetjens | Defined mandatory Application/Run Slice 5 Controlled Failure Reporting to Standard Error coverage. |
| 2.23 | 2026-09-03 | Approved Baseline | Jack Spaetjens | Synchronized implemented Application/Run Slice 5 Controlled Failure Reporting to Standard Error coverage and validation evidence. |
| 2.24 | 2026-09-04 | Approved Baseline | Jack Spaetjens | Defined required but unimplemented Application/Run Slice 6 Runtime File Logging and Controlled-Failure Events coverage. |
| 2.25 | 2026-09-04 | Approved Baseline | Jack Spaetjens | Synchronized implemented Application/Run Slice 6 Runtime File Logging and Controlled-Failure Events coverage and validation evidence. |
| 2.26 | 2026-09-06 | Approved Baseline | Jack Spaetjens | Defined required/planned Application/Run Slice 7 import, termination and subprocess coverage while preserving pre-Slice-7 evidence. |
| 2.27 | 2026-09-06 | Approved Baseline | Jack Spaetjens | Synchronized implemented Application/Run Slice 7 test coverage and measured validation evidence. |
| 2.28 | 2026-09-06 | Approved Baseline | Jack Spaetjens | Defined planned Application/Run Slice 8 lifecycle logging validation and preserved pre-Slice-8 evidence. |
| 2.29 | 2026-09-08 | Approved Baseline | Jack Spaetjens | Synchronized implemented Application/Run Slice 8 lifecycle logging coverage and measured validation evidence. |
| 2.30 | 2026-09-11 | Approved Baseline | Jack Spaetjens | Defined required/planned validation for final unexpected-error handling and diagnostic safety while preserving current evidence. |
| 2.31 | 2026-09-11 | Approved Baseline | Jack Spaetjens | Allocated the approved planned validation contract to Application/Run Slice 9 without changing validation requirements or evidence. |
| 2.32 | 2026-09-11 | Approved Baseline | Jack Spaetjens | Synchronized implemented Slice-9 validation coverage and measured quality evidence. |
| 2.33 | 2026-09-12 | Approved Baseline | Jack Spaetjens | Proposed Review Gate 3 integration, live-validation allocation, evidence recording and findings criteria. |
| 2.34 | 2026-09-12 | Approved Baseline | Jack Spaetjens | Defined prospective validation for the owner-approved execution-summary contract while preserving historical implementation evidence. |
| 2.35 | 2026-09-16 | Approved Baseline | Jack Spaetjens | Associated prospective execution-summary validation with allocated Application/Run Slice 10 while preserving requirements and historical evidence. |
| 2.36 | 2026-09-16 | Approved Baseline | Jack Spaetjens | Recorded PR #157 Slice-10 automated validation evidence for G3-SUM-D1 to G3-SUM-D9; live Services validation remains pending. |
| 2.37 | 2026-09-16 | Approved Baseline | Jack Spaetjens | Defined prospective Gate-3 HTTP validation, scenario allocation, live-plan and consolidated dossier requirements without claiming new evidence. |
| 2.38 | 2026-09-17 | Approved Baseline | Jack Spaetjens | Recorded PR #162 HTTP reporting automated validation evidence; non-HTTP and live Gate-3 evidence remains incomplete. |
| 2.39 | 2026-09-20 | Draft | Jack Spaetjens | Recorded the Gate-3 application/integration evidence mapping and historical applicability assessment, confirming sufficient existing automated evidence while retaining required live Services validation. |

---

# Table of Contents

- [Azure DevOps Backlog Generator](#azure-devops-backlog-generator)
- [Testing Strategy](#testing-strategy)
- [Version History](#version-history)
- [Table of Contents](#table-of-contents)
- [1. Introduction](#1-introduction)
- [2. Purpose](#2-purpose)
- [3. Testing Objectives](#3-testing-objectives)
- [4. Testing Principles](#4-testing-principles)
- [5. Test Levels](#5-test-levels)
  - [Unit Testing](#unit-testing)
  - [Integration Testing](#integration-testing)
  - [System Testing](#system-testing)
  - [Regression Testing](#regression-testing)
- [6. Test Environment](#6-test-environment)
- [7. Test Data](#7-test-data)
- [8. Validation Strategy](#8-validation-strategy)
- [9. Acceptance Criteria](#9-acceptance-criteria)
  - [9.1 Review Gate 3 evidence requirements](#91-review-gate-3-evidence-requirements)
  - [9.2 Execution-summary validation](#92-execution-summary-validation)
  - [9.3 Gate-3 HTTP reporting and closure validation](#93-gate-3-http-reporting-and-closure-validation)
  - [9.4 Gate-3 Application/Integration Evidence Mapping](#94-gate-3-applicationintegration-evidence-mapping)
    - [9.4.1 Assessed Revision and Historical Applicability](#941-assessed-revision-and-historical-applicability)
    - [9.4.2 Evidence Levels and Boundary Rules](#942-evidence-levels-and-boundary-rules)
    - [9.4.3 Package Integration Evidence](#943-package-integration-evidence)
    - [9.4.4 Requirement-to-Evidence Mapping](#944-requirement-to-evidence-mapping)
    - [9.4.5 Stateful Failure and Rerun Evidence](#945-stateful-failure-and-rerun-evidence)
    - [9.4.6 Secret-Safety Evidence](#946-secret-safety-evidence)
    - [9.4.7 D06–D10 Applicability](#947-d06d10-applicability)
    - [9.4.8 Evidence Classification](#948-evidence-classification)
    - [9.4.9 Remaining Live-Only Evidence](#949-remaining-live-only-evidence)
    - [9.4.10 Release-Row Implications](#9410-release-row-implications)
- [10. Defect Management](#10-defect-management)
- [11. Traceability](#11-traceability)
- [12. Approval](#12-approval)


---

# 1. Introduction

This document defines the testing strategy for Version 1.0 of the Azure DevOps Backlog Generator.

It describes how the application shall be verified and validated to ensure compliance with the approved documentation baseline.

The Testing Strategy establishes a consistent approach to quality assurance throughout the software development lifecycle.

---

# 2. Purpose

The purpose of this document is to define the testing activities required to verify that Version 1.0 satisfies the approved requirements.

The strategy establishes the framework for planning, executing and documenting testing activities while maintaining traceability to the approved documentation.

---

# 3. Testing Objectives

Version 1.0 shall achieve the following testing objectives:

- Verify implementation of approved functional requirements.
- Validate compliance with the approved Software Architecture Document.
- Detect defects as early as practical.
- Support repeatable and automated testing.
- Verify reliable Azure DevOps REST API communication.
- Maintain complete traceability between requirements, implementation and testing.

---

# 4. Testing Principles

Testing shall follow the following principles:

- Documentation-driven validation.
- Risk-based testing.
- Repeatable execution.
- Automated testing where practical.
- Independent verification of implemented functionality.
- Early defect detection.
- Complete traceability to approved documentation.

---

# 5. Test Levels

Version 1.0 shall be validated through multiple levels of testing.

## Unit Testing

Unit testing shall verify the behaviour of individual software components in isolation.

Unit tests shall:

- Verify individual functions.
- Validate expected outputs.
- Detect implementation defects.
- Execute automatically where practical.

---

## Integration Testing

Integration testing shall verify interaction between application components.

Integration testing shall validate:

- Configuration management.
- Documentation processing.
- Azure DevOps REST API communication.
- Work item generation.
- Parent-child relationship creation.
- Scrum compatibility validation.
- Mandatory validation-only candidate creation after structural compatibility validation.

---

## System Testing

System testing shall verify the complete application operating as an integrated system.

System testing shall confirm:

- End-to-end execution.
- Correct backlog generation.
- Successful Azure DevOps integration.
- Compliance with the approved documentation baseline.

---

## Regression Testing

Regression testing shall verify that previously implemented functionality continues to operate correctly following software changes.

Regression testing shall be executed before each approved release.

---

# 6. Test Environment

Testing shall be performed within a controlled development environment.

The environment shall include:

- Python development environment.
- Azure DevOps Services test organisation/project.
- Standard Scrum and compatible inherited/customised Scrum test projects or controlled equivalent test fixtures.
- Test configuration files.
- Approved documentation baseline.
- Automated testing framework.

The test environment shall be maintained independently from production environments where practical.

Azure DevOps integration and system validation for Version 1.0 shall use an Azure DevOps Services test organisation/project. Azure DevOps Server test environments are not required for Version 1.0 acceptance or release validation.

---

# 7. Test Data

Test data shall support repeatable and reliable validation.

Version 1.0 shall use:

- Approved documentation.
- Representative Azure DevOps projects.
- Representative work item structures.
- A project missing a required work-item type.
- A project with a missing or incompatible required standard field.
- A project with missing, wrongly typed, read-only, inapplicable, process-required or otherwise incompatible `Custom.BacklogGeneratorSourceIdentity` support.
- Marked, unmarked and ambiguously marked existing work items for controlled lookup outcomes.
- A project/process rule that prevents candidate creation.
- Controlled configuration files.

Test data shall avoid the inclusion of confidential or sensitive information.

---

# 8. Validation Strategy

Validation activities shall confirm that Version 1.0 satisfies the approved documentation baseline.

Validation shall include:

- Functional verification.
- Architectural compliance.
- API communication validation.
- Documentation traceability verification.
- Automated test execution.
- Manual verification where appropriate.
- Scrum compatibility validation, including failure before persistent backlog generation when required metadata cannot be retrieved or a candidate request is invalid.

Documentation Input Specification validation shall cover:

- dedicated source-directory discovery and direct regular `.md` file discovery;
- case-insensitive extension matching, no recursive traversal and symbolic-link exclusion;
- UTF-8 input, accepted UTF-8 byte order marks and invalid UTF-8 rejection;
- CommonMark 0.31.2 semantic parsing, top-level ATX hierarchy mapping, excluded or nested Markdown contexts and top-level setext-heading rejection;
- hierarchy-level validation and orphan Feature, Product Backlog Item and Task rejection;
- title extraction and normalisation, empty-title rejection, title rejection above 255 characters and duplicate normalised sibling-title rejection;
- deterministic NFC, `casefold()` and ordinal file ordering, with item source order preserved;
- deterministic source identity and accepted rename sensitivity;
- cross-file hierarchy rejection; and
- source validation before persistent backlog generation.

Description Mapping validation shall additionally cover:

- installation and operation of `markdown-it-py==4.2.0` on the supported Python 3.14 environment;
- the fixed `MarkdownIt("commonmark")` configuration, with no plugins, option overrides, linkify, typography, GFM preset or custom renderer rules;
- relevant CommonMark 0.31.2 parsing and parsed-node validation behaviour;
- direct-body extraction and exclusion of child semantic headings and child-item content;
- missing, whitespace-only, rendering-failure and empty-rendered-output validation failures before persistence;
- raw HTML and Markdown image rejection;
- permitted RFC 3986 absolute HTTP/HTTPS links and rejection of relative, non-HTTP(S), hostless and malformed destinations;
- supported CommonMark body content, including fenced and indented code blocks;
- exact normative HTML snapshots after CRLF and lone-CR normalisation to LF only, preserving every other character and any renderer-produced final LF; and
- confirmation that Description content does not change source identity.

Acceptance Criteria Mapping validation shall additionally cover:

- recognition of the reserved marker and ordinary-prose or non-direct-context occurrences;
- valid Epic, Feature and Product Backlog Item constructs and optional absence;
- Task rejection, duplicate markers and invalid placement;
- Description and Acceptance Criteria partitioning, including mandatory Description validation after exclusion;
- one valid ordered or unordered top-level list, list cardinality, mixed-list rejection, nested-list rejection and prose-outside-list rejection;
- empty or whitespace-only criterion rejection;
- raw HTML, Markdown image and invalid-link rejection;
- CommonMark rendering, exact HTML snapshots, line-ending normalisation and renderer-produced final-LF preservation;
- Acceptance Criteria exclusion from source identity; and
- source-validation failure before persistent backlog generation.

Tags Mapping validation shall additionally cover:

- direct-body marker recognition and nested or container-context non-recognition;
- valid optional Tags constructs for Epic, Feature, Product Backlog Item and Task;
- fixed Description, Tags and Acceptance Criteria ordering, Tags boundaries and Description preservation after partitioning;
- unordered-list requirements and ordered-list, duplicate-marker, empty-list, multiple-list, nested-list and prose-outside-list rejection;
- visible inline-text extraction, Unicode whitespace normalisation, empty-tag rejection and source-order preservation;
- comma, semicolon, more-than-400-Unicode-character, Unicode control-character, Unicode format-character and malformed-surrogate rejection;
- casefold duplicate-tag rejection and exact `; ` prepared `System.Tags` values;
- raw HTML, Markdown image and invalid link or autolink rejection;
- Tags exclusion from source identity; and
- source-validation failure before persistent backlog generation.

REST Client Foundation validation shall additionally cover:

- use of `urllib` from the Python standard library with no third-party HTTP dependency;
- Azure DevOps Services URL construction, configured organisation/project addressing, URI path-segment encoding and the fixed `api-version=7.1` contract;
- exact HTTP method, common `Accept` header, endpoint-specific Content-Type and JSON transport representation where required;
- HTTP Basic authentication construction from a synthetic PAT using an empty username and confirmation that PATs and Authorization headers do not appear in representations, logs, exceptions or diagnostics;
- the fixed effective 30-second `urllib` timeout with no externally configurable timeout settings;
- rejection without following of every HTTP `3xx` response and confirmation that redirect handling does not forward the Authorization header or any credential;
- explicit disabling of `urllib` proxy handling, so environment proxy variables, Windows or other system proxy configuration and other ambient proxy settings do not affect transport; direct requests retain the configured Azure DevOps Services target; Authorization is not sent through a discovered proxy; and no proxy retry or fallback behaviour occurs;
- no automatic retry or sleep for transport failures, HTTP `408`, HTTP `429`, `5xx`, optimistic-concurrency failures or uncertain mutation results;
- controlled handling of connection, DNS, TLS and timeout failures, unexpected statuses, malformed JSON, missing required bodies and malformed required response shapes;
- exact endpoint-specific `200 OK` success validation and rejection of an unexpected success-range status;
- safe handling of non-JSON error bodies and bounded optional diagnostics without full response-body logging by default; and
- independent request/response lifecycles with response closure, no retained response object, persistent session, cookie state, redirect state, connection pool or other persistent mutable request state.

Authorization and least-privilege validation shall additionally cover:

- preservation of `403` as a controlled authorization failure, distinct from `401` authentication rejection;
- no automatic retry, alternate credential or privilege-escalation attempt after `403`;
- continued exclusion of PATs and Authorization headers from authorization-failure diagnostics; and
- full Generator Orchestration coverage confirming that no later mutation occurs after an authorization failure; wider application/run integration coverage remains deferred.

Scrum Compatibility validation shall additionally cover:

- Work Item Types Get evidence for the fixed Epic, Feature, Product Backlog Item and Task types;
- Work Item Type Field Get with `$expand=All` as type-specific evidence, and Fields Get as global field-definition evidence, without treating global metadata as proof of type applicability;
- structural validation of required standard fields and the fixed `Custom.BacklogGeneratorSourceIdentity` reference name, display name, String type, non-read-only state, applicability, no-default state and `alwaysRequired=false` optional process-level state, using only properties returned by the approved endpoints;
- failure before persistent generation for absent, malformed, wrongly typed, read-only, inapplicable, defaulted, process-required or otherwise incompatible required-field evidence;
- additional `alwaysRequired` fields not causing compatibility failure solely from that property;
- mandatory non-persisting validation-only Create checks after structural compatibility and before existing-item resolution or persistent generation for every constructed candidate in deterministic source order, including candidates that later resolve REUSED;
- use of the exact candidate JSON Patch contract, including the identity marker and all fields emitted for the candidate, with `validateOnly=true` as the only approved request difference from persistent Create;
- validation-only rejection caused by an additional required field or other process rule stopping the complete invocation before any later operation;
- no automatic retry, no persistent work-item creation and secret-safe diagnostics throughout compatibility validation; and
- Tags presence and absence, Acceptance Criteria presence and absence, Task's mandatory Acceptance Criteria omission, and equal-shaped candidates with differing values, each receiving separate validation-only evidence.

Implemented full-preflight coordinator coverage proves complete preflight sequencing; immutable returned `PreflightState`; deterministic candidate order across multiple roots and documents; separate validation of same-type candidates and optional-value differences; source-identity failure before REST; project, metadata and compatibility failure propagation; mid-sequence validation-only failure without retry; and zero WIQL, existing-item GET, persistent Create, relationship-state GET or Parent-Child Relationship PATCH operations before or after the barrier within that slice. Implemented traversal-composition coverage proves malformed candidate-count and source-identity association failure before persistence; exact candidate-object reuse without reconstruction; NEW and REUSED roots; deterministic Epic → Feature → Product Backlog Item → Task, multiple-root and multiple-document traversal; parent eligibility; REUSED CORRECT, MISSING recovery and CONFLICTING stop; deep, root, non-root-resolution, relationship-state GET and relationship PATCH failure stops; empty hierarchy and zero-root document handling; two-run recovery without duplicate child Create; and no repeated preflight operations. Final Generator-entry wiring coverage proves the exact hierarchy, returned `PreflightState` and REST-client identities; preflight and traversal exactly once; their successful mutation-barrier ordering; exact PAT preservation; and `None` return. Full Generator composition proves preflight failure prevents persistence and that malformed Azure DevOps responses and HTTP `401` and `403` propagate exactly once without retry, alternate credentials or PAT event leakage, while genuinely stopping all later descendants, siblings, roots, documents and persistence operations. Lower-level REST tests remain responsible for response parsing; Generator tests prove full-composition propagation and global stop. Review Gate 2 completed with PASS: 0 BLOCKER, 0 MAJOR, 0 MINOR and no required remediation. Ruff passed; the focused orchestration suite recorded 34 passed; `pytest -ra` and `pytest -W error` each recorded 680 passed, with 0 failed, skipped, warnings, xfail or xpass. Coverage was 95% across 1,281 statements with 64 missed statements; the missed-statements audit found no material uncovered current Generator-Orchestration branch. All Generator-Orchestration traceability requirements were PROVEN.

Implemented Application/Run Slice 1 composition coverage uses collaborator doubles and proves that
`coordinate_application_run(configuration)` passes the exact configured `source_directory` unchanged to one
`DocumentationProcessor.process` invocation; constructs exactly one `AzureDevOpsRestClient` with the exact
configured organisation and project, without passing the PAT to its constructor; and passes the exact
returned `DocumentationHierarchy`, REST-client instance and original PAT through the Generator keyword
argument to exactly one `coordinate_generator_orchestration` invocation. It proves a `None` return on
success; unchanged propagation of documentation-processing, REST-client-construction and Generator failures;
documentation failure prevents REST-client construction and Generator invocation; REST-client-construction
failure prevents Generator invocation; and Generator failure causes no retry, fallback or second invocation.
It further proves no direct preflight, traversal, lifecycle or persistence call; no CLI parsing,
logging/reporting or process-exit mapping; and no PAT leakage in test events or diagnostics. These are
composition tests and do not duplicate Documentation Processor, REST Client or Generator internal tests.
The focused Slice-1 suite recorded 4 passed. The full suite and `pytest -W error` each recorded 684 passed,
with 0 failed, skipped, warnings, xfail or xpass. Ruff passed. Coverage was 95% across 1,289 statements
with 64 missed statements; `main.py` was 100% covered, and all new Slice-1 production statements were
covered.

Implemented Application/Run Slice 2 composition coverage tests
`coordinate_application_bootstrap(arguments: Sequence[str]) -> None` at the configuration/bootstrap
collaborator boundary. Three tests prove successful bootstrap composition using the exact supplied arguments
object, one loader invocation, the exact returned validated `Configuration`, one Slice-1 invocation in loader-
then-Slice-1 order, `None` return and PAT-safe event data. They also prove that a specific loader exception
propagates unchanged with no Slice-1 invocation or retry, and that a specific Slice-1 exception propagates
unchanged after the exact `Configuration` reaches Slice 1 once, without retry, fallback or second invocation.

The implemented Slice-2 composition tests prove that the coordinator does not itself parse CLI options,
validate configuration, read environment variables, perform document processing, construct a REST client,
invoke the Generator directly, log or report, or map process exits. Composition-test events and diagnostics do
not contain a synthetic PAT value. These tests do not duplicate configuration-loader parsing or validation tests,
nor Slice-1 composition tests. Process-entrypoint tests, including executable CLI, user-facing output
and process-exit behaviour, remain outside Slice 2. The focused `tests/test_main.py` suite recorded 7 passed;
the full suite and `pytest -W error` each recorded 687 passed, with 0 failed, skipped, warnings, xfail or xpass.
Ruff passed. Coverage was 95% across 1,294 statements with 64 missed statements; `main.py` had 13 statements
with 0 missed, and all new Slice-2 production statements were covered.

Implemented Application/Run Slice 3 — Process Bootstrap Invocation composition coverage tests `main() -> None`
at the process-to-bootstrap boundary. A successful-delegation test installs a controlled `sys.argv`, proves that
`sys.argv[0]` is excluded, verifies that the values represented by `sys.argv[1:]` reach
`coordinate_application_bootstrap(...)` directly, and proves exactly one bootstrap invocation, `None` return,
no stdout, no stderr and no logging. A bootstrap-failure test installs controlled process arguments, makes the
bootstrap collaborator raise a specific sentinel exception object, and proves exactly one invocation and
propagation of that exact object from `main()` with no retry, fallback, second invocation, stdout, stderr,
logging, process-exit conversion or deliberate `SystemExit`.

The two Slice-3 tests do not duplicate `--config-file` parsing, CLI usage validation, TOML loading,
configuration validation, PAT acquisition, environment precedence, Slice-2 or Slice-1 composition,
Documentation Processor, REST Client, Generator, REST-error, hierarchy or lifecycle coverage. They do not
require subprocess tests because Slice 3 deliberately defines no executable adapter. The focused
`tests/test_main.py` suite recorded 9 passed; the full suite and `pytest -W error` each recorded 689 passed,
with 0 failed, skipped, warnings, xfail or xpass. Ruff passed. Coverage was 95% across 1,297 statements with
64 missed statements; `main.py` had 16 statements with 0 missed, and all new Slice-3 production statements
were covered.

Implemented Application/Run Slice 4 — Controlled Application Outcome Mapping coverage in
`tests/test_main.py` tests the `run_process() -> int` wrapper at the process-outcome boundary. It proves one
successful `main()` invocation, an exact integer return of `0`, no retry or fallback, no stdout, no stderr, no
logging and no `SystemExit`. Controlled-failure mapping tests use representative instances or subclasses, with
parameterisation where appropriate, and prove exact integer return `1` for the `ConfigurationError`,
`DocumentationProcessingError` and `AzureDevOpsRestClientError` hierarchies and for
`SourceIdentityValidationError`, `ExistingWorkItemResolutionError` and
`ConflictingReusedChildRelationshipError`. They prove exactly one `main()` invocation, no retry, fallback or
second invocation, no re-raise of the controlled exception, no stdout, no stderr, no logging and no
`SystemExit`.

At the Slice-4 baseline, an unexpected-failure test made `main()` raise one sentinel exception outside that approved controlled set
and proved that the exact object propagated unchanged; `run_process()` did not return `1`, catch it
generically, retry, fall back or invoke `main()` again, and produced no stdout, stderr, logging or
`SystemExit`. Slice-4 tests do not duplicate configuration parsing or PAT validation; document parsing; Azure
DevOps transport, HTTP `401`/`403` or malformed-response semantics; Generator lifecycle or relationship
behaviour; or Slice-1, Slice-2 or Slice-3 composition. No subprocess coverage is required because Slice 4
defines no executable adapter. The focused `tests/test_main.py` suite recorded 17 passed; the full suite and
`pytest -W error` each recorded 697 passed, with 0 failed, skipped, warnings, xfail or xpass. Ruff passed.
Coverage was 95% across 1,309 statements with 64 missed statements; `main.py` had 28 statements with 0 missed,
and all new Slice-4 production statements were covered.

Implemented Application/Run Slice 5 — Controlled Failure Reporting to Standard Error focused process-boundary
coverage in `tests/test_main.py` does not duplicate lower-layer generation, configuration, documentation, REST,
HTTP `401`/`403`, work-item resolution, relationship, Slice-1, Slice-2, Slice-3 or Slice-4 classification tests. A
successful-execution test proves exactly one `main()` invocation, exact integer `0`, empty stdout, empty stderr, no
logging, no `SystemExit`, no retry and no fallback. Slice 5 includes no subprocess tests; the implemented
Slice-7 adapter subprocess coverage is recorded below.

For each approved controlled category — the `ConfigurationError`, `DocumentationProcessingError` and
`AzureDevOpsRestClientError` hierarchies, and `SourceIdentityValidationError`, `ExistingWorkItemResolutionError`
and `ConflictingReusedChildRelationshipError` — focused tests prove exactly one `main()` invocation, exact integer
`1`, empty stdout, no logging, no `SystemExit`, no retry, no fallback, no second invocation and no re-raise. They
prove exact stderr content comprising only the corresponding fixed message and one newline:
`Configuration error.\n`, `Documentation processing error.\n`, `Azure DevOps error.\n`,
`Source identity validation error.\n`, `Existing work item resolution error.\n` or
`Conflicting reused child relationship error.\n`. Representative existing concrete exceptions or subclasses may be
used where useful.

A secret-safety test uses synthetic PAT-like detail, a synthetic configuration path and a synthetic URL in an
existing controlled exception, and proves that stderr contains only the applicable fixed category message, that all
synthetic detail is absent, that stdout is empty and that the result is `1`. No exception classes were changed merely
to facilitate this test. At the Slice-5 baseline, an unexpected-failure test made `main()` raise one sentinel exception outside the approved
controlled set and proved that the exact object propagated unchanged after one invocation, with empty stdout and
stderr, no controlled message, no logging, no `SystemExit`, retry, fallback or second invocation. The tests require
no dynamic exception rendering, generic exception catching or executable adapter.

The focused `tests/test_main.py` suite recorded 18 passed; the full suite and `pytest -W error` each recorded 698
passed, with 0 failed, skipped, warnings, xfail or xpass. Ruff passed. Coverage was 95% across 1,323 statements
with 64 missed statements; `main.py` had 42 statements with 0 missed, and all new Slice-5 production statements
were covered.

Implemented Application/Run Slice 6 — Runtime File Logging and Controlled-Failure Events focused coverage in
`tests/test_main.py` proves all five configured thresholds; the fixed logger, file and formatter; append and UTF-8
semantics; `propagate=False`; and silent successful execution. It covers reachable post-initialisation controlled
categories, the pre-initialisation configuration-failure boundary, stale-handler removal before configuration
loading, `ApplicationLoggingError` on constructor failure, partial-initialisation cleanup, repeated invocations, and
same-named non-owned, root and unrelated logger isolation.

The focused tests prove exactly one category-only `CRITICAL` controlled event reaches only the active owned handler;
the handler’s direct LogRecord dispatch prevents non-owned same-named handlers from receiving it. D5 coverage proves
that a secondary owned-handler write failure preserves the original controlled category, exact stderr, empty stdout
and integer `1`, without retry, fallback, alternate destination, duplicate event, `ApplicationLoggingError`
substitution, logging traceback or secondary exception propagation. The tests prove `logging.raiseExceptions` remains
unchanged. Full post-initialisation secret-safety coverage supplies `SYNTHETIC_PAT_DO_NOT_RENDER`,
`C:\\secret\\config.toml` and `https://example.invalid/private` in underlying detail and proves they are absent from
stdout, stderr beyond the fixed line and the runtime logfile. Historical Slice-6 unexpected-exception coverage
preserved the exact exception object with no controlled event or traceback logging. Slice-9 coverage below
supersedes the earlier process-facing propagation assertions while preserving direct lower-level propagation.

The focused `tests/test_main.py` suite recorded 35 passed. The full suite and `pytest -W error` each recorded 715
passed, with 0 failed, skipped, warnings, xfail or xpass. Ruff passed. Coverage was 95% across 1,367 statements with
64 missed statements; `main.py` had 86 statements with 0 missed (100%), and all meaningful Slice-6 production
statements were covered. These are pre-Slice-7 baseline results. Slice 6 required no subprocess,
`SystemExit` or traceback-content tests; implemented Slice-7 evidence follows.

Application/Run Slice 7 — Package Execution Adapter with Controlled Process Termination is implemented.
The focused `tests/test___main__.py` module provides executed coverage of the approved S7-D1/S7-D2
boundary in Architecture Section 7.1.7. Slices 1–9 are implemented; wider Application/Run remains incomplete.

Implemented coverage includes:

1. Ordinary package and executable-module import safety: no application execution, `run_process()`,
   `main()` or bootstrap call, `SystemExit`, stdout/stderr or adapter-controlled logging.
2. Exact one-call delegation to `run_process()`, without direct `main()` or bootstrap invocation;
   exact integer `0` and `1` become `SystemExit(0)` and `SystemExit(1)` without adapter output or logging.
3. Adapter-only same-object unexpected-exception propagation when substituted `run_process()` raises: no controlled translation, generic catch,
   `SystemExit(1)`, stdout/stderr or application-generated traceback logging.
4. Real package controlled-failure subprocess invocation:
   `python -m azure_devops_backlog_generator --config-file <explicit missing temp file>`.
   Measured return code is `1`, stdout is empty and stderr is exactly `Configuration error.\n`, without
   a Python traceback. The explicit configuration remains absent, no runtime logfile is created on this
   pre-logging configuration-failure path, and no network/application processing is reached.
5. Isolated successful child adapter harness: substituted `run_process()` returns `0`; process status is
   `0`, stdout and stderr are empty. This is adapter-boundary validation, not successful application E2E.
6. Isolated unexpected child adapter harness: substituted `run_process()` raises; termination is nonzero,
   stdout is empty and native interpreter stderr is nonempty. No exact unexpected exit code, traceback
   content or formatting, or final diagnostic policy is claimed.

Child processes use the project interpreter with an intentionally allowlisted environment and an isolated
temporary working directory. Only available `SystemRoot`/`WINDIR` values are inherited; explicit settings
are absolute repository `src` `PYTHONPATH`, `PYTHONNOUSERSITE=1`, `PYTHONDONTWRITEBYTECODE=1`,
`PYTHONIOENCODING=utf-8` and isolated `TEMP`/`TMP`/`TMPDIR`. The child does not inherit `AZDO_PAT`,
proxy variables, developer `PYTHONPATH`, `PYTHONHOME`, `PYTHONSTARTUP`, `PYTHONWARNINGS`, coverage
subprocess activation or broader developer environment credentials/configuration. These are test-isolation
settings, not new application configuration. This isolation does not establish secret-safety for arbitrary
native unexpected traceback output. Slice-9 evidence below resolves the previous limitation only for
the supported handled-Exception `run_process()`/package path; direct lower-level propagation remains intentional.

Historical Slice-7 implementation validation evidence from PR #136 (commit `468d98d`, merge `009ef71`):

| Validation | Collected | Passed | Failed | Skipped | Warnings | Xfail | Xpass |
|------------|-----------|--------|--------|---------|----------|-------|-------|
| Focused `tests/test___main__.py` | 8 | 8 | 0 | 0 | 0 | 0 | 0 |
| Full pytest | 723 | 723 | 0 | 0 | 0 | 0 | 0 |
| `pytest -W error` | 723 | 723 | 0 | 0 | 0 | 0 | 0 |

Ruff passed. Overall coverage was 95% across 1,370 statements with 64 missed.

| Module | Statements | Missed | Coverage |
|--------|------------|--------|----------|
| `src/azure_devops_backlog_generator/__main__.py` | 3 | 0 | 100% |
| `src/azure_devops_backlog_generator/main.py` | 86 | 0 | 100% |

Compared with the pre-Slice-7 baseline, tests increased from 715 to 723 (+8), statements from 1,367 to
1,370 (+3), missed statements remained 64 and coverage remained 95%. `main.py` remained unchanged at
86 statements / 0 missed / 100%. The implementation added exactly `src/azure_devops_backlog_generator/__main__.py`
and `tests/test___main__.py`: 2 files, 210 insertions, 0 deletions. The adapter has 6 physical lines and
3 coverage-counted statements; the focused test module has 204 physical lines. Physical line counts
are not a measure of production complexity. These are recorded implementation results, not new test runs
performed during this documentation status sync.

Existing Slice-5/6 evidence remains authoritative for all seven controlled categories, exact reporting,
owned-handler logging, D1–D5 and controlled secret-safety; Slice 7 changes none of those contracts.
Broader logging beyond the implemented slices, execution-summary content and presentation, broader integration/E2E,
live Azure DevOps Services validation, Operational Readiness, API Section 6.1
status-drift reconciliation before Review Gate 3, Gate 3 and final Version 1.0 readiness remain future.
Version 1.0 remains pre-release; no live Azure DevOps E2E or release-readiness claim is made.

**Application/Run Slice 8 — Process-Neutral Application Lifecycle File Logging: IMPLEMENTED.**
The implementation was merged in PR #141 (implementation commit `378e2b1`, merge `8560a89`), following
contract PR #139 and approval PR #140. Architecture Section 7.1.8 remains authoritative for implemented,
approved S8-D1–D3. The Slice-8 status-sync revision 2.29 is Approved Baseline; the implementation is complete within its approved scope.
Revision 2.32 is Approved Baseline.

The recorded Slice-7 evidence above is the PRE-SLICE-8 implementation quality baseline: focused 8/8,
full pytest 723/723 and `pytest -W error` 723/723, each with zero failed, skipped, warnings, xfail
or xpass; Ruff passed. Coverage remains historical evidence of 95%, 1,370 statements and 64 missed,
with `__main__.py` 3/0/100% and `main.py` 86/0/100%. These figures are not Slice-8 results.

The merged Slice-8 validation extended `tests/test_main.py`, covering bootstrap composition, logging,
isolation and failure handling without a new test module. At that baseline, empty-log assertions were updated:
successful eligible runs record START and COMPLETION; unexpected application failure records START
only; configuration failure after prior success leaves earlier lifecycle records unchanged. Silence
and unexpected-diagnostic exclusions remain intact. Existing Slice-5/6/7 coverage remains authoritative
for its behaviour, with lifecycle assertions added to controlled, isolation and repeated-invocation tests.

| Implemented category | Verified behaviour |
|---------------------------|--------------------|
| Successful eligible sequence | Exactly one START emission, configured application execution, then exactly one COMPLETION emission, in that order. |
| Exact messages | START is exactly `Application run started.`; COMPLETION is exactly `Application run completed successfully.`. |
| Severity | Both lifecycle records use INFO. |
| Configured filtering | DEBUG and INFO thresholds permit both records; WARNING, ERROR and CRITICAL filter INFO without threshold bypass or required lifecycle write attempt. |
| Configuration failure | No lifecycle event or logfile attempt; existing configuration outcome remains unchanged. |
| Logger initialisation failure | Neither lifecycle event occurs; existing initialisation-only `ApplicationLoggingError` behaviour remains unchanged. |
| Controlled failure after START | One eligible START, no COMPLETION, existing controlled CRITICAL event exactly once, unchanged exact stderr and result `1`. |
| Unexpected failure after START | One eligible START and no COMPLETION; direct bootstrap calls retain same-object propagation. Slice 9 now supplies the process-facing unexpected event and report; Slice-8 lifecycle behaviour remains unchanged. |
| Repeated invocation | Only current-invocation owned-handler behaviour; no stale or duplicate lifecycle records. |
| Same-named non-owned isolation | Non-owned handlers on the named logger receive no lifecycle records and remain untouched. |
| Root/unrelated isolation | No lifecycle propagation/delivery to root or unrelated handlers; those handlers remain untouched. |
| START write failure | Application execution still occurs, with no retry, fallback, extra event/output, logging traceback, exception substitution or outcome change. |
| COMPLETION write failure | Bootstrap still returns normally; success, process result and adapter status are preserved, without retry, fallback, extra event/output, logging traceback or exception substitution. |
| Fixed-content secret safety | Synthetic PAT, Authorization markers, paths, dynamic exception text and other supplied sentinel data do not appear in lifecycle records. |
| Successful output | stdout and stderr remain empty, including best-effort lifecycle write failures. |

The START/COMPLETION timing assertions establish successful configuration loading/validation and logging
initialisation before START, START immediately before `coordinate_application_run(configuration)`,
and COMPLETION only after its normal return and before normal bootstrap return. Write-failure coverage
verifies preservation of D1–D5, `logging.raiseExceptions`, owned-handler-only delivery and initialisation-only
`ApplicationLoggingError`; lifecycle failures are not an eighth controlled category. Failure of START
does not prevent the independently eligible COMPLETION following successful execution. Tests exercise
raised lifecycle failures from both `handle()` and `emit()`, bootstrap and `run_process()` composition,
and failed START followed by controlled or unexpected application failure. `KeyboardInterrupt` and
`SystemExit` propagation is verified. The helper's `Exception` catch surrounds lifecycle emission only,
not `coordinate_application_run(configuration)`. Fixed lifecycle messages do not establish secret-safety
for arbitrary native unexpected traceback output.

No new Slice-8 subprocess tests were required or added: SystemExit and real package execution are
unchanged, and existing Slice-7 package/subprocess coverage passed. Slice-8 tests use isolated application
composition; no live Azure DevOps Services validation, network access, real PAT, live organisation/project
or real work-item mutation was performed. Broader integration/E2E release evidence remains future.

Recorded merged Slice-8 validation evidence:

| Validation | Collected | Passed | Failed | Skipped | Warnings | Xfail | Xpass |
|------------|-----------|--------|--------|---------|----------|-------|-------|
| Focused `tests/test_main.py` | 55 | 55 | 0 | 0 | 0 | 0 | 0 |
| Full pytest | 743 | 743 | 0 | 0 | 0 | 0 | 0 |
| `pytest -W error` | 743 | 743 | 0 | 0 | 0 | 0 | 0 |

Ruff passed. Historical Slice-8 overall coverage was 95% across 1,381 statements with 64 missed.

| Module | Statements | Missed | Coverage |
|--------|------------|--------|----------|
| `src/azure_devops_backlog_generator/main.py` | 97 | 0 | 100% |
| `src/azure_devops_backlog_generator/__main__.py` | 3 | 0 | 100% |

Compared with the pre-Slice-8 baseline, full tests increased from 723 to 743 (+20), statements from
1,370 to 1,381 (+11), missed statements remained 64 (+0) and coverage remained 95%. These measured
results establish no known failures in the executed checks, not mathematical proof of defect freedom.
They are merged implementation evidence; Ruff and pytest were not rerun for this documentation-only
status sync. Summary, remaining logging, integration/E2E, live validation,
Operational Readiness, API Section 6.1 reconciliation before Gate 3,
Review Gate 3 and final Version-1.0 readiness remain future.

**Application/Run Slice 9 — Final Unexpected-Error Handling and Diagnostic Safety — IMPLEMENTED — APPROVED CONTRACT.**
Architecture's
[Application/Run Slice 9 — Final Unexpected-Error Handling and Diagnostic Safety](02-Architecture.md#applicationrun-slice-9--final-unexpected-error-handling-and-diagnostic-safety)
section is authoritative for UE-D1–UE-D10. Those decisions remain approved and are implemented.
Testing revision 2.32 is Approved Baseline.

Implementation provenance is PR #148 (commit `738fdc3`, merge `4549eee`). Contract provenance remains
PR #144 (commit `2070425`, merge `4d80b58`) and approval PR #145 (commit `e3e190f`, merge `fa158d9`);
allocation remains PR #146 (commit `720bb68`, merge `e332c69`) and allocation approval PR #147
(commit `1174bcb`, merge `ea37478`). Production changes are confined to
`src/azure_devops_backlog_generator/main.py`; implemented validation is in `tests/test_main.py` and
`tests/test___main__.py`. Production `__main__.py` remains unchanged.

The following records implemented validation of the approved contract:

| Implemented boundary | Verified observation |
|------------------|----------------------|
| Generic process fallback | An otherwise-unclassified `Exception` from the application is handled by `run_process()` after exactly one `main()` invocation; result is exactly `int` `1`. |
| Exact presentation | Stderr is exactly `Unexpected application error.\n`; stdout is empty, with no duplicate reporting. |
| Diagnostic exclusion | Synthetic exception type/message/string/repr/args/cause/context, PAT, Authorization, paths, configuration, organisation/project, URLs, titles, source/user content and request/response sentinels are absent from output and logfile content. No `exc_info`, traceback or stack data is emitted. |
| Active runtime logging | Exactly one CRITICAL `Unexpected application error.` emission attempt uses only the current-invocation owned handler; a successful write produces one record at every supported configured threshold. |
| Handler isolation and repeated invocation | Root, unrelated and same-named non-owned handlers receive nothing; only the current owned handler is used, stale handlers are replaced, and repeated invocations produce no duplicate event or fallback destination. |
| Unexpected logfile emission failure | An ordinary `Exception` during the owned emission preserves the primary unexpected classification, fixed stderr and result `1` when stderr remains writable; no retry, fallback, replacement event, logging diagnostic/traceback or `ApplicationLoggingError` substitution occurs. |
| Stderr boundary | A stderr-delivery failure propagates unchanged; no suppression, retry or fallback is introduced. |
| Pre-initialisation unexpected failure | No unexpected logfile event is attempted and no stale handler receives it; fixed stderr and result `1` remain the process report. |
| Post-initialisation application failure | Eligible START may exist; COMPLETION is absent; the best-effort unexpected event precedes fixed stderr and result `1`. |
| Direct lower-level calls | `main()`, `coordinate_application_bootstrap(...)` and `coordinate_application_run(...)` retain same-object unexpected-exception propagation without generic process conversion. |
| Controlled precedence | All seven controlled categories retain their exact existing messages, result `1` and logging contracts; the generic fallback does not absorb them or become an eighth category. |
| Configuration failure | `ConfigurationError` retains `Configuration error.\n`, result `1` and no pre-initialisation file event. |
| Logger initialisation failure | Initialisation-only `ApplicationLoggingError` retains `Application logging error.\n`, result `1` and no unexpected logfile event. |
| Process-control exceptions | `KeyboardInterrupt`, `SystemExit` and `GeneratorExit` propagate unchanged; the generic fallback and unexpected-event best-effort handling do not catch `BaseException` subclasses outside `Exception`. |
| Package composition | The existing adapter maps the handled unexpected result to `SystemExit(1)` without its own catch, diagnostic output or duplicate reporting. |
| Native traceback suppression | An isolated subprocess reaching the real `run_process()` fallback through package execution returns OS status `1`, exact fixed stderr and empty stdout, without native traceback from the handled exception. |
| Existing behaviour | Slice-6 D1–D5, stale-handler cleanup, configured logging, owned-handler isolation, seven controlled categories, Slice-8 exact INFO messages/filtering/best effort and sole package execution surface remain unchanged. |

Implemented subprocess evidence exercises the actual fallback before and after logging initialisation,
with isolated lower-level collaborators inducing failure without network access. Substituting `run_process()` itself does not prove its
catch or traceback-suppression behaviour. Existing adapter-only unexpected-propagation tests describe
their separate boundary; direct lower-level propagation remains intentional. No live Azure operation,
real PAT or live environment is required for this capability's validation. Broader integration/E2E and
live Services release validation remain separate and incomplete.

Recorded merged Slice-9 implementation validation evidence:

| Validation | Collected | Passed | Failed | Skipped | Warnings | Xfail | Xpass |
|------------|-----------|--------|--------|---------|----------|-------|-------|
| Combined focused `tests/test_main.py` and `tests/test___main__.py` | 84 | 84 | — | — | — | — | — |
| Full pytest | 764 | 764 | 0 | 0 | 0 | 0 | 0 |
| `pytest -W error` | 764 | 764 | 0 | 0 | 0 | 0 | 0 |

The combined focused run comprises 73 tests in `tests/test_main.py` and 11 in `tests/test___main__.py`.
Ruff passed. Overall coverage is 95% across 1,394 statements with 64 missed.

| Module | Statements | Missed | Coverage |
|--------|------------|--------|----------|
| `src/azure_devops_backlog_generator/main.py` | 110 | 0 | 100% |
| `src/azure_devops_backlog_generator/__main__.py` | 3 | 0 | 100% |

| Measure | Pre-Slice-9 | Post-Slice-9 | Delta |
|---------|-------------|--------------|-------|
| Full-suite tests | 743 | 764 | +21 |
| `tests/test_main.py` tests | 55 | 73 | +18 |
| Statements | 1,381 | 1,394 | +13 |
| Missed statements | 64 | 64 | +0 |
| Overall coverage | 95% | 95% | Unchanged |
| `main.py` statements / missed / coverage | 97 / 0 / 100% | 110 / 0 / 100% | +13 statements; +0 missed |
| `__main__.py` statements / missed / coverage | 3 / 0 / 100% | 3 / 0 / 100% | Unchanged |

These are merged implementation results, not new test runs for this documentation-only status sync.
No tests were added or changed, and neither Ruff nor pytest was executed for this revision. No live
Azure DevOps operations occurred. Slice-6, Slice-8 and package import/adapter regressions remain covered.
The previous native traceback limitation is resolved only on the supported handled-Exception
`run_process()`/package path. Direct lower-level callers still receive exceptions; no generic redaction
framework, sanitised traceback or debug diagnostic feature was added.

Slices 1–9 are implemented under approved contracts; wider Application/Run remains incomplete.
Slice 10 is IMPLEMENTED + AUTOMATED VALIDATION COMPLETE; future capability ordering beyond Slice 10 remains undefined.
The execution-summary behavioural contract is owner-approved in Architecture Section 13.4.
Section 9.2 records its merged PR #157 implementation and automated validation evidence.
The preceding Slice-9 results remain historical and do not validate the new count returns or SUMMARY.
Broader Architecture Section-12 logging and HTTP/API reporting contracts remain separate work.
API Section 6.1 implementation status reconciliation is already approved; HTTP reporting decisions remain separate.
Broader integration/E2E and live validation remain incomplete. Operational Readiness definition/evidence
remains incomplete; Section 9.1 applies the resolved owner placements to Gate-3 evidence. Broader
Operational Recovery / DR is outside V1.0 under G3-D3. Gates 3 and 4 remain future and Version 1.0 remains pre-release.

Work Item Create Payload validation shall additionally cover:

- the exact Create endpoint, HTTP `POST`, `application/json-patch+json` Content-Type, `api-version=7.1` and validation-only query behaviour;
- RFC 6902 JSON Patch array structure, the `add`-only Create profile and exclusion of `replace`, `remove`, `test`, `copy` and `move`;
- the exact five-field allowlist, canonical field order, mandatory Title, mandatory Description and mandatory final `Custom.BacklogGeneratorSourceIdentity` operation;
- optional Acceptance Criteria, mandatory Task Acceptance Criteria omission, optional Tags, absent optional-field omission and no empty placeholder operations;
- valid three-, four- and five-operation payloads, with identity always final and the exact same marker in validation-only and persistent Create;
- exact prepared-value preservation, JSON escaping without semantic transformation, no double HTML escaping, no Markdown re-rendering and no Tags splitting, reordering or renormalisation;
- exclusion of `System.WorkItemType`, additional fields, server-managed fields and relationship operations;
- exclusion of `bypassRules`, `suppressNotifications` and `$expand`;
- validation-only and persistent candidate-payload equivalence; and
- pre-persistence failure for incomplete or incompatible candidates.

Persisted Source Identity and Existing Item Resolution validation shall additionally cover:

- Document 09 remaining authoritative for logical source identity and the digest remaining only its remote persisted representation;
- exact framing bytes for the ASCII `adbg-source-identity-v1` prefix, zero byte, unsigned 32-bit big-endian path byte length, UTF-8 path bytes, unsigned 32-bit big-endian hierarchy-component count, heading-level byte, unsigned 32-bit big-endian title byte length and UTF-8 title bytes;
- UTF-8 without a byte-order mark, byte rather than code-point lengths, Unicode and non-ASCII inputs, no additional Unicode normalisation, and exclusion of newlines, delimiters, JSON framing, locale encoding, platform path conversion and additional whitespace;
- exclusion of Description, Acceptance Criteria, Tags, Azure DevOps IDs, project, organisation, work-item type label, parent ID, remote state and configuration from the digest;
- SHA-256 output as exactly 64 lowercase hexadecimal characters, the exact `adbg:source-id:v1:sha256:` prefix, exact marker-format validation and uppercase or otherwise case-altered marker rejection;
- run-level validation across zero items, one item and multiple unique items;
- duplicate logical identity failure when the same canonical relative source path and ordered complete normalised semantic-heading hierarchy occur more than once in one execution;
- persisted-marker collision failure when structurally distinct logical identities are forced to produce the same complete marker;
- deterministic first failure when multiple duplicate logical identity or persisted-marker collision conditions are present;
- inclusion of roots and descendants from multiple parsed documents in run-level identity validation; and
- confirmation that either run-level identity validation failure prevents compatibility validation, WIQL, Work Item GET, Create, relationship processing and external mutation;
- the fixed custom-field reference, display name, String/single-line-text type, applicability to all four supported types, Create writability, optional process status, absent default and mandatory generator Create value;
- compatibility failure for missing, wrongly typed, read-only, inapplicable, process-required or otherwise incompatible identity-field support and confirmation that the generator performs no process or field provisioning;
- the exact WIQL endpoint, HTTP `POST`, `application/json` Content-Type, `$top=2`, `api-version=7.1`, `@project`, fixed field references, fixed operators, fixed supported type literals and validated-marker insertion;
- absence of Title, path, heading, parent ID, State, Area and caller-controlled fields, operators or fragments from the authoritative WIQL query;
- zero results causing Create, exactly one result causing GET without Create, and two results causing ambiguity failure without further candidate retrieval or Create;
- duplicate IDs, missing or non-numeric IDs, WIQL transport/API failure and malformed result failure before Create;
- the exact Work Item GET endpoint and fields query, and required numeric ID, numeric revision, project, exact type and exact ordinal marker response state;
- canonical project-name verification after project configuration by name or accepted identifier, exact work-item-type and casing verification, and exact ordinal case-sensitive marker verification;
- failure rather than zero-match fallback for missing, null, malformed or conflicting candidate response evidence or GET transport/API failure;
- same Title with different logical identities resolving independently, and unmarked manual Title or hierarchy collisions not being queried heuristically, adopted, warned about solely for matching Title or treated as failures;
- successful existing-ID and revision retention, descendant processing with the reused ID, no Create after resolution and no ordinary field or identity update;
- Description-only, Acceptance Criteria-only and Tags-only changes retaining identity and causing reuse without update;
- heading, ancestor-heading, canonical path rename and identity-significant path-case changes producing changed identities, without rename migration or obsolete-item cleanup;
- secret-safe diagnostics and absence of PATs, Authorization headers, full remote response bodies by default and unnecessary raw logical identities from logs; and
- successful existing-item resolution remaining free of ordinary field or identity updates while authorising only the approved reused-child relationship-state contract for non-root items.

The following known digest vectors shall be tested exactly:

| Canonical path | Ordered hierarchy | Expected SHA-256 | Complete marker |
|----------------|-------------------|-----------------|-----------------|
| `file-a.md` | `(1, Platform)` | `fc590bceef6c25da9e47138a34883f99eadf0e52201fe04fb700a20edc14acaf` | `adbg:source-id:v1:sha256:fc590bceef6c25da9e47138a34883f99eadf0e52201fe04fb700a20edc14acaf` |
| `file-a.md` | `(1, Platform), (2, API)` | `2dd6a0940a9677d61a11c4726af7f0ab39814419cfb9bcdda8c28cfe91751d63` | `adbg:source-id:v1:sha256:2dd6a0940a9677d61a11c4726af7f0ab39814419cfb9bcdda8c28cfe91751d63` |
| `caf\u00e9.md` (`U+0063 U+0061 U+0066 U+00E9 U+002E U+006D U+0064`) | `(1, Cr\u00e8me)` where the title is `U+0043 U+0072 U+00E8 U+006D U+0065` | `d5e7aab193d51ff379aee0fc4c1fdbe4260801e2e8600dbd67d2b21bc95df7bc` | `adbg:source-id:v1:sha256:d5e7aab193d51ff379aee0fc4c1fdbe4260801e2e8600dbd67d2b21bc95df7bc` |

For the non-ASCII vector, the canonical path UTF-8 bytes shall be hexadecimal `63 61 66 c3 a9 2e 6d 64`, and the title UTF-8 bytes shall be `43 72 c3 a8 6d 65`. The complete framed bytes shall be hexadecimal `61 64 62 67 2d 73 6f 75 72 63 65 2d 69 64 65 6e 74 69 74 79 2d 76 31 00 00 00 00 08 63 61 66 c3 a9 2e 6d 64 00 00 00 01 01 00 00 00 06 43 72 c3 a8 6d 65`.

Parent-Child Relationship validation shall additionally cover:

- the exact relationship endpoint, HTTP `PATCH`, `application/json-patch+json` Content-Type, `api-version=7.1` and numeric child ID in the endpoint;
- exactly two JSON Patch operations: a first `test` operation at `/rev` using the current numeric child revision, followed by a second `add` operation at `/relations/-`;
- the exact `System.LinkTypes.Hierarchy-Reverse` relation type and exclusion of `System.LinkTypes.Hierarchy-Forward` and all other relation types;
- the canonical numeric-parent target URL `https://dev.azure.com/{organization}/_apis/wit/workItems/{parentId}`, including no project segment, no `api-version`, no query parameters and no browser/UI URL;
- a relation object containing exactly `rel` and `url`, with no relation attributes or other relation-specific fields;
- absence of ordinary field operations, `validateOnly`, `bypassRules`, `suppressNotifications` and `$expand` from relationship PATCH requests;
- exact HTTP `200 OK` acceptance, a non-empty valid UTF-8 JSON object response with no required properties, ignored unknown response properties and a `None` return;
- rejection through the existing controlled Azure DevOps response-error contract of empty bodies, invalid UTF-8, invalid JSON and top-level JSON arrays, strings, numbers, booleans and `null`;
- exact-`int` child Work Item ID acceptance and rejection of `bool` and non-integer child IDs before URL construction;
- preservation of existing HTTP and transport failures, response consumption and closure, and no retry;
- absence of PATCH-response requirements for `id`, `rev`, revision advancement, `fields`, `relations`, parent-target verification, relationship classification, automatic GET-after-PATCH or a dedicated response model;
- exactly one relationship PATCH for each newly created Feature, Product Backlog Item and Task, no relationship PATCH for a root Epic, and no relationship-state expectation for reused non-root items under this contract;
- permitted direct hierarchy edges Epic → Feature, Feature → Product Backlog Item and Product Backlog Item → Task; rejected direct shortcuts; and exactly one intended immediate parent for each non-root child;
- parent resolution-or-creation before newly created child persistence, immediate child-to-parent relationship PATCH timing, and parent/child ID plus child-revision lifecycle;
- fail-fast behaviour when a relationship PATCH fails, including no later persistent work-item or relationship creation;
- no automatic retry, rollback, deletion, relationship removal or remote-state repair, with already-created remote work items and relationships remaining; and
- responsibility boundaries in which the Documentation Processor supplies source hierarchy, the Backlog Generator coordinates IDs and relationship timing, and the REST Client constructs and transmits the relationship JSON Patch request.

Existing Relationship State and Recovery validation shall additionally cover:

- the exact reused-child relationship-state GET endpoint, HTTP `GET`, `$expand=relations`, `api-version=7.1`, numeric child ID and absence of a `fields` parameter;
- required numeric response `id` equal to the reused child ID and required numeric fresh `rev`, including rejection of missing, null, malformed, non-numeric or mismatched values;
- omitted `relations` and an empty relation array as accepted zero-relation representations;
- rejection of explicit `null` and object, string, number or boolean relation values;
- rejection of non-object array members and mixed valid/invalid arrays;
- rejection of relation members with missing, empty or non-string `rel` or `url` values;
- acceptance of structurally valid relations both without and with optional `attributes`;
- exact case-sensitive `System.LinkTypes.Hierarchy-Reverse` parent evidence and rejection of a case-altered reverse-hierarchy reference;
- ignored well-formed unrelated-only and `System.LinkTypes.Hierarchy-Forward`-only collections;
- CORRECT classification with coexisting well-formed unrelated or forward relations;
- MISSING, CORRECT, wrong-parent, multiple-different-parent, duplicate-same-parent and correct-parent-plus-second-reverse outcomes;
- strict reverse-relation URI rejection for malformed or relative URIs, HTTP, wrong host, wrong organisation, wrong route, query, fragment, extra path, missing ID, non-numeric ID, zero ID and negative ID;
- structurally valid URI parsing followed by numeric intended-parent ID comparison, including equal and differing target IDs without raw full-string equality or unconstrained terminal-ID parsing;
- no separate parent GET;
- use of the fresh relationship-state revision for MISSING repair and exclusion of the earlier Existing Item Lookup revision from the repair `/rev` test;
- exact reuse of the approved Parent-Child Relationship PATCH endpoint, Content-Type, two-operation body, operation order, relation type and canonical target URL;
- successful missing-parent repair, `/rev` conflict and repair transport/API failure;
- no automatic reread, retry or rollback after recovery failure;
- root Epic bypass of relationship GET and PATCH, newly created non-root child bypass of relationship GET, and reused non-root child execution of the relationship GET;
- CORRECT skipping PATCH, MISSING performing the recovery PATCH and CONFLICTING performing no remote mutation;
- descendant blocking until a newly created relationship PATCH succeeds, a reused child is observed CORRECT or a MISSING reused-child relationship is successfully repaired;
- the complete two-run lifecycle in which child creation succeeds, the initial relationship PATCH fails, the rerun resolves both items, observes MISSING, repairs with the fresh revision and then continues descendants;
- absence of remove, replace, move, relation-index, ordinary field-update and identity-update operations and absence of WIQL changes; and
- secret-safe diagnostics containing no PAT, Authorization header, unnecessary full response body or relation URL when the numeric target ID suffices.

Focused root existing/new Work Item lifecycle composition coverage is implemented. It verifies that NEW uses the real resolution path, performs one persistent Create and returns only its ID without relationship work; REUSED uses the real lookup and existing-evidence path, performs no Create and returns the existing ID without relationship work; resolution failure propagates unchanged without Create or relationship work; and Create failure propagates unchanged after one attempt without retry or relationship work. Complete Generator Orchestration coverage is implemented through its final entry coordinator, full preflight, deterministic hierarchy traversal, parent-before-child, descendant-blocking, run-failure and full-hierarchy rerun composition.

Testing shall confirm that source processing order does not imply Azure DevOps rank, priority, state, iteration or business priority.

Validation results shall be documented before Version 1.0 is approved for release.

---

# 9. Acceptance Criteria

Version 1.0 shall be considered successfully validated when all of the following acceptance criteria have been satisfied:

- All approved functional requirements have been successfully implemented.
- All automated tests have completed successfully.
- Integration with Azure DevOps has been successfully validated.
- Azure DevOps work items have been created correctly.
- Parent-child relationships have been created correctly.
- Configuration validation has completed successfully.
- Scrum compatibility validation has completed successfully for standard Scrum and compatible inherited/customised Scrum projects.
- Missing required work-item types, missing or incompatible standard fields, missing or incompatible custom identity-field support, additional project/process rules that prevent candidate creation, validation-only failures and metadata retrieval failures have been validated to stop persistent backlog generation.
- No critical or high-severity defects remain unresolved.
- Complete traceability has been maintained between requirements, implementation and testing.

Acceptance shall be based on the successful completion of the planned validation activities.

---

## 9.1 Review Gate 3 evidence requirements

**APPROVED EVIDENCE FRAMEWORK — no new test execution evidence is claimed.**
The Gate-3 evidence framework is already approved. G3-D1 to G3-D3 are RESOLVED / OWNER APPROVED and
settle summary/live-proof placement and broader DR exclusion alongside existing Sections 5 to 9.
[Release Section 8.1](07-Release.md#81-review-gate-3-operational-readiness-acceptance) owns mandatory
rows, placement decisions and acceptance. [Architecture Section 13](02-Architecture.md#13-review-gate-3-operational-readiness-boundaries)
owns behavioural dependencies. Writing this section does not satisfy an evidence requirement.

[Section 9.4](#94-gate-3-applicationintegration-evidence-mapping) records the application/integration
mapping and historical applicability at the assessed revision. It preserves the mandatory minimum,
live-validation requirements and original execution results below; no new execution is claimed.

### Evidence forms and minimum application integration

Existing unit, component/composition, subprocess, fake REST, stateful rerun and real filesystem/config
results shall be credited with their actual boundaries. The recorded 764/764 full and warnings-as-errors
results, Ruff pass, 95% coverage, 1,394 statements and 64 missed remain historical implementation evidence;
`main.py` remains recorded as 110/0/100% and `__main__.py` as 3/0/100%. These results do not establish
successful complete application E2E or live Services validation. Successful adapter-only subprocesses
that replace `run_process()` are not successful application execution evidence.

Before Gate-3 PASS, the following application-level evidence is mandatory under G3-OWN-D11 Option A:

- At least one successful complete supported package invocation using real argument/configuration loading,
  temporary non-secret configuration and Markdown files, documentation processing, Generator preflight and
  traversal, runtime logging, approved reporting and the required summary, and process outcome/termination.
  A controlled transport substitute may support repeatable automated integration, but the application,
  parser and Generator shall not be replaced by successful no-op collaborators in this evidence.
- Integrated failure evidence for configuration/bootstrap, preflight-before-persistence, downstream
  mutation/relationship failure and the unexpected process fallback, showing no later work after failure.
  Existing evidence may be composed by traceability where it already proves the relevant boundary;
  failures need not all be induced against a live service.
- Evidence of identity-based rerun behaviour and fresh relationship inspection, including child Create
  followed by relationship failure, later MISSING repair without duplicate Create, CORRECT continuation
  and CONFLICTING stop. Existing stateful Generator tests remain valid component evidence; the application
  integration record shall identify which connections to the runtime path are additionally proven.
- Approved logging/reporting acceptance, including configuration success interpretation, event ownership,
  thresholds, duplicate prevention, delivery-failure precedence, `401`/`403` distinctions and rate-limit
  reporting for `429` without sleep/retry. Under G3-D1, the owner-approved summary contract in
  Architecture Section 13.4 requires implementation, validation and recorded evidence before Gate-3
  PASS. Section 9.2 records the merged PR #157 automated summary-validation results.
- Regression and secret-safety evidence for all changed behaviour and the preserved Slice-1-9 boundaries.
  A successful full suite and Ruff result tied to the assessed implementation shall be recorded; evidence
  reuse shall identify the unchanged implementation and why earlier results remain applicable.

Under owner-approved G3-D2, mock-only/fake-transport evidence is insufficient for Gate-3 PASS; minimum
real Services operational proof is mandatory. V1.0 dry-run remains unsupported. A successful reused/CORRECT run with no persistent mutation
still makes Azure requests and is not a substitute for creation/relationship validation.

### Required live Services proof - G3-D2 RESOLVED / OWNER APPROVED

Minimum real Services operational proof shall be complete before Gate-3 PASS; final RC repetition
remains at Gate 4. The proof shall demonstrate a successful supported application invocation against
an approved isolated dedicated test project inside an existing Azure DevOps TEST organisation,
as selected by G3-OWN-D12 Option B; concrete environment values and execution authorisation remain pending.
It shall cover, where applicable to the supported V1.0 path, real connectivity, approved authentication/
authorisation setup, project/field compatibility, validation-only Work Item Create acceptance, actual
creation across the supported hierarchy and work-item types, expected mapped fields and parent-child
relationships, followed by identity-based reuse on a later invocation without duplicate creation.
The evidence shall demonstrate that no automatic retry, rollback or compensation is introduced and
that credential and diagnostic handling remain safe.
The record shall identify the actual process and custom identity-field support; it shall not label an
inherited/customised project as proof of unmodified standard Scrum compatibility.

The owner shall approve a scenario-to-gate matrix covering all existing Section-9 acceptance obligations,
including standard Scrum and compatible inherited/customised Scrum compatibility and rejection scenarios.
Only explicitly allocated scenarios beyond the mandatory minimum proof may remain for Gate 4 through
the Release deferral rule, alongside final live repetition and release evidence. The minimum proof
cannot be deferred; absence of a live environment does not permit mock-only acceptance. Exact project
configuration, permissions, cleanup authorisation and the controlled scenario procedure still require
definition before execution. No live-validation obligation is waived or live execution performed here.

A controlled, repeatable manual procedure with documented results is acceptable; a dedicated automated
live harness is not mandated unless a later approved contract requires automation. The procedure shall
identify the isolated test organisation/project,
approved input, required fields and process compatibility, API Section 6.2 least-privilege scopes and
permissions, runtime-only credential provision, writable log destination, expected results and authorised
mutation boundaries. Credentials shall not appear in source, TOML, CLI arguments, captured diagnostics or
evidence. Any cleanup needs separately authorised scope; application deletion/compensation is not added.

Broader Operational Recovery / DR is OUTSIDE V1.0 under owner-approved G3-D3 and is not deferred to
Gate 4. No new DR/backup infrastructure, generic recovery subsystem or logfile recovery/rotation
validation is required. Existing global-stop, partial-state, identity-reuse and fresh relationship
MISSING/CORRECT/CONFLICTING validation remains required, as does bounded failure/rerun operator guidance.

### Evidence record and findings

For each Release matrix row A-O, the review record shall contain the source document/version/section,
acceptance condition, assessed implementation commit and relevant merged change references, test, manual procedure or document-review
identifier as applicable, environment and input identity without secrets, execution date, expected and actual
outcome, result/artefact reference, known limitations, current status and reviewer. Existing evidence shall
state its component/subprocess/live boundary and applicability to the assessed revision. A procedure that
has not been executed is planned evidence, not a passed result.

G3-REC-R01 reconciles the already-authoritative Section-9 Gate-3 threshold:
**No unresolved CRITICAL or HIGH defects/findings.** This is not a new behavioural or owner decision
and does not relax the existing V1.0 rule.
Findings shall record severity, impact, disposition and closure evidence. If another review uses
BLOCKER/MAJOR/MINOR/EDITORIAL labels, the owner-approved record shall state their critical/high relevance;
labels shall not be silently treated as equivalent or used to evade the threshold. Lower-severity findings
shall not leave a mandatory acceptance condition unsatisfied; any permitted residual work requires an
explicit disposition under the Release deferral rule.

No live operations, new tests, Ruff or pytest runs are performed by this contract-definition revision.
Final RC regression/live repetition and final release evidence remain subject to Gate 4.

---

## 9.2 Execution-summary validation

**MERGED AUTOMATED VALIDATION EVIDENCE — NO LIVE SERVICES VALIDATION CLAIMED.**
**Application/Run Slice 10 — Execution Summary Implementation and Validation — IMPLEMENTED + AUTOMATED VALIDATION COMPLETE.**
PR #157 (implementation `666f7aa`, merge `8e2a57d`) implemented and automatically validated the
approved requirements below. The Slice-10 reconciliation is Approved Baseline; the present PR #162
reconciliation remains Draft. No tests, Ruff, pytest or live Azure DevOps operations are run for this
documentation-only reconciliation; the results recorded here are the supplied PR #157 evidence.

[Architecture Section 13.4](02-Architecture.md#134-execution-summary-behavioural-contract) is
authoritative for owner-approved G3-SUM-D1 to G3-SUM-D9. Tests shall validate the following observable
behaviour; these validation requirements remain unchanged.

- **D1 — Count semantics:** exact non-negative integer count across Epic, Feature, Product Backlog Item
  and Task; new, reused and mixed paths; repaired relationships without double counting; multiple
  documents/roots; and a permitted zero-item success where applicable. Each source item counts once;
  validation-only/other HTTP requests and relationships shall not inflate the count. No action
  breakdown or item inventory shall be added.
- **D2 — Applicability:** summary only after successful configured execution; none on controlled,
  unexpected, configuration, logger-initialisation, pre-application, partial-persistence or
  conflicting/global-stop failure. Include child Create followed by relationship failure and a later
  successful rerun reporting only its own count. Summary absence shall not imply absence of remote mutation.
- **D3 — Ownership and forwarding:** Generator count becomes available only after successful full
  preflight and traversal; configured application execution forwards it unchanged to bootstrap.
  Count values shall not become process exit codes. Preserve exact exception propagation, mutation
  barrier, global stop and the unchanged interfaces listed in Architecture Section 13.4.
- **D4 — Destination/filtering:** exactly one eligible INFO summary attempt at DEBUG/INFO; no delivery
  at WARNING/ERROR/CRITICAL. Verify both logger and handler filtering, current-owned-handler-only
  delivery, root/unrelated/same-named non-owned handler isolation, repeated invocations without stale
  reuse or duplication, and silent stdout/stderr success.
- **D5/D8 — Order and representation:** eligible START, successful application execution, SUMMARY,
  independently eligible COMPLETION, normal return and existing process termination in that order.
  Assert the exact logical message, field order, punctuation and ASCII decimal substitution, including
  zero and multiple-digit values without signs/grouping/leading zeroes. Preserve the logfile envelope,
  timestamp behaviour and record termination; do not require identical timestamps across runs.
- **D6 — Delivery failure:** inject ordinary exceptions in summary formatting and delivery; prove
  unchanged domain success, process outcome and subsequent COMPLETION eligibility, with no retry,
  fallback, replacement diagnostic or `ApplicationLoggingError`. Best effort shall cover summary work
  only. Process-control failures outside `Exception` shall propagate unchanged. Existing lifecycle and
  failure-report delivery boundaries shall retain regression coverage.
- **D7 — Safety:** synthetic sensitive values in source, configuration, remote evidence and delivery
  exceptions shall not enter the summary or secondary diagnostics. Assert the exact summary allowlist
  and absence of titles, IDs, hierarchy, source identities/digests, paths, URLs, organisation/project/
  configuration values, request/response content, exception details, tracebacks, PAT and Authorization.
- **D9 — Complete application evidence:** execute a supported package success with real argument/
  configuration loading, non-secret temporary configuration and Markdown, documentation processing,
  Generator preflight/traversal, runtime logging, exact SUMMARY/COMPLETION and process status 0.
  A controlled transport substitute is permitted; successful no-op application/parser/Generator
  substitutes are insufficient. Preserve the failure/rerun integration obligations in Section 9.1.

Historical Slice-9 764/764 full-suite and warnings-as-errors results, Ruff pass and 95% coverage remain
historical implementation evidence only. The following PR #157 record supplies the Slice-10 evidence
against G3-SUM-D1 to G3-SUM-D9, distinct from earlier adapter-only success.

Section 9.4 records the applicability of this historical result and its package evidence to the
assessed revision; it does not present PR #157 as a new run or as PR #162 evidence.

| PR #157 automated check | Recorded result |
|-------------------------|-----------------|
| Ruff | PASS |
| pytest collected / passed / failed | 824 / 824 / 0 |
| Coverage | 95% |
| Statements / missed | 1,409 / 64 |
| Changed production `generator/orchestration.py` coverage | 100% |
| Changed production `main.py` coverage | 100% |
| `git diff --check` | PASS |

Production changes are in `src/azure_devops_backlog_generator/generator/orchestration.py` and
`src/azure_devops_backlog_generator/main.py`. Merged test evidence is traceable as follows:

| Contract | Merged automated evidence | Proven boundary |
|----------|---------------------------|-----------------|
| D1/D3 | `tests/generator/test_orchestration.py`: `test_generator_counts_source_items_once_across_documents_and_roots`, `test_generator_returns_zero_for_permitted_document_without_semantic_items`, and existing preflight/traversal failure tests | Exact integer count after success; all-created, all-reused and mixed paths; MISSING repair without double counting, CORRECT relationships, multiple documents/roots, zero semantic items and exclusion of HTTP activity. |
| D3 | `tests/test_main.py`: `test_composes_the_configured_application_run_once` and preserved bootstrap/main/process tests | Unchanged forwarding of zero and multidigit counts; bootstrap/main remain `None`-returning and successful process outcome remains 0. |
| D2/D4/D5/D8 | `tests/test_main.py`: successful lifecycle order, filtering, handler isolation, repeated invocation and failure-path tests | Exact zero/multidigit summary; INFO behaviour, logger and handler filtering/threshold suppression, current-handler ownership, silent console, SUMMARY before COMPLETION and no summary on failure. |
| D6/D7 | `tests/test_main.py`: `test_summary_failure_is_silent_best_effort_and_completion_is_independent`, `test_summary_preserves_non_exception_failures` | Ordinary formatting/delivery failures preserve success and independent COMPLETION eligibility without retry, fallback or replacement diagnostics; KeyboardInterrupt, SystemExit, GeneratorExit and other non-Exception BaseException propagation; diagnostic-safety sentinels. |
| D2/D7/D9 | `tests/test___main__.py`: `test_package_summary_with_real_parsing_generator_and_controlled_transport` | Supported package execution with real argument/configuration loading, temporary Markdown, parser, Generator preflight/traversal and logging; only JSON transport is substituted. Success, empty input, partial-persistence/rerun and conflict/global-stop/rerun scenarios prove invocation-local summaries, bounded repair without duplicate creation, exact SUMMARY/COMPLETION, process outcomes and diagnostic safety. |

The implemented logical message is exactly `Execution summary: outcome=success; source_items_processed=N.`
It is constructed only from fixed text, literal success and the Generator-owned count; source,
configuration, transport and exception details are excluded. Its INFO delivery uses only the current
invocation's owned logfile handler with normal logger/handler enablement, levels and filtering.
Ordinary `Exception` failures in summary work are best effort; non-`Exception` BaseException subclasses
propagate. These observations reconcile the implementation; Architecture Section 13.4 remains authoritative.

The integrated evidence uses controlled transport, not live Azure DevOps Services. No live validation
occurred in PR #157. Minimum live Services proof remains pending under Section 9.1 / G3-D2 and Release
row H. The bounded summary evidence supports Release row F; it does not close the wider integration,
logging/HTTP reporting, live-validation or Gate-3 acceptance obligations. No warnings-as-errors result
is claimed for PR #157. No new test execution evidence is produced by this reconciliation.

---

## 9.3 Gate-3 HTTP reporting and closure validation

**HTTP REPORTING — IMPLEMENTED + AUTOMATED VALIDATION COMPLETE; REMAINING GATE-3 EVIDENCE INCOMPLETE.**
[Architecture Section 13.5](02-Architecture.md#135-gate-3-owner-approved-closure-decisions) owns
G3-OWN-D01 to G3-OWN-D14 and reconciliation-only G3-REC-R01. PR #162 (implementation `8515573`,
merge `337116d`) implements and automatically validates D01-D05 against the Approved Baseline
contract. The HTTP requirements below now have merged automated evidence; the remaining non-HTTP
closure requirements still require evidence completion/review. Section 9.2 and all earlier slice
evidence remain historical and unchanged. No source/test changes, Ruff/pytest run or live operation
forms part of this documentation revision.

### HTTP reporting — G3-OWN-D01 to G3-OWN-D05

Merged PR #162 automated coverage validates the following continuing requirements:

- Exact 401 logical message `Azure DevOps authentication failed.`, exact 403 logical message
  `Azure DevOps authorisation failed.` and exact 429 logical message `Azure DevOps rate limit reached.`;
  status categories remain distinct with no unsupported root-cause diagnosis.
- Each specific message replaces `Azure DevOps error.` in BOTH logfile and stderr, with no duplicate
  generic event/report for that failure, one eligible attempt per destination and CRITICAL logfile
  severity. Reporting follows propagated status-aware classification at the process boundary.
  All other HTTP / Azure DevOps REST-client errors retain the generic `Azure DevOps error.` report.
- Role-specific controlled-terminal delivery: only the current invocation owned logfile handler receives
  the event, no root/unrelated/same-named non-owned or stale handler delivery, and preserved
  process-boundary stderr semantics. Lifecycle/SUMMARY filtering and delivery remain unchanged.
- Ordinary secondary logfile-write Exception failure preserves the primary failure, stderr reporting
  and process outcome; no retry, fallback destination, replacement diagnostic or logging recovery.
  Non-Exception BaseException/process-control failures remain unsuppressed.
- D01 safety with synthetic sensitive sentinels: no PAT/derived Authorization material, request/response
  bodies, exception details, tracebacks, local paths, source titles/content, identities/digests, URLs,
  organisation/project names, configuration values, remote IDs or new numeric diagnostics. Preserve
  the existing G3-SUM allowlist; do not add a general redaction framework.
- Preserved HTTP status and lower-level failure propagation, global stop with no later Generator work,
  existing failure outcome `1` and package termination ownership; no retry, sleep/backoff, alternate
  credentials, escalation, rollback or compensation, and no exception-taxonomy redesign.
- Complete 429 Retry-After omission: no reporting inspection, application-report propagation, added
  header parsing, header-derived diagnostics or raw header output. Include header-present cases with
  sensitive/malformed synthetic data to prove it is ignored for reporting.
- Full-suite and Ruff regression evidence after implementation, tied to the assessed implementation
  revision and preserving earlier controlled/unexpected, lifecycle, SUMMARY and failure/rerun behaviour.

The supplied PR #162 validation record is:

| PR #162 automated check | Recorded result |
|-------------------------|-----------------|
| Targeted Ruff | PASS |
| Targeted pytest passed / failed | 652 / 0 |
| Full Ruff | PASS |
| Full pytest collected / passed / failed | 1,018 / 1,018 / 0 |
| Coverage | 95% |
| Statements / missed | 1,414 / 64 |
| Changed production `main.py` coverage | 100% |
| `git diff --check` | PASS |

Only `src/azure_devops_backlog_generator/main.py` changed in production. Lower-layer REST-client
production code, exception taxonomy and `__main__.py` remain unchanged. Merged tests provide this traceability:

| Contract / boundary | Merged automated evidence | Proven scope |
|---------------------|---------------------------|--------------|
| D01-D05 terminal reporting | `tests/test_main.py`: controlled process/category reporting, `test_each_reachable_post_initialisation_controlled_failure_is_logged_once`, owned-handler isolation and repeated-invocation tests | Exact status-specific logfile/stderr replacement without generic duplication; generic fallback for other REST-client errors; CRITICAL severity, diagnostic safety, one eligible delivery attempt, exact integer outcome 1 and current-handler ownership. |
| D02 delivery failures | `tests/test_main.py`: `test_secondary_log_write_failure_preserves_the_primary_controlled_failure`, `test_http_terminal_delivery_retains_filtering_and_stderr_failure_semantics` | Ordinary secondary logfile Exception preserves the primary failure and stderr attempt; non-Exception BaseException propagates; existing filtering and stderr-failure semantics remain unchanged. |
| D05 header omission and retained status | `tests/azure_devops/test_rest_client.py`: `test_http_error_is_controlled_and_discards_the_error_body`, `test_429_headers_are_ignored_through_terminal_reporting` | 401/403/429 status preservation; header-present 429 cases, including sensitive/malformed synthetic Retry-After data, reach terminal reporting without header inspection or disclosure, retry or sleep. |
| Global stop | `tests/generator/test_orchestration.py`: `test_real_generator_orchestration_stops_all_later_work_after_persistence_failure` | 401/403/429 propagation stops later descendants, siblings, roots, documents and persistence operations without retry or credential substitution. |
| Supported package integration | `tests/test___main__.py`: `test_package_summary_with_real_parsing_generator_and_controlled_transport` | Each status at preflight and relationship PATCH, with real argument/configuration loading, parser, Generator and logging; exact safe logfile/stderr reports, outcome 1, global stop, no success SUMMARY/COMPLETION and unchanged package termination ownership. Only JSON transport is substituted. |

No live Azure DevOps Services validation occurred; no live evidence is supplied by PR #162.
These results support Release row E within its automated reporting scope. Section 9.4 now records
application/integration evidence completeness and applicability and D06-D10 event/evidence mapping.
Required live proof remains outstanding; row D remains PARTIALLY SATISFIED and row H NOT SATISFIED.
No warnings-as-errors result or new test execution is claimed here. Gate 3 remains NOT PASSED.

### Evidence interpretations and scenario allocation — G3-OWN-D06 to G3-OWN-D11

D06-D10 require no new runtime events. Evidence review shall credit START for successful configuration
and logging initialisation and reaching application execution, with D06's filtering/best-effort absence
limitations and no claim of processing, connectivity or persistence success. D07 accepts the successful
application path, SUMMARY and traceable automated/integration evidence. D08 additionally requires
successful Generator completion and live Services proof; D09 requires automated Generator/integration
and live remote inspection evidence alongside SUMMARY. SUMMARY remains a processed-source-item count,
not a created-item count; no created/reused counters, per-item events, titles or IDs are added. D10
requires no distinct V1.0 warning taxonomy; WARNING remains a configured threshold feature.

Under D11 Option A, the complete scenario-to-gate matrix shall cover Section-9 obligations. The mandatory
minimum in Section 9.1 and Architecture D11 cannot be deferred: supported application success, required
integrated failures, preflight-before-persistence, downstream mutation/relationship failures, unexpected
fallback, partial-state rerun, MISSING repair, CORRECT continuation, CONFLICTING stop, 401/403/429
reporting/safety, applicable full-suite/Ruff and minimum real Services proof. Eligible remaining scenarios
may be allocated to Gate 4 only with exact requirement/scenario, rationale, receiving gate, responsible
owner, required evidence and completion condition. Gate 4 retains final RC regression and repeated live
validation. No scenario is deferred by this revision; G3-D2 and G3-D3 remain unchanged.

### Live-plan acceptance — G3-OWN-D12

D12 Option B selects an isolated dedicated test project within an existing Azure DevOps TEST
organisation. Before execution, the environment-specific procedure shall document synthetic backlog
input only, the truthfully identified actual supported/inherited-compatible Scrum process, externally
provisioned `Custom.BacklogGeneratorSourceIdentity`, runtime-only least-privilege PAT with
`Project and Team: Read` and `Work Items: Read & write`, project/Area Path permissions and tag-creation
permission only when required. It shall cover real persistent Create and parent-child PATCH, a later
unchanged-input reuse run and remote inspection, with expected/actual results for Section 9.1 proof.
No deliberate rate-limit generation or unapproved disruptive negative scenarios are permitted.

Concrete values and execution authorisation remain pending. Before live execution, record explicit
authorisation either to remove specifically identified synthetic test artefacts or to retain them with
a custodian and review/expiry point. No generator deletion/cleanup capability or runtime deletion
permissions merely for cleanup are added. Evidence shall exclude secrets and prohibited diagnostics;
safe references do not authorise raw diagnostic capture. Gate-4 live repetition remains mandatory.

### Operator review and consolidated dossier — G3-OWN-D13 and G3-OWN-D14

Review the future separate `docs/10-Operator-Guide.md` and discoverable README link against every D13
acceptance topic and the implemented behaviour. Guide creation and review remain pending.

D14 Option A requires one consolidated versioned Gate-3 dossier containing the assessed implementation
commit, governing document versions, relevant merged changes and the A-O index. For every row record
normative source/section, acceptance condition, current status, evidence references and type
(automated/manual/live/document-review), safe environment/input references, execution dates,
expected/actual result, artefact reference, limitations and earlier evidence applicability to the assessed
revision. Include approved owner decisions and the findings register with CRITICAL/HIGH relevance,
owner/disposition and verified closure evidence; explicit permitted D11 Gate-4 deferrals; reviewer;
review date; and final dated owner PASS/NOT-PASSED sign-off. Missing or unexecuted evidence remains
pending. Dossier structure alone cannot satisfy a row or establish Gate-3 PASS.

---

## 9.4 Gate-3 Application/Integration Evidence Mapping

This record maps existing evidence to the mandatory Gate-3 application/integration obligations.
It supports later Release reconciliation and the future consolidated Gate-3 dossier; it changes no
behavioural contract or Release acceptance status. Existing automated evidence is sufficient within
the boundaries below. Required live Services evidence remains separate and incomplete.

### 9.4.1 Assessed Revision and Historical Applicability

The assessed revision is `661102d64180417629ee7a96d36ad5bd40ac5a03` (`main` at review).
The governing Approved Baseline is Architecture 2.48, Roadmap 1.43, API 2.28, Testing 2.38 and
Release 1.37, together with Configuration 1.10 and Documentation Input 0.5 for their contracts.

| Historical record | Implementation / merge | Recorded validation | Applicability |
|-------------------|------------------------|---------------------|---------------|
| PR #157; Section 9.2 | `666f7aa` / `8e2a57d` | Ruff PASS; 824 passed; 95% coverage; 1,409 statements / 64 missed. | Historical Slice-10 provenance: Generator/application count returns, SUMMARY and complete package integration with controlled transport. Continued regression support comes from PR #162. |
| PR #162; Section 9.3 | `8515573` / `337116d` | Targeted pytest 652 passed; full pytest 1,018 passed; targeted/full Ruff PASS; 95% coverage; 1,414 statements / 64 missed; `main.py` 100%; `git diff --check` PASS. | Latest recorded implementation-wide regression evidence, including status-aware HTTP reporting, safety, delivery failures, Retry-After omission and package/global-stop coverage. |

Production source, automated tests and `pyproject.toml` are unchanged from PR #162 implementation
`8515573` / merge `337116d` through assessed revision `661102d`. The source/test/configuration
comparison is empty; PRs #163, #164 and #165 changed documentation only. Therefore the recorded
PR #162 Ruff/full-suite/coverage evidence remains applicable to the unchanged implementation and tests
within its declared automated boundaries. PR #157 remains historical Slice-10 provenance, with
regression support from PR #162; its results are not relabelled as PR #162 results.

No Ruff/pytest execution is newly claimed by this revision, and no live Services result is claimed.
Historical execution dates and artefacts must be referenced truthfully where available; commit dates
are not substitutes for execution dates. Missing result metadata remains identified as missing, not
invented. The future dossier references these records and records available execution artefacts,
dates, reviewer and limitations under Sections 9.1/9.3 and G3-OWN-D14.

### 9.4.2 Evidence Levels and Boundary Rules

| Level | Meaning in this mapping |
|-------|-------------------------|
| Unit (U) | An individual function or decision with supplied values and, where needed, collaborator doubles. |
| Component (C) | A bounded application, relationship or REST component; real behaviour inside that boundary with declared doubles outside it. |
| Filesystem component integration (F) | Real temporary files and configuration loading/validation or Markdown parsing/rendering; synthetic environment and selected injected failures. |
| Generator component integration (G) | Real Generator preflight/traversal and relevant lifecycle/resolution logic over a fake REST boundary and supplied hierarchy/evidence. |
| Package/subprocess integration (P) | Actual package adapter and process/application boundaries inside an isolated child process; the particular substitutions remain explicit. |
| Historical full-suite evidence (H) | Recorded execution result at an identified implementation revision, reused only within demonstrated applicability. |
| Live Services evidence (L) | Executed authorised application behaviour against actual Azure DevOps Services, including required remote inspection. No such result is supplied here. |

Unit evidence is not package evidence. Package evidence using substituted transport is not live
Services evidence. Under Section 9.1, evidence may be composed by traceability: not every mandatory
scenario requires its own complete subprocess test. Substituted collaborators and limitations remain
explicit, and historical evidence applies only where revision applicability is demonstrated.

The file keys below identify exact current test locations used throughout Section 9.4.
`KEY::test_name` denotes that named test in the corresponding file.

| Key | File | Real and substituted boundaries |
|-----|------|--------------------------------|
| PK | [tests/test___main__.py](../tests/test___main__.py) | Package adapter is real. PK-full is defined in Section 9.4.3. Missing-configuration subprocess uses the real loader; fallback subprocess replaces loader/application execution to induce failure. Adapter-only tests replace `run_process()`. |
| M | [tests/test_main.py](../tests/test_main.py) | Real application boundary under test; logging tests use real owned handlers/files unless injecting delivery failure. Loader, processor, REST constructor, Generator or configured application execution are replaced as each test specifies. |
| GO | [tests/generator/test_orchestration.py](../tests/generator/test_orchestration.py) | Full-composition tests use real Generator logic with fake REST and supplied hierarchy. Focused wiring tests additionally substitute preflight/traversal; compatibility-failure propagation substitutes the evaluator. |
| GR | [tests/generator/test_relationships.py](../tests/generator/test_relationships.py) | Classification, lifecycle or recovery boundary with fake REST. Focused delegation tests may also substitute classification, gate or recovery; the two-run recovery test composes real resolution/lifecycle logic. |
| RES | [tests/generator/test_resolution.py](../tests/generator/test_resolution.py) | Real resolution over fake WIQL/GET evidence; no network. |
| ID | [tests/generator/test_identity.py](../tests/generator/test_identity.py) | Real identity/validation logic over supplied source models; deliberate marker substitution for collision evidence. |
| REST | [tests/azure_devops/test_rest_client.py](../tests/azure_devops/test_rest_client.py) | Real request construction, authentication-header construction, JSON and response handling; fake urllib opener/responses, not Services. |
| COMP | [tests/azure_devops/test_compatibility.py](../tests/azure_devops/test_compatibility.py) | Real structural evaluator over supplied metadata fixtures. |
| CFG | [tests/config/test_loader.py](../tests/config/test_loader.py) | Real loader/validator and temporary files with synthetic environment. |
| CFG-M | [tests/config/test_models.py](../tests/config/test_models.py) | Real configuration model with synthetic PAT. |
| DOC | [tests/documentation/test_processor.py](../tests/documentation/test_processor.py) | Real parser and temporary files; unreadable-file failure is injected. |
| DESC | [tests/documentation/test_description_mapping.py](../tests/documentation/test_description_mapping.py) | Real parser/Description preparation and temporary files; selected renderer failures are injected. |

Application evidence resides in M and PK; there is no `tests/application/` directory at this revision.
Earlier component evidence in Section 8, including Acceptance Criteria and Tags mapping, retains its
scope. The package success fixture does not exercise every optional source-field combination.

### 9.4.3 Package Integration Evidence

**PK-full** denotes
`tests/test___main__.py::test_package_summary_with_real_parsing_generator_and_controlled_transport`.
It composes the real CLI/package adapter, configuration loading/validation, runtime PAT acquisition,
Markdown parsing, application/bootstrap, Generator, preflight/compatibility, runtime logging,
execution SUMMARY and process termination. REST endpoint methods, payload builders and endpoint
structural response validation remain real. `AzureDevOpsRestClient.send_json_request` is the
controlled transport substitute; `time.sleep` is guarded against use.

| Parameter combination | Recorded assertions and scope |
|-----------------------|-------------------------------|
| `success` | Three Markdown documents and 12 semantic items; outcome `[0]`; exact SUMMARY count 12 followed by COMPLETION; silent console. |
| `empty` | Permitted Markdown prose with zero semantic items; outcome `[0]`; SUMMARY count 0. This is not absence of eligible input files. |
| `partial-rerun` | Outcomes `[1, 0]`; first PATCH failure leaves two items; later invocation reuses them, repairs MISSING and completes with count 4; only four Creates across both invocations. |
| `conflict-rerun` | Outcomes `[1, 1, 0]`; initial partial state, then conflicting parent evidence and stop, then recoverable evidence and success. The fixture changes the conflict evidence; the application does not repair CONFLICTING state. |
| `http-401-preflight` | One request, zero items, outcome 1, exact authentication report and no SUMMARY/COMPLETION. |
| `http-401-patch` | Two items remain at first PATCH failure; exact authentication report, outcome 1 and no later transport work. |
| `http-403-preflight` | One request, zero items, outcome 1, exact authorisation report and no SUMMARY/COMPLETION. |
| `http-403-patch` | Two items remain at first PATCH failure; exact authorisation report, outcome 1 and no later transport work. |
| `http-429-preflight` | One request, zero items, outcome 1, exact rate-limit report and no SUMMARY/COMPLETION. |
| `http-429-patch` | Two items remain at first PATCH failure; exact rate-limit report, outcome 1 and no later transport work. |

HTTP cases assert one exact stderr message and one CRITICAL logfile report without generic duplication,
no DELETE and no sleep. Rerun failure snapshots have no success SUMMARY/COMPLETION; the successful
summary describes only its own invocation. Synthetic source/configuration/remote sentinels are absent
from application output. Lower-level REST tests separately establish header handling and HTTP parsing.

The child runs an instrumented `-c` harness using `runpy.run_module(..., run_name="__main__")`.
The actual adapter raises `SystemExit`; the harness records it, retains simulated remote state for
reruns and exits the child with the final outcome. This is strong package integration evidence, not
unintercepted repeated OS-process execution or live validation. No real HTTP, TLS, authentication
exchange or Services state is exercised. The fake transport does not independently establish every
remote field/relationship or actual process compatibility.

`PK::test_adapter_boundary_success_subprocess` replaces `run_process()` and proves only adapter
termination. It must not be cited as complete application-success evidence. Conversely,
`PK::test_real_package_subprocess_reports_missing_configuration` exercises the actual `python -m`
missing-configuration path. `PK::test_package_subprocess_real_fallback_suppresses_unexpected_details_and_traceback`
exercises the real fallback before/after logger initialisation with lower collaborators substituted.

### 9.4.4 Requirement-to-Evidence Mapping

Document abbreviations are A = Architecture, API = API Specification, Cfg = Configuration and
DI = Documentation Input. Sections 9.1/9.3 and A Section 13.5 D11 govern every row. Levels and
collaborator boundaries are defined in Section 9.4.2; historical execution applicability is H in
Section 9.4.1. All rows have sufficient reusable automated evidence within those boundaries.

In the live column, **Yes** identifies required related corroboration in the minimum live proof,
not a requirement to induce every negative case live. **No separate case** means the specific local
or negative boundary can be evidenced automatically; it does not waive G3-D2 or D11 allocation review.

| Obligation / normative source | Strongest reusable tests/evidence | Level | Proven boundary and key limitation | Additional live corroboration |
|-------------------------------|----------------------------------|-------|------------------------------------|-------------------------------|
| Complete supported application success; Section 9.1, A 13.4 D9 | PK-full `success` | P | Real configuration/parser/Generator/logging/adapter success; JSON transport substituted. | Yes: actual Services application success. |
| Configuration/bootstrap success; Cfg 5–8, A 7.1.2–7.1.3 | `CFG::test_uses_the_canonical_default_configuration_path`, `CFG::test_loads_the_explicit_cli_configuration_file`, `M::test_composes_application_bootstrap_with_the_exact_collaborator_values`; PK-full | F/C/P | Default/explicit loading and exact bootstrap composition; M uses loader/application doubles, PK-full exercises explicit real loading. | No separate case. |
| Controlled configuration failure; Cfg 7, A 7.1.4–7.1.6 | `PK::test_real_package_subprocess_reports_missing_configuration`, `CFG::test_reports_malformed_toml`, `CFG::test_requires_a_non_empty_runtime_pat`, `M::test_propagates_configuration_failure_without_invoking_slice_1` | F/C/P | Fixed failure, no application continuation; actual missing-file package result 1 without logfile. Other cases are composed evidence. | No separate case. |
| Source/documentation failure; DI 13, A 7.1.1/7.3/11 | `DOC::test_rejects_invalid_utf8`, `DOC::test_reports_an_unreadable_matching_file`, `DESC::test_rejects_missing_or_whitespace_only_description`, `M::test_propagates_documentation_failure_without_constructing_other_collaborators`, `M::test_run_process_maps_each_controlled_failure_to_one` | F/C | Parser failures, no later REST construction/Generator and category reporting; not one malformed-source package run. | No separate case. |
| Logging initialisation failure; Cfg 6.4, A 7.1.6 | `M::test_logging_initialisation_failure_is_a_controlled_application_error`, `M::test_partial_logging_initialisation_failure_closes_the_created_handler` | C | Fixed stderr, outcome 1, no active/fallback handler; injected constructor/attachment failure. | No separate case. |
| Project/metadata preflight failure; API 7.1, A 7.4 | `GO::test_project_failure_propagates_once_without_later_preflight_requests`, `GO::test_metadata_failure_propagates_without_later_metadata_or_validation_requests`; PK-full HTTP preflight cases | G/P | No later preflight/persistence; package cases stop after one request. Fake REST failure. | Yes for real successful preflight; no mandated live rejection case. |
| Structural compatibility; API 7.1, Section 9 | `COMP::test_accepts_complete_compatible_evidence_without_returning_persistence_authority`, `COMP::test_rejects_missing_required_work_item_type`, `COMP::test_rejects_missing_required_type_specific_field_evidence`, `COMP::test_rejects_incompatible_global_identity_evidence`, `COMP::test_rejects_incompatible_identity_type_specific_evidence`, `GO::test_compatibility_failure_prevents_every_validation_only_request` | U/G | Real evaluator acceptance/rejection plus injected evaluator failure propagation in GO; fixtures do not prove actual project compatibility. | Yes: actual process/field compatibility. |
| Per-candidate validation; API 7.1, A 7.4 | `GO::test_coordinates_complete_preflight_in_source_order_and_returns_minimal_state`, `GO::test_validation_checks_each_same_type_candidate_with_its_actual_optional_values`, `REST::test_validates_work_item_create_with_the_exact_endpoint_contract` | G/C | Every actual candidate checked in order, optional-value differences and exact validation-only request; fake acceptance. | Yes: actual candidate acceptance. |
| Candidate rejection; API 7.1 | `GO::test_validation_failure_stops_after_the_failing_candidate_without_retry`, `GO::test_real_generator_orchestration_preflight_failure_preserves_mutation_barrier`, `REST::test_validation_only_create_uses_the_existing_controlled_http_failure` | G/C | Mid-sequence rejection stops before persistence; no claim about an actual target's rejecting rule. | No separate case; D11 scenario allocation remains. |
| Persistence barrier; A 7.4, API 7.1 | `GO::test_real_generator_orchestration_crosses_mutation_barrier_before_traversal`, `GO::test_real_generator_orchestration_preflight_failure_preserves_mutation_barrier`, `GO::test_rejects_malformed_preflight_state_before_persistent_operations` | G | Complete validation before lookup/mutation; invalid state/failure prevents traversal. Fake REST. | Yes: real supported execution corroboration. |
| Identity/collision rejection; API 8.3.1, DI 12 | `ID::test_duplicate_logical_identity_takes_precedence_over_marker_collision`, `ID::test_distinct_logical_identities_with_one_complete_marker_fail`, `GO::test_source_identity_failure_prevents_all_rest_activity` | U/G | Duplicate/collision failure before external work; collision fixture deliberately forces marker equality. | No separate case. |
| Persistent Create; API 8.1, A 7.4 | `GO::test_creates_a_new_root_once_and_returns_only_its_id`, `GR::test_coordinates_new_child_relationship_lifecycle`, `REST::test_creates_work_item_with_the_exact_persistent_endpoint_contract`; PK-full | C/G/P | One Create and real request contract; simulated rather than actual persistence. | Yes. |
| Parent-child PATCH; API 8.2 | `GR::test_coordinates_new_child_relationship_lifecycle`, `REST::test_builds_the_exact_parent_child_relationship_json_patch`, `REST::test_patches_parent_child_relationship_with_the_exact_endpoint_contract`; PK-full | U/C/P | Immediate PATCH with Create ID/revision and exact payload/endpoint; no independent Services inspection. | Yes. |
| Downstream failure/global stop; A 7.4/11, API 10 | `GO::test_real_generator_orchestration_stops_all_later_work_after_persistence_failure`, `GO::test_failure_stops_later_sibling_root_and_document`, `GO::test_relationship_patch_failure_stops_later_work`; PK-full HTTP PATCH cases | G/P | No later descendants/siblings/roots/documents or transport; GO status injection is at resolution after prior persistence. | No separate negative case. |
| Unexpected application fallback; A Slice 9 | `M::test_run_process_handles_unexpected_exception_after_exactly_one_main_call`, `PK::test_package_maps_real_unexpected_fallback_to_system_exit_one`, `PK::test_package_subprocess_real_fallback_suppresses_unexpected_details_and_traceback` | C/P | Actual fixed fallback/outcome/traceback suppression; lower failure-producing collaborators substituted. | No separate case. |
| Accepted partial persistence; A 11, API 8.5 | `GR::test_recovers_a_created_child_on_a_second_run_after_initial_relationship_failure`; PK-full `partial-rerun` | C/P | Created items survive PATCH failure without success records; remote state is simulated. | No forced live partial failure required. |
| Later invocation recovery; API 8.5, Section 9.1 | `GO::test_later_run_recovers_created_child_without_duplicate_create`; PK-full `partial-rerun` / `conflict-rerun` | G/P | Later invocation can reuse/repair/complete; not automatic retry or independent OS-process recovery evidence. | Yes: later unchanged-input live invocation. |
| Identity-based reuse; API 8.3–8.4, DI 12 | `RES::test_resolves_one_matching_work_item_as_verified_existing_evidence`, `RES::test_rejects_ambiguous_wiql_evidence_without_retrieving_a_work_item`, `RES::test_rejects_conflicting_existing_work_item_evidence`; PK-full reruns | C/P | Valid identity authorises reuse; ambiguous/conflicting evidence does not authorise Create. No real WIQL execution. | Yes. |
| Fresh relationship inspection; API 8.5 | `GR::test_recovers_a_created_child_on_a_second_run_after_initial_relationship_failure`, `REST::test_retrieves_work_item_relationship_state_with_the_exact_get_contract` | C | Fresh GET/revision used for repair; fake response and retained simulated state. | Yes: actual reused-state inspection. |
| MISSING repair; API 8.5 | `GR::test_recovers_missing_parent_relationship_with_fresh_evidence`, `GO::test_reused_non_root_missing_relationship_repairs_before_descendant`; PK-full `partial-rerun` | C/G/P | Missing parent repaired before descendants with fresh revision; no generic repair. | No forced live partial-failure case required. |
| CORRECT continuation; API 8.5 | `GR::test_gates_correct_reused_child_for_descendant_processing_without_rest_operation`, `GO::test_correct_reused_non_root_allows_descendant_processing`, `GO::test_generator_counts_source_items_once_across_documents_and_roots` | U/G | CORRECT skips PATCH and permits descendants, including all-reused/mixed Generator paths; no dedicated CORRECT package parameter. | Yes: live unchanged-input reuse corroboration. |
| CONFLICTING stop; API 8.5 | `GR::test_classifies_reused_child_relationship_state`, `GR::test_blocks_conflicting_reused_child_descendant_processing_without_rest_operation`, `GO::test_conflicting_reused_non_root_stops_descendant_and_later_work`; PK-full `conflict-rerun` | U/G/P | Wrong/multiple/duplicate parents block repair/continuation; conflict is simulated. | No disruptive live conflict case required. |
| HTTP 401; API 6.1, A 13.5 D01–D03 | `REST::test_http_error_is_controlled_and_discards_the_error_body`, `M::test_each_reachable_post_initialisation_controlled_failure_is_logged_once`; PK-full 401 cases | C/P | Exact authentication report replaces generic in both destinations; no diagnosis of expiration/revocation. | No separate case. |
| HTTP 403; API 6.1–6.2, A 13.5 D04 | `REST::test_http_403_is_controlled_without_retry_or_credential_disclosure`, `M::test_each_reachable_post_initialisation_controlled_failure_is_logged_once`; PK-full 403 cases | C/P | Distinct exact authorisation report and preserved failure; no claim of identifying missing permission. | Real permissions require live proof, not a forced 403. |
| HTTP 429 / Retry-After omission; API 6.1/11, A 13.5 D05 | `REST::test_429_headers_are_ignored_through_terminal_reporting`; PK-full 429 cases | C/P | Exact rate-limit report; no header access, sleep or disclosure; package transport alone does not exercise headers. | No deliberate throttling required. |
| Generic Azure DevOps REST failure; API 6.1 | `M::test_each_reachable_post_initialisation_controlled_failure_is_logged_once`; PK-full first rerun failure | C/P | Other HTTP/base/transport/response/compatibility failures retain `Azure DevOps error.`; not every status is a package case. | No separate case. |
| Secret-safe reporting; A 10, Slice 9, 13.4 D7, 13.5 D01 | `M::test_each_reachable_post_initialisation_controlled_failure_is_logged_once`, `M::test_unexpected_events_are_secret_safe_owned_and_not_duplicated_across_invocations`; PK-full; Section 9.4.6 | C/P | Fixed output and sentinel exclusions; not redaction of all internal exceptions or review of live artefacts. | Yes: live-procedure/evidence safety. |
| Logger ownership/isolation; A 7.1.6–7.1.8, 13.4 D4, 13.5 D02 | `M::test_application_events_bypass_non_owned_named_root_and_unrelated_handlers`, `M::test_repeated_invocations_replace_only_owned_handlers_and_do_not_duplicate_records`, `M::test_configuration_error_has_no_file_event_and_deactivates_a_stale_handler` | C | Current handler only, stale closure and no duplicates; application work substituted. | No separate case. |
| Logfile delivery failure; A 7.1.6, Slice 9, 13.4 D6, 13.5 D02 | `M::test_secondary_log_write_failure_preserves_the_primary_controlled_failure`, `M::test_unexpected_log_failure_is_secondary_without_retry_or_fallback`, `M::test_summary_failure_is_silent_best_effort_and_completion_is_independent` | C | Ordinary secondary failures preserve outcome and applicable stderr/COMPLETION; no guaranteed log delivery or recovery. | No separate case. |
| START; A 7.1.8, 13.5 D06 | `M::test_successful_run_emits_only_eligible_fixed_lifecycle_records_in_order`; PK-full | C/P | Exact INFO START after configuration/logger initialisation; filtering/best effort limits absence interpretation. | No separate case. |
| SUMMARY; A 13.4, Section 9.2 | `GO::test_generator_counts_source_items_once_across_documents_and_roots`, `GO::test_generator_returns_zero_for_permitted_document_without_semantic_items`, `M::test_composes_the_configured_application_run_once`; PK-full | G/C/P | Successful invocation-local processed-source count, zero and created/reused/mixed paths; not a mutation inventory. | No separate summary case; D08/D09 still require live proof. |
| SUMMARY filtering; A 13.4 D4 | `M::test_summary_honours_logger_and_handler_filtering`, `M::test_summary_accepts_replacement_records_from_normal_logger_filters`, `M::test_successful_run_emits_only_eligible_fixed_lifecycle_records_in_order` | C | Logger/handler filters, thresholds and disabled/no-handler cases; no guaranteed delivery. | No separate case. |
| COMPLETION; A 7.1.8, 13.4 D5–D6 | `M::test_successful_run_emits_only_eligible_fixed_lifecycle_records_in_order`, `M::test_lifecycle_delivery_failure_preserves_silent_success_without_retry_or_fallback`, `M::test_summary_failure_is_silent_best_effort_and_completion_is_independent`; PK-full | C/P | Separate exact event after normal return/SUMMARY, independently eligible after ordinary summary failure; not remote inspection. | No separate case. |
| Failure without SUMMARY/COMPLETION; A 13.4 D2 | `M::test_each_reachable_post_initialisation_controlled_failure_is_logged_once`, `M::test_unexpected_exception_after_start_reports_failure_without_completion_or_detail`, `PK::test_real_package_subprocess_reports_missing_configuration`; PK-full failures | C/P | Failed and partial runs emit no success records; absence does not prove absence of mutation. | No separate case. |
| No retry/backoff; API 6.1/11, A 13.3 | `REST::test_network_and_timeout_failures_are_controlled_without_retry`, `REST::test_persistent_create_preserves_http_failure_without_retry`, `REST::test_parent_child_relationship_patch_preserves_http_failure_without_retry`, `REST::test_429_headers_are_ignored_through_terminal_reporting`; PK-full | C/P | Single attempts, stopped work and guarded sleep; no actual network failure in package evidence. | Yes: live record must retain approved behaviour. |
| No rollback/compensation; A 11/13.3, API 8.5 | `GR::test_recovers_a_created_child_on_a_second_run_after_initial_relationship_failure`, `GO::test_real_generator_orchestration_stops_all_later_work_after_persistence_failure`; PK-full | C/G/P | Partial state retained and no later compensation; HTTP cases exclude DELETE. Simulated state. | Yes: live record must retain approved behaviour. |
| No duplicate Create during valid reuse; API 8.4 | `GO::test_reuses_root_without_create_or_relationship_work`, `GO::test_later_run_recovers_created_child_without_duplicate_create`; GR two-run test in Section 9.4.5; PK-full reruns | C/G/P | Existing valid identities skip Create across simulated invocations; no guarantee for changed identities or arbitrary external concurrency. | Yes: actual no-duplicate inspection. |
| Process-control/stderr boundaries; A Slice 9, 13.4 D6, 13.5 D02 | `M::test_lifecycle_best_effort_does_not_swallow_process_control_exceptions`, `M::test_unexpected_boundaries_preserve_process_control_exceptions`, `M::test_summary_preserves_non_exception_failures`, `M::test_http_terminal_delivery_retains_filtering_and_stderr_failure_semantics`, `M::test_unexpected_stderr_delivery_failure_propagates_without_retry_or_fallback` | C | Tested non-Exception failures and stderr errors propagate; no blanket outcome-1 guarantee for interruptions/broken output. | No separate case. |

Controlled-terminal HTTP delivery retains its role-specific owned-handler profile: handler filtering
applies, while logger filtering/disabled state is not globally imposed on that direct profile.
SUMMARY separately applies normal logger and handler filtering. This mapping does not harmonise
historical delivery profiles or add events. No missing mandatory automated test is identified.

### 9.4.5 Stateful Failure and Rerun Evidence

| Existing test/scenario | Stateful observation | Limitation |
|------------------------|----------------------|------------|
| `GR::test_recovers_a_created_child_on_a_second_run_after_initial_relationship_failure` | Real resolution/lifecycle first Creates child 17 at revision 3, then PATCH fails. Second resolution reuses the child; fresh relationship GET supplies revision 8 for repair. Exactly one Create across both simulated runs. | Fake REST retains the item; no Services operation. |
| `GO::test_later_run_recovers_created_child_without_duplicate_create` | Repeated traversal retains fake work items; the fixture enables rediscovery and clears the injected PATCH failure. Create list remains only Epic and Feature. | Supplied preflight state and fake discoverability; not a fresh OS-process invocation. |
| PK-full `partial-rerun` | Connects surviving items, identity reuse and MISSING repair to real configuration/parser/Generator/logging/package outcomes and one later successful count. | Invocations share the instrumented child and simulated remote dictionaries. |
| PK-full `conflict-rerun` | Connects CONFLICTING stop to fixed process reporting and absence of success records, followed by success when the supplied state permits repair. | The fixture changes conflicting evidence; no application conflict repair is claimed. |

Together with the barrier, global-stop, resolution and relationship cases in Section 9.4.4, existing
evidence demonstrates validation before persistence, global stop after the first relevant failure,
legitimate partial persistence, later invocation recovery, identity reuse, no duplicate Create,
MISSING-only repair, CORRECT continuation, CONFLICTING stop, no automatic retry and no
rollback/compensation. Later invocation recovery is not an automatic retry within the failed run.

**No mandatory Gate-3 failure/rerun automated obligation is currently unsupported.** This does not
prove actual remote Services reuse, remote duplicate absence or independently inspected relationships.

### 9.4.6 Secret-Safety Evidence

This assessment concerns supported process/application reporting under Architecture Slice 9,
G3-SUM-D7 and G3-OWN-D01. It does not state that all internal/lower-level exceptions are redacted.
Some lower-level exceptions retain causes or numeric relationship context; approved fixed reporting
does not emit those values. Direct lower-level callers and non-Exception propagation retain their
separate contracts. No general redaction framework is introduced.

| Prohibited material | Applicable existing evidence | Proven scope / limitation |
|---------------------|------------------------------|---------------------------|
| PAT | `CFG-M::test_configuration_keeps_the_runtime_pat_out_of_its_representation`, `CFG::test_rejects_a_pat_toml_key_without_exposing_its_value`; PK-full | Synthetic PAT excluded from model representation, invalid-key diagnostics and application output; not a live credential audit. |
| Derived Authorization | `REST::test_http_403_is_controlled_without_retry_or_credential_disclosure`, `M::test_each_reachable_post_initialisation_controlled_failure_is_logged_once`; PK-full | REST test checks actual synthetic Basic material against exception representation/state; terminal tests exclude Authorization sentinels. PK-full bypasses Basic construction. |
| Exception detail | `M::test_each_reachable_post_initialisation_controlled_failure_is_logged_once`, `M::test_unexpected_events_are_secret_safe_owned_and_not_duplicated_across_invocations` | Exact fixed output; sentinel exception string/repr methods fail if called. |
| Cause/context/traceback | M unexpected-event test above; `PK::test_package_subprocess_real_fallback_suppresses_unexpected_details_and_traceback` | Handled Exception fallback excludes causes/context and native traceback; not blanket suppression of process-control failures. |
| Request/response body | M controlled/unexpected sentinel tests above; `REST::test_http_error_is_controlled_and_discards_the_error_body`, `REST::test_429_headers_are_ignored_through_terminal_reporting`; PK-full | Body sentinels excluded from reports; no claim of erasing all request/exception-chain memory. |
| URL and local path | `M::test_run_process_does_not_render_controlled_failure_detail`, M unexpected-event test; PK-full | Fixed output excludes supplied URLs, paths and temporary directory. |
| Organisation/project/configuration values | `M::test_successful_run_emits_only_eligible_fixed_lifecycle_records_in_order`, M unexpected-event test; PK-full | Supplied configuration sentinels excluded; future live artefacts remain unreviewed. |
| Source title/content/hierarchy | M controlled/unexpected sentinel tests; PK-full | Real parsed synthetic Markdown excluded from package output; no per-item diagnostic entitlement. |
| Source identities/digests | M controlled HTTP sentinel cases; PK-full | Synthetic digest and generated identity markers excluded, including each identity retained by the package fixture. |
| Remote IDs | M controlled HTTP sentinel cases; PK-full | Numeric remote/conflict sentinels and exact output checks; not generic numeric redaction. |
| Retry-After | `REST::test_429_headers_are_ignored_through_terminal_reporting` | Sensitive, malformed and numeric header values tested; no header access, output or sleep. |
| Other prohibited dynamic/numeric diagnostics | Exact-message/LogRecord assertions in M; `M::test_summary_failure_is_silent_best_effort_and_completion_is_independent`; PK-full | Approved fixed output and summary count allowlist, with silent secondary failures. Contract prohibition remains broader than an exhaustive enumeration of sentinel values. |

The evidence establishes approved output allowlists and representative direct exclusions, not a test
for every conceivable secret value. The summary-specific processed-count and normal logfile-envelope
permissions remain unchanged. Concrete live-procedure and resulting evidence safety still require
review under Release row I, G3-D2 and G3-OWN-D12; automated safety alone does not close that row.

### 9.4.7 D06–D10 Applicability

Architecture Section 13.5 remains authoritative for these approved no-new-event interpretations.

| Decision | Approved interpretation and automated applicability | Remaining limitation |
|----------|-----------------------------------------------------|----------------------|
| D06 — configuration success | START establishes that configuration loading/validation and logger initialisation completed and application execution was reached. M lifecycle-order/initialisation tests and PK-full connect this interpretation to the runtime path. | Does not prove parsing, connectivity or persistence; filtering/best effort may suppress START, so absence does not establish validation failure. |
| D07 — documentation processing | Successful application path + SUMMARY + parser/application/integration evidence is sufficient. PK-full exercises real parsing; Section-8 source-mapping tests retain detailed coverage. | No new processing-success event, source titles, paths or document counters are required. |
| D08 — communication | Automated package/REST/Generator evidence exists and connects successful Generator completion to SUMMARY. | Live Azure DevOps Services communication proof remains mandatory; substituted transport cannot provide it. |
| D09 — creation/reuse | Automated Create/PATCH/reuse/rerun evidence exists and connects to SUMMARY. | Live remote creation/reuse inspection remains mandatory. SUMMARY is a processed-source count, not a mutation inventory or created-item count. |
| D10 — warnings | No distinct warning taxonomy/event is required. `CFG::test_normalizes_logging_level_and_validates_its_type` and M five-threshold tests support WARNING as a configured logging threshold. | No approved warning-worthy condition exists; no warning scenario is invented. |

### 9.4.8 Evidence Classification

**A. Sufficient existing automated evidence**

Application success; configuration/source failures; preflight/barrier; Create/PATCH contracts;
global stop; unexpected fallback; partial rerun; identity reuse; MISSING/CORRECT/CONFLICTING;
lifecycle/SUMMARY; HTTP reporting; secret-safe reporting; handler/delivery behaviour; and no
retry/backoff/rollback/compensation are supported within the declared automated boundaries.

**B. Existing evidence requiring traceability/applicability documentation**

This Draft records the B/D/G/I/J consolidated mapping, D06–D10 applicability, component/package
boundaries, stateful-rerun limitations, PR #157/#162 provenance and applicability to `661102d`.
Review and baseline promotion of this record remain pending; later Release reconciliation and
the consolidated dossier should reference it rather than duplicate all test prose.

**C. Genuine missing mandatory evidence**

- Minimum real Azure DevOps Services validation under Section 9.1 / G3-D2.
- D08 live communication proof.
- D09 live creation/reuse remote inspection.
- Concrete live-procedure/evidence safety confirmation under Release row I / G3-OWN-D12.
- Broader later findings/dossier/sign-off governance work under D11/D14 and Release rows M/N/O.

**No missing mandatory automated test has been identified.** No new automated test is required by
this reconciliation; the remaining live and governance obligations are not satisfied by that conclusion.

### 9.4.9 Remaining Live-Only Evidence

Existing automated tests cannot establish the following required actual-environment observations:

- Real Services connectivity and authenticated communication.
- Real least-privilege PAT scopes and project/Area Path permissions, including tag-creation permission
  only when required.
- Actual target process compatibility, identified truthfully as supported Scrum or inherited/customised
  compatible Scrum, and actual required standard/type-specific field compatibility.
- Actual `Custom.BacklogGeneratorSourceIdentity` compatibility and external prerequisite provisioning.
- Actual candidate validation-only acceptance by the target project/process.
- Real persistent Create across the supported hierarchy/work-item types and actual mapped remote fields.
- Real parent-child PATCH and independent remote inspection of items and relationships.
- A later unchanged-input invocation, real identity reuse and real no-duplicate verification.
- D08 live communication and D09 live creation/reuse inspection evidence alongside the automated record.
- Safe live credential handling and safe collection/review of live evidence without prohibited diagnostics.

Section 9.1 and G3-OWN-D12 retain the environment-specific prerequisites: an isolated dedicated project
inside an existing TEST organisation, synthetic approved input, truthful process/field identification,
least privilege, writable logging, expected/actual results, explicit mutation authorisation and an
approved cleanup-or-retention decision. No live execution is authorised or performed by this revision.

No automated live harness is required; controlled manual execution with documented results is acceptable.
Deliberate throttling/429 generation and disruptive negative scenarios are not required by this evidence
mapping and are not authorised. This does not waive Section-9 rejection scenarios or the D11 allocation
review. Inherited/customised Scrum evidence must be labelled truthfully and must not be represented as
proof of unmodified standard Scrum. Minimum Gate-3 live proof cannot be deferred; final RC regression
and repeated live validation remain at Gate 4.

### 9.4.10 Release-Row Implications

[Release Section 8.1](07-Release.md#81-review-gate-3-operational-readiness-acceptance) owns acceptance
statuses. The following records potential implications only; no row is promoted by this Draft.

| Row | Current status | Potential implication of accepted mapping | Remaining boundary |
|-----|----------------|-------------------------------------------|--------------------|
| B — operational implementation completeness | PARTIALLY SATISFIED | Mapping establishes no identified missing mandatory Gate-3 production capability and connects implementation to reusable tests. Later Release reconciliation may assess whether B can become SATISFIED. | This does not close D/H live evidence or imply Gate-3 PASS. |
| D — observability/logging | PARTIALLY SATISFIED | Automated event/reporting mapping and D06–D10 applicability become complete. | D08/D09 live evidence remains; mapping alone cannot make D SATISFIED. |
| G — integration/system validation | PARTIALLY SATISFIED | Integrated success/failure/rerun evidence becomes explicitly traceable, with actual collaborator boundaries. Later Release reconciliation may assess whether G can become SATISFIED. | Required live Services proof remains independently under H / G3-D2. |
| I — security/secret safety | PARTIALLY SATISFIED | Automated reporting/security evidence and preserved protections become traceable. | Live-procedure/evidence safety remains; mapping alone cannot make I SATISFIED. |
| J — failure/rerun behaviour | PARTIALLY SATISFIED | Failure/rerun behaviour becomes fully connected to runtime/package evidence. Later Release reconciliation may assess whether J can become SATISFIED. | Actual Services reuse/inspection remains required under H/D09. |

The future versioned Gate-3 dossier should reference this detailed mapping and add its required A–O
index, execution metadata/artefacts, live records, findings, explicit permitted deferrals, reviewer and
dated owner sign-off. Release should receive resulting acceptance-state reconciliation later.
No Release status changes, no Slice 11 is allocated, Gate 3 remains NOT PASSED, Gate 4 remains FUTURE
and Version 1.0 remains PRE-RELEASE. GUI governance is unchanged; broader DR remains outside V1.0
under G3-D3 rather than deferred to Gate 4.

---

# 10. Defect Management

Defects identified during testing shall be recorded, evaluated and resolved in a controlled manner.

The defect management process shall include:

- Defect identification.
- Severity assessment.
- Root cause analysis where appropriate.
- Corrective implementation.
- Regression testing.
- Defect closure following successful verification.

Resolved defects shall remain traceable through version control and project documentation.

---

# 11. Traceability

This Testing Strategy defines the quality assurance activities supporting implementation of the approved documentation baseline.

Traceability shall be maintained between:

- Product Requirements Document
- Software Architecture Document
- Development Roadmap
- Development Standards
- API Specification
- Testing Strategy
- Azure DevOps Backlog
- Source Code
- Test Documentation

Testing activities shall remain aligned with the approved documentation baseline and shall not introduce validation outside the scope of the approved requirements.

---

# 12. Approval

Approval of a document version requires:

- Completion of the editorial review.
- Approval of that document version.
- Creation of the corresponding Approved Baseline.
- Commit to the project repository using the agreed Git workflow.

The document metadata and Version History record whether the current version has completed this approval process.

Subsequent modifications shall follow the established documentation governance process and be recorded through Version History.
