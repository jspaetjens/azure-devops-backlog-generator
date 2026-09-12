# Azure DevOps Backlog Generator

# Release Management

> *This document defines the release management process, versioning strategy and deployment governance for Version 1.0 of the Azure DevOps Backlog Generator.*

**Version:** 1.33

**Status:** Draft

**Last Updated:** 2026-09-12

**Target Release:** v1.0.0

**License:** MIT

**Author:** Jack Spaetjens

**Revision scope:** This Draft records owner-approved G3-SUM-D1 to G3-SUM-D9.
The execution-summary behavioural decisions are approved; their implementation and validation
remain pending. The approved starting baseline is main at `cff3397`. Historical slice contracts,
`None` returns, summary exclusions and recorded test results below describe their original
implementation boundaries; they do not override the current summary contract in
[Architecture Section 13.4](02-Architecture.md#134-execution-summary-behavioural-contract).
Historical references to pending API Section 6.1 status reconciliation describe the earlier
baseline; this Draft reconciles that status only. HTTP reporting decisions remain separate.
Gate 3 remains NOT PASSED, Gate 4 FUTURE and Version 1.0 PRE-RELEASE; no Slice 10 is allocated.

---

# Version History

| Version | Date | Status | Author | Description |
|----------|------------|-------------------|-----------------|------------------------------------------------|
| 0.1 | 2026-07-31 | Draft | Jack Spaetjens | Initial Release Management document. |
| 1.0 | 2026-07-31 | Approved Baseline | Jack Spaetjens | Initial approved Release Management baseline. |
| 1.1 | 2026-08-27 | Approved Baseline | Jack Spaetjens | Recorded the current pre-release implementation status. |
| 1.2 | 2026-08-27 | Approved Baseline | Jack Spaetjens | Updated the current pre-release implementation status through existing/new Work Item resolution. |
| 1.3 | 2026-08-28 | Approved Baseline | Jack Spaetjens | Updated the current pre-release implementation status through Persistent Work Item Create transport. |
| 1.4 | 2026-08-28 | Approved Baseline | Jack Spaetjens | Updated the current pre-release implementation status through Parent-Child Relationship JSON Patch construction. |
| 1.5 | 2026-08-28 | Approved Baseline | Jack Spaetjens | Updated the current pre-release implementation status through Parent-Child Relationship HTTP PATCH transport. |
| 1.6 | 2026-08-28 | Approved Baseline | Jack Spaetjens | Updated the current pre-release implementation status through reused-child relationship-state GET and structural evidence parsing. |
| 1.7 | 2026-08-28 | Approved Baseline | Jack Spaetjens | Updated the current pre-release implementation status through reused-child relationship-state classification. |
| 1.8 | 2026-08-28 | Approved Baseline | Jack Spaetjens | Updated current pre-release status after the missing-parent recovery ownership governance correction. |
| 1.9 | 2026-08-28 | Approved Baseline | Jack Spaetjens | Updated current pre-release implementation status through MISSING missing-parent recovery coordination. |
| 1.10 | 2026-08-29 | Approved Baseline | Jack Spaetjens | Updated current pre-release implementation status through reused-child descendant gating. |
| 1.11 | 2026-08-29 | Approved Baseline | Jack Spaetjens | Updated current pre-release implementation status through complete non-root Parent-Child Relationship lifecycle coordination. |
| 1.12 | 2026-08-29 | Approved Baseline | Jack Spaetjens | Synchronized implemented root existing/new Work Item lifecycle coordination status. |
| 1.13 | 2026-08-29 | Approved Baseline | Jack Spaetjens | Synchronized implemented full preflight coordination status while retaining incomplete release readiness. |
| 1.14 | 2026-08-30 | Approved Baseline | Jack Spaetjens | Synchronized implemented deterministic hierarchy traversal while retaining final Generator entry composition before Review Gate 2. |
| 1.15 | 2026-08-30 | Approved Baseline | Jack Spaetjens | Synchronized complete Generator Orchestration implementation and coverage status. |
| 1.16 | 2026-08-30 | Approved Baseline | Jack Spaetjens | Recorded Generator Orchestration Review Gate 2 PASS with no required remediation. |
| 1.17 | 2026-08-31 | Approved Baseline | Jack Spaetjens | Synchronized implemented Application/Run Slice 1 status while retaining incomplete release readiness. |
| 1.18 | 2026-08-31 | Approved Baseline | Jack Spaetjens | Synchronized implemented Application/Run Slice 2 status while retaining incomplete release readiness. |
| 1.19 | 2026-09-02 | Approved Baseline | Jack Spaetjens | Synchronized implemented Application/Run Slice 3 Process Bootstrap Invocation status while retaining incomplete release readiness. |
| 1.20 | 2026-09-02 | Approved Baseline | Jack Spaetjens | Synchronized implemented Application/Run Slice 4 Controlled Application Outcome Mapping status while retaining incomplete release readiness. |
| 1.21 | 2026-09-03 | Approved Baseline | Jack Spaetjens | Recorded approved but unimplemented Application/Run Slice 5 Controlled Failure Reporting to Standard Error. |
| 1.22 | 2026-09-03 | Approved Baseline | Jack Spaetjens | Synchronized implemented Application/Run Slice 5 Controlled Failure Reporting to Standard Error status. |
| 1.23 | 2026-09-04 | Approved Baseline | Jack Spaetjens | Defined the approved but unimplemented Application/Run Slice 6 Runtime File Logging and Controlled-Failure Events contract. |
| 1.24 | 2026-09-04 | Approved Baseline | Jack Spaetjens | Synchronized implemented Application/Run Slice 6 Runtime File Logging and Controlled-Failure Events status. |
| 1.25 | 2026-09-06 | Approved Baseline | Jack Spaetjens | Recorded the approved but unimplemented Application/Run Slice 7 package execution adapter and interim pre-release limitations. |
| 1.26 | 2026-09-06 | Approved Baseline | Jack Spaetjens | Synchronized implemented Application/Run Slice 7 executable outcomes and pre-release limitations. |
| 1.27 | 2026-09-06 | Approved Baseline | Jack Spaetjens | Recorded the approved but unimplemented Application/Run Slice 8 lifecycle logging contract and pre-release exclusions. |
| 1.28 | 2026-09-08 | Approved Baseline | Jack Spaetjens | Synchronized implemented Application/Run Slice 8 lifecycle logging status and remaining pre-release limitations. |
| 1.29 | 2026-09-11 | Approved Baseline | Jack Spaetjens | Recorded the owner-approved but unimplemented final unexpected-error handling and diagnostic-safety contract and remaining pre-release limitations. |
| 1.30 | 2026-09-11 | Approved Baseline | Jack Spaetjens | Allocated the approved but unimplemented Final Unexpected-Error Handling and Diagnostic Safety capability as Application/Run Slice 9. |
| 1.31 | 2026-09-11 | Approved Baseline | Jack Spaetjens | Synchronized implemented Application/Run Slice 9 status and remaining pre-release limitations. |
| 1.32 | 2026-09-12 | Approved Baseline | Jack Spaetjens | Proposed Review Gate 3 acceptance matrix, owner decisions, PASS and deferral rules and Gate-4 boundary. |
| 1.33 | 2026-09-12 | Draft | Jack Spaetjens | Recorded approved execution-summary decisions with implementation and validation pending; Gate 3 remains not passed. |

---

# Table of Contents

- [Azure DevOps Backlog Generator](#azure-devops-backlog-generator)
- [Release Management](#release-management)
- [Version History](#version-history)
- [Table of Contents](#table-of-contents)
- [1. Introduction](#1-introduction)
- [2. Purpose](#2-purpose)
- [3. Release Objectives](#3-release-objectives)
- [4. Release Principles](#4-release-principles)
- [5. Current Release Status](#5-current-release-status)
- [6. Versioning Strategy](#6-versioning-strategy)
- [7. Release Types](#7-release-types)
  - [Major Release](#major-release)
  - [Minor Release](#minor-release)
  - [Patch Release](#patch-release)
- [8. Release Criteria](#8-release-criteria)
  - [8.1 Review Gate 3 Operational Readiness Acceptance](#81-review-gate-3-operational-readiness-acceptance)
- [9. Release Preparation](#9-release-preparation)
- [10. Release Approval](#10-release-approval)
- [11. Post-Release Activities](#11-post-release-activities)
- [12. Traceability](#12-traceability)
- [13. Approval](#13-approval)


---

# 1. Introduction

This document defines the release management strategy for Version 1.0 of the Azure DevOps Backlog Generator.

It establishes the governance, approval process and release activities required to deliver controlled software releases while maintaining alignment with the approved documentation baseline.

---

# 2. Purpose

The purpose of this document is to define a consistent release management process.

The Release Management document establishes the framework for planning, approving, publishing and maintaining software releases throughout the project lifecycle.

---

# 3. Release Objectives

Version 1.0 shall achieve the following release objectives:

- Deliver approved functionality in a controlled manner.
- Maintain complete traceability between documentation and released software.
- Ensure release quality through approved validation activities.
- Support repeatable release processes.
- Maintain consistent versioning throughout the project lifecycle.

---

# 4. Release Principles

Release management shall follow the following principles:

- Documentation-driven releases.
- Approved documentation baseline before release.
- Successful validation before approval.
- Controlled version management.
- Traceable release history.
- Repeatable release procedures.
- Configuration consistency.
- Continuous improvement through release feedback.

---

# 5. Current Release Status

Version 1.0 has not been approved or published and remains pre-release. The project is in
implementation: its configuration, documentation-processing, source-identity, REST foundation,
compatibility, candidate, JSON Patch, validation-only Create, WIQL identity lookup, Work Item GET
evidence retrieval, existing/new Work Item resolution, Persistent Work Item Create REST transport,
complete non-root Parent-Child Relationship lifecycle coordination, root existing/new Work Item
lifecycle coordination and deterministic hierarchy traversal are complete. Full preflight validates
every exact candidate and returns at the mutation barrier; traversal then reuses the retained candidates,
processes documents and hierarchy items in deterministic parent-before-child order, and composes root
and non-root lifecycle operations with global fail-fast across roots and documents. Rerun safety relies
on source identity and fresh reused-child relationship inspection, including MISSING recovery and
CORRECT or CONFLICTING handling. The final Generator-owned coordinator is implemented: it composes
full preflight through the successful mutation barrier into deterministic hierarchy traversal. Generator
Orchestration implementation and currently approved pre-Review-Gate-2 coverage are complete, including
malformed-response and HTTP `401`/`403` full-orchestration global-stop evidence. Review Gate 2 completed
with PASS, zero findings and no required remediation. Application/Run Slice 1 is implemented: it composes
an already-loaded and validated `Configuration` into documentation processing, one REST-client construction
and one Generator invocation, then returns `None`; collaborator failures propagate unchanged without retry
or fallback. Application/Run Slice 2 is implemented: the callable application chain supports arguments
through configuration selection, loading, validation and PAT acquisition into Slice 1 and the Generator.
Application/Run Slice 3 is implemented: `main() -> None` composes process `sys.argv` through `sys.argv[1:]`
to Slice 2, Slice 1 and the Generator, returning `None` on success and propagating bootstrap exceptions
unchanged. Application/Run Slice 4 is implemented: `run_process() -> int` invokes `main()` exactly once,
returns the exact integer `0` on successful completion, returns the exact integer `1` for the approved
controlled failure set without re-raising it, and originally propagated unexpected exceptions unchanged. Slice 4 adds no
retry, fallback, stdout/stderr output, reporting, logging, `SystemExit`, executable adapter, direct execution
or packaging. Application/Run Slice 5 — Controlled Failure Reporting to Standard Error is implemented. The
existing `run_process() -> int` retains controlled classification and, on a caught controlled failure, calls the
private `_render_controlled_failure(error)`, writes exactly one fixed category-only stderr message and newline, and
returns the existing exact integer `1`, with stdout empty and no re-raise. The renderer exposes no exception detail,
including `str(exception)`, `repr(exception)`, exception arguments, paths, source-derived content, Azure DevOps
URLs, response bodies, headers, PAT values, Authorization values or arbitrary exception messages; focused tests
prove synthetic sensitive-looking detail absent from stderr. Successful `run_process()` execution remains silent and
returns `0`; Slice 5 originally preserved unexpected propagation without generic reporting. Implemented Slice 9 now supplies that fallback. The
wider Application/Run phase is not yet complete. Application/Run Slice 6 — Runtime File Logging and Controlled-Failure
Events is implemented. Runtime controlled-failure file logging now uses one configured application-owned UTF-8 append handler and one
safe category-only `CRITICAL` emission attempt per eligible controlled failure; a record is written exactly once when
that attempt succeeds, while a secondary write failure preserves the primary controlled failure. It permits no
root/console/fallback logging and adds an `ApplicationLoggingError` controlled category only when initialisation
fails. Version 1.0 remains pre-release. The following Slice-7 status records the implemented executable
boundary while retaining incomplete wider Application/Run and release readiness.

Application/Run Slice 7 — Package Execution Adapter with Controlled Process Termination is implemented
in PR #136 (implementation commit `468d98d`, merge `009ef71`), following contract PR #134 and approval PR #135.
S7-D1/S7-D2 remain approved owner decisions. Slices 1–9 are implemented. The sole implemented executable
surface is `python -m azure_devops_backlog_generator` through
`src/azure_devops_backlog_generator/__main__.py`, with exactly one call to `run_process()` and direct
use of its unchanged integer as the `SystemExit` code. The executable adapter exclusively owns
`SystemExit`. Controlled success maps `0` to OS status `0` with empty stdout/stderr; controlled failure
maps `1` to OS status `1` with empty stdout and the existing exact stderr owned by `run_process()`,
without adapter traceback or duplicate output. Import safety is implemented for both the package and
`__main__`; ordinary import does not start the application or emit adapter output or logging.
Runtime logging, D1–D5, all seven controlled categories and existing application/core return contracts
remain unchanged. No console script, `[project.scripts]`, `main.py` execution guard, packaging metadata,
dependency, package-version or README invocation change was introduced.

If `run_process()` itself raises, the adapter still propagates the exact same exception object without
classification, translation, sanitisation or output. Implemented Slice 9 now handles otherwise-unclassified
application `Exception` instances inside `run_process()`, yielding fixed stderr and result `1` without
native traceback on the supported package path. This resolves that path's previous traceback limitation;
direct lower-level propagation and arbitrary Python invocation paths remain separate.

Version 1.0 remains pre-release; wider Application/Run and release readiness remain incomplete. Remaining
broader logging and HTTP/API reporting reconciliation/contract work, execution-summary content and
presentation remain future. Typed execution-result/aggregation and created/reused/repaired counts are conditional on later summary requirements.
Broader integration/E2E, live Azure DevOps Services validation, Operational Readiness
and Review Gate 3 remain future. Console-script packaging requires separate approval; GUI implementation
remains future and outside Version 1.0. The known pre-existing non-blocking `05-API.md` Section 6.1 broad
deferred Application/Run status conflicts with the more specific current documents showing Slices 1–9
implemented. Reconciliation remains required before Gate 3 and is not a Slice-9 implementation blocker.
The API Specification and REST semantics remain unchanged by this status sync.

The package adapter now supplies a real executable surface and controlled OS statuses `0`/`1`.
Testing Section 8 records the implementation evidence, including the real package configuration-failure
subprocess and isolated successful/unexpected adapter-boundary subprocesses. Success-boundary validation
does not establish successful application E2E. The existing release criteria remain unchanged; production
readiness, Gate 3 completion and final Version 1.0 approval are not claimed.

Application/Run Slice 8 — Process-Neutral Application Lifecycle File Logging is **IMPLEMENTED**
in PR #141 (implementation commit `378e2b1`, merge `8560a89`), following contract PR #139 and approval
PR #140. Architecture Section 7.1.8 defines implemented, approved owner decisions S8-D1–D3. The
Slice-8 status-sync revision 1.28 is Approved Baseline; revision 1.31 is Approved Baseline.

Slice 8 adds only two process-neutral INFO file lifecycle messages: `Application run started.`
after successful configuration validation/logging initialisation and immediately before configured
execution, and `Application run completed successfully.` only after normal application return.
Normal configured threshold filtering and current-owned-handler-only isolation apply. Writes are
best effort, with no retry, fallback, additional output or outcome change; `ApplicationLoggingError`
remains initialisation-only. Completion is not an execution summary or evidence of item counts.

Slices 1–9 are implemented; the Slice-8 contract remains approved. D1–D5, all seven controlled categories, controlled
CRITICAL reporting and the sole package surface `python -m azure_devops_backlog_generator` remain
unchanged. `__main__.py` exclusively owns SystemExit; `run_process()`, `main()` and application/core
return contracts remain unchanged. No Generator, REST, configuration, CLI, dependency, result-model,
counter or summary change is included. Successful stdout/stderr stay empty; controlled failures retain
existing exact stderr. Unexpected exceptions retain identical propagation through direct lower-level
calls; Slice 9 now provides the fixed process-facing report and bounded native traceback suppression.
The Slice-8 fixed lifecycle messages and their safety contract remain unchanged.

Version 1.0 remains pre-release and wider Application/Run remains incomplete. Slice 8 covers only
configured-run START and successful COMPLETION; existing controlled-failure logging remains Slice 6
and other logging topics remain future where not already implemented. It does not complete execution
summary, broader integration/E2E, live Azure
validation, Operational Readiness checklist/evidence, Review Gate 3 or
release readiness. The preceding Approved Baseline did not contain a complete normative Gate-3
acceptance checklist; Section 8.1 of this revision defines the Gate-3 acceptance framework.
Gate 3 remains FUTURE / NOT YET PASSED. Lifecycle observations contribute operational execution
evidence without establishing Gate-3 prerequisites.
Owner-approved G3-D3 places broader Operational Recovery / DR outside V1.0; Generator later-run
recovery remains unchanged and is not equivalent to Operational Recovery / DR.

API Section 6.1 drift remains separate future documentation reconciliation required before Review
Gate 3; the API Specification is unchanged. Testing Section 8 records merged Slice-8 evidence:
55/55 focused tests, 743/743 full pytest and 743/743 warnings-as-errors pytest, Ruff passed and 95%
coverage across 1,381 statements with 64 missed. No live Azure DevOps validation was performed or new
subprocess tests added; existing Slice-7 package/subprocess coverage passed. Future GUI/alternate-adapter
reuse remains possible through presentation-neutral application/core behaviour; GUI remains outside
Version 1.0.

---

**Application/Run Slice 9 — Final Unexpected-Error Handling and Diagnostic Safety — IMPLEMENTED — APPROVED CONTRACT.**
Architecture's
[Application/Run Slice 9 — Final Unexpected-Error Handling and Diagnostic Safety](02-Architecture.md#applicationrun-slice-9--final-unexpected-error-handling-and-diagnostic-safety)
section defines authoritative owner-approved decisions UE-D1–UE-D10. Those decisions remain approved
and are implemented. Release revision 1.31 is Approved Baseline.
Slices 1–9 are implemented. No Slice 10 has been allocated; future capability ordering beyond Slice 9
remains undefined.

Implementation provenance is PR #148 (commit `738fdc3`, merge `4549eee`). Contract provenance remains
PR #144 (commit `2070425`, merge `4d80b58`) and approval PR #145 (commit `e3e190f`, merge `fa158d9`);
allocation remains PR #146 (commit `720bb68`, merge `e332c69`) and allocation approval PR #147
(commit `1174bcb`, merge `ea37478`). Production changes are confined to
`src/azure_devops_backlog_generator/main.py`; validation is in `tests/test_main.py` and
`tests/test___main__.py`. Production `__main__.py` remains unchanged.

The implementation supplies the otherwise-unclassified `Exception` fallback only at `run_process()`, after
the existing seven controlled categories, with integer result `1`, exactly `Unexpected application error.`
plus newline on stderr, empty stdout and one best-effort fixed CRITICAL logfile attempt only when the
current invocation's owned runtime logger is already active. The supported handled-Exception package
path suppresses native traceback output and dynamic exception diagnostics. The fixed category
message is the approved operational diagnostic for this bounded fallback; no redaction or richer
diagnostic feature is approved. Direct lower-level propagation, process-control exceptions outside
`Exception`, existing stderr-delivery behaviour and `__main__.py` SystemExit ownership remain preserved.

Testing Section 8 records merged Slice-9 evidence: 84/84 combined focused tests (73 in
`tests/test_main.py`, 11 in `tests/test___main__.py`), Ruff passed, 764/764 full pytest and
764/764 `pytest -W error`, each full run with zero failed, skipped, warnings, xfail or xpass.
Coverage is 95% across 1,394 statements with 64 missed; `main.py` is 110/0/100% and `__main__.py`
is 3/0/100%. No live Azure DevOps operations occurred; Ruff and pytest were not rerun for this status sync.

The previous native-traceback limitation is resolved for the supported handled-Exception
`run_process()`/package path. Direct lower-level callers still receive propagated exceptions;
no generic redaction framework exists. This implemented bounded safety does not establish Operational
Readiness, integration/E2E completion, live Azure validation, Gate-3 completion, Gate-4 completion or RC readiness.

Version 1.0 remains pre-release and wider Application/Run remains incomplete. Gates 1 and 2 remain
PASS; Gates 3 and 4 remain future. Broader Architecture Section-12 logging and unresolved HTTP/API
reporting remain separate capability work. Architecture Section 13.4 records owner-approved
G3-SUM-D1 to G3-SUM-D9; execution-summary implementation and validation remain pending. No result DTO
is approved. API Section 6.1 implementation status is reconciled in this Draft; separate HTTP
reporting decisions remain unresolved.
Broader integration/E2E, live Azure DevOps Services validation, Operational Readiness definition/evidence,
and final release approval remain outstanding. Section 8.1 records the Draft Gate-3 framework and
resolved placement decisions; broader Operational Recovery / DR is outside V1.0 under G3-D3.
Existing release criteria are unchanged.

---

# 6. Versioning Strategy

Version 1.0 shall follow a consistent versioning strategy throughout the project lifecycle.

The project shall use Semantic Versioning in the format:

**MAJOR.MINOR.PATCH**

Version numbering shall follow these principles:

- **MAJOR** versions represent significant or incompatible changes.
- **MINOR** versions represent new functionality while maintaining backward compatibility.
- **PATCH** versions represent defect corrections that do not introduce new functionality.

All released versions shall be recorded through Version History and Git tags where applicable.

---

# 7. Release Types

The project shall support the following release types.

## Major Release

A major release introduces significant functional enhancements or incompatible changes.

Example:

- Version 2.0.0

---

## Minor Release

A minor release introduces approved functionality while maintaining backward compatibility.

Example:

- Version 1.1.0

---

## Patch Release

A patch release resolves defects without introducing new functionality.

Example:

- Version 1.0.1

Patch releases shall remain fully compatible with the corresponding major and minor release.

---

# 8. Release Criteria

A software release shall not be approved until the following criteria have been satisfied:

- Approved documentation baseline.
- Successful completion of planned testing.
- No unresolved critical defects.
- Successful validation of Azure DevOps functionality.
- Successful code review.
- Approved Version History updates.
- Successful repository commit.

Only approved releases shall be published.

---

## 8.1 Review Gate 3 Operational Readiness Acceptance

**Gate 3 is FUTURE / NOT YET PASSED and currently NOT READY.**
This Draft records approved summary decisions within the approved Gate-3 framework.
Gate 3 answers: "Is the application operationally complete and sufficiently evidenced to enter final
release-candidate validation?" Gate 4 remains the Release Candidate / final pre-release gate. Neither
approval of this contract nor a later Gate-3 PASS constitutes RC acceptance or final Version-1.0 approval.

Existing normative requirements are identified in the matrix's source column. The gate framework,
including its assignments and PASS rule, forms part of the approved starting baseline at main `cff3397`.
G3-D1 to G3-D3 remain RESOLVED / OWNER APPROVED on 2026-09-12 and settle placement/applicability.
This Draft records the separately owner-approved summary contract in Architecture Section 13.4;
summary implementation and validation remain pending, and no Gate-3 PASS is implied.

[Architecture Section 13](02-Architecture.md#13-review-gate-3-operational-readiness-boundaries) defines
operational boundaries and logging/reporting dependencies; [Testing Section 9.1](06-Testing.md#91-review-gate-3-evidence-requirements)
defines evidence. [Roadmap Section 5.1](03-Roadmap.md#51-review-gate-3-next-governance-milestone) records
the governance milestone. Existing implementation evidence below was recorded at `751c928`; source
and tests remain unchanged at starting baseline `cff3397`. Row F now records approved summary
behaviour with implementation and validation pending; writing this Draft produces no execution evidence.

### Status and closure model

SATISFIED means the stated condition is supported by applicable recorded evidence. PARTIALLY SATISFIED
means some required behaviour/evidence exists but closure remains. NOT SATISFIED means required closure
is absent. DECISION REQUIRED means an owner decision prevents a settled acceptance condition. Contract
approval alone does not change an implementation or validation status to SATISFIED.

Closure types identify remaining work: IMPLEMENTATION, CONTRACT, DOCUMENTATION, VALIDATION,
OWNER DECISION and GOVERNANCE. A dash means no additional closure work currently identified for that row;
its evidence must still be checked for applicability at gate review. G3-D1 to G3-D3 are resolved;
remaining behavioural decisions shall be closed through their separate contracts. Any permitted
remaining release-scenario allocation must be explicit under the deferral rule.

### Proposed acceptance matrix

| Area | Normative source | Gate-3 acceptance condition | Required evidence | Current status | Closure type |
|------|------------------|-----------------------------|-------------------|----------------|--------------|
| A. Contract/documentation consistency | Development Sections 8-10; Release Section 5 pre-Gate-3 API prerequisite | Required behavioural/gate documents are Approved Baseline and consistent; API Section 6.1 status drift is reconciled; summary/completion and severity wording cannot undermine acceptance. | Approved revisions and reconciliation record linked to affected requirements. | NOT SATISFIED | CONTRACT, DOCUMENTATION, GOVERNANCE |
| B. Operational implementation completeness | PRD FR-001 to FR-010; Architecture Sections 7-13 | Existing approved core and Slices 1-9 remain implemented; all additional operational behaviours assigned by this gate and resolved decisions are implemented and merged. | Implementation/review references and requirement-to-test coverage, including D-F. | PARTIALLY SATISFIED | CONTRACT, IMPLEMENTATION, VALIDATION |
| C. Runtime/configuration | Architecture Sections 7.1.1-7.1.7 and Slice 9; Configuration Sections 5-8 | Supported package invocation, default/explicit configuration, PAT acquisition, outcomes and termination ownership retain their approved contracts. | Existing configuration, application and package/subprocess evidence; integrated success is separately required by G. | SATISFIED | - |
| D. Observability/logging | PRD FR-009; Architecture Sections 12 and 13.1; Configuration Section 6.4 | All applicable logging topics have approved minimum interpretations and validated implementation; summary placement follows F. | Event acceptance mapping, tests for content/timing/levels/delivery and applicable operational records. | PARTIALLY SATISFIED | CONTRACT, OWNER DECISION, IMPLEMENTATION, VALIDATION |
| E. HTTP/API reporting | API Sections 6.1, 6.2 and 9-11; Architecture Section 13.2 | Approved reconciliation of 401/403 reporting, rate-limit logging and current generic presentation is implemented and evidenced; status preservation and no retry remain. | Reconciled behavioural baseline and status-specific reporting/safety/global-stop tests. | PARTIALLY SATISFIED | CONTRACT, OWNER DECISION, IMPLEMENTATION, VALIDATION |
| F. Execution summary | Architecture Sections 8, 12 and 13.4; API Section 7.1; owner-approved G3-D1 and G3-SUM-D1 to G3-SUM-D9 | The V1.0 summary is fully contract-defined, implemented, validated and evidenced before Gate-3 PASS; unfinished functionality cannot be deferred to Gate 4. | Owner-approved behaviour in Architecture Section 13.4; merged implementation and Testing Section 9.2 validation evidence remain required. | NOT SATISFIED: behavioural decisions approved; implementation and validation pending. | IMPLEMENTATION, VALIDATION, DOCUMENTATION |
| G. Integration/system validation | Testing Sections 5 and 9 | Complete successful application-level execution and integrated failure/rerun evidence meet Testing Section 9.1; adapter-only success is insufficient. | Traceable application integration results with real configuration/parser/Generator and declared transport boundary. | PARTIALLY SATISFIED | VALIDATION, IMPLEMENTATION |
| H. Azure DevOps Services validation | Testing Sections 6 and 9; Release Sections 8 and 10; owner-approved G3-D2 | Complete the minimum real Services operational proof in Testing Section 9.1 before Gate-3 PASS; mock-only evidence is insufficient. | Prepared controlled procedure/environment and executed live records; final RC repetition and explicitly assigned remaining scenarios retained for Gate 4. | NOT SATISFIED | VALIDATION, GOVERNANCE, DOCUMENTATION |
| I. Security/secret safety | PRD NFR-005; Architecture Section 10 and Slice 9; API Sections 5-6.2; Configuration Section 8 | Existing credential/transport/reporting protections remain; newly approved output and live evidence expose no credentials or prohibited diagnostics. | Existing safety tests plus new behaviour and live-procedure safety evidence. | PARTIALLY SATISFIED | VALIDATION |
| J. Failure/rerun behaviour | PRD FR-007/FR-010; Architecture Sections 7.4 and 11; API Sections 8.5 and 10 | Preserve mutation barrier, global stop, accepted partial state and bounded later-run repair; prohibit automatic retry/rollback/compensation. | Existing Generator evidence plus application-path traceability and required integration results. | PARTIALLY SATISFIED | VALIDATION |
| K. Operational Recovery / DR applicability | Owner-approved G3-D3; Architecture Section 13.3 | Broader Operational Recovery / DR is OUTSIDE V1.0, not deferred to Gate 4; existing bounded failure/rerun and operator-guidance obligations remain under J and L. | G3-D3 owner scope decision recorded below on 2026-09-12. | SATISFIED | - |
| L. User/operator documentation | Architecture Section 7.1.7; Configuration Sections 5-8; proposed documentation assignment | Reviewed runtime guidance covers `python -m azure_devops_backlog_generator`, a `--config-file` example, default/config-relative paths, AZDO_PAT-only sourcing, 0/1 outcomes, logfile location/levels, no dry-run and bounded failure/rerun behaviour. | README or clearly linked operator guidance checked against implementation and approved contracts; secrets excluded. | NOT SATISFIED | DOCUMENTATION, VALIDATION |
| M. Defects/findings | Testing Section 9; proposed Gate-3 adoption | No unresolved critical/high defects or findings; remaining findings cannot prevent mandatory row satisfaction. | Assessed-revision findings register, severity/disposition and verified closure evidence. | NOT SATISFIED | GOVERNANCE, VALIDATION |
| N. Evidence traceability | PRD NFR-006; Testing Sections 8-11; Release Section 12 | Every row has the versioned source, assessed revision, evidence scope/result and disposition required by Testing Section 9.1. | Complete indexed evidence record; recorded baseline results credited only within their proven scope. | PARTIALLY SATISFIED | DOCUMENTATION, VALIDATION, GOVERNANCE |
| O. Approval/sign-off | Release Sections 8-10 and 13; AI Working Agreement Section 13 | Owner explicitly records Gate-3 PASS only after the PASS rule is met. | Dated owner acceptance referring to the completed matrix, evidence and approved decision records. | NOT SATISFIED | GOVERNANCE |

IMPLEMENTATION in G means additional automated integration coverage where needed, not a prescribed
production feature. F requires a separate behavioural contract before implementation. K is SATISFIED
only for the owner-approved exclusion of broader DR from V1.0, not completion of failure/rerun evidence
or operator guidance; those remain under J and L. Existing Gate-1/2 PASS records do not establish M or O
for the current operational gate. Runtime documentation can be completed separately; README is not edited here.

### Owner decision register

Owner decisions below were explicitly approved on 2026-09-12. They resolve gate placement and
scope only. The framework is part of the approved starting baseline; this summary-contract revision
remains Draft.

| Decision | Status | Owner-approved decision | Remaining boundary |
|----------|--------|-------------------------|--------------------|
| G3-D1 - Summary placement | RESOLVED / OWNER APPROVED | The summary shall be fully contract-defined, implemented, validated and evidenced before Gate-3 PASS. It shall not be deferred as unfinished runtime functionality; Gate 4 may repeat/verify it in final RC regression. | G3-SUM-D1 to G3-SUM-D9 are owner-approved and recorded in Architecture Section 13.4: one processed-source-item count, two prospective integer-return changes and success-only INFO summary delivery. Implementation and validation remain pending; no result DTO is approved. |
| G3-D2 - Live validation placement | RESOLVED / OWNER APPROVED | Minimum real Azure DevOps Services operational proof is required before Gate-3 PASS; mock-only evidence is insufficient. Final RC repetition and explicitly assigned remaining release scenarios remain at Gate 4. | Exact isolated project configuration, permissions, cleanup authorisation and controlled procedure still need definition. A repeatable manual procedure with recorded evidence is acceptable; no dedicated automated live harness is mandated. |
| G3-D3 - Recovery/DR applicability | RESOLVED / OWNER APPROVED | Broader Operational Recovery / Disaster Recovery is OUTSIDE V1.0, not deferred to Gate 4. No new backup/restore or DR infrastructure, automatic retry/rollback/compensation, generic recovery subsystem, logfile recovery/rotation or dedicated DR platform/service is required. | Existing global fail-fast, legitimate partial state, later-run identity rediscovery/reuse and fresh MISSING repair, CORRECT continuation and CONFLICTING stop remain. Bounded operator guidance remains required under L; failure/rerun evidence remains under J. |

Separate behavioural owner decisions remain for unresolved logging interpretations in Architecture
Section 13.1 and HTTP reporting channels/messages/event interaction. G3-SUM-D1 to G3-SUM-D9 settle
summary behaviour only, including one processed-source-item count and two prospective return changes;
they do not resolve other logging or HTTP decisions. Architecture Section 13.4 owns that contract and
Testing Section 9.2 owns prospective validation. No result DTO, new exception taxonomy, configuration
or implementation slice is introduced. Summary approval does not satisfy row F or establish Gate-3 PASS.

### Entry, PASS and NOT-READY rules

Preparation and contract review may proceed while the gate is NOT READY. Formal acceptance review shall
use an identified merged implementation revision, approved gate/behavioural documentation, the complete
matrix/evidence record and owner-approved G3-D1 to G3-D3. Remaining behavioural decisions require
separate contract closure. Gates 1 and 2 remain recorded PASS.

Gate 3 may PASS only when:

1. Every mandatory row A-N is SATISFIED against the approved acceptance conditions; no DECISION REQUIRED,
   PARTIALLY SATISFIED or NOT SATISFIED prerequisite remains.
2. All Gate-3-assigned runtime implementation, including the complete execution summary and required
   logging/reporting, and automated coverage are merged; required governing documentation is
   Approved Baseline and required operator guidance is complete, reviewed and available.
3. Required integration, summary and minimum real Services operational validation under G3-D2 are
   executed, recorded and applicable to the assessed revision; evidence traceability is complete.
   Planned procedures and this contract text are not execution evidence.
4. No unresolved critical/high defect or finding remains, consistent with Testing Section 9. Other
   findings have explicit permitted dispositions and do not prevent mandatory row satisfaction.
5. Jack Spaetjens, as final decision authority, records explicit Gate-3 approval against that evidence;
   this completes row O as SATISFIED. Contract approval is a separate earlier decision.

Gate 3 remains NOT READY if any prerequisite above is unmet, evidence is missing/inapplicable, a required
contract is unapproved or contradictory, a remaining behavioural decision is unresolved, a prohibited-severity finding remains,
or owner sign-off is absent. Gate 3 remains FUTURE / NOT YET PASSED in this Draft; no PASS is claimed.

### Deferral rule and Gate-4 boundary

Deferral is permitted only for explicitly allocated remaining release-validation scenarios beyond the
mandatory Gate-3 minimum and the final RC/release activities below. The execution-summary capability
and minimum real Services operational proof shall not be deferred beyond Gate 3. Gate 4 may repeat
summary validation as final regression but shall not receive unfinished summary functionality. Broader
Operational Recovery / DR is outside V1.0 under G3-D3, not a Gate-4 deferral. A deferral record shall name the
requirement/deliverable, rationale, receiving Gate-4 owner, acceptance evidence and required completion
before RC acceptance. It shall show that no existing V1.0 requirement due before operational readiness
is contradicted. The owner shall approve the allocation; unresolved requirements cannot simply be marked
SATISFIED. Other gate-scope changes require a new approved contract revision. API Section 6.1 status
reconciliation, required reconciled HTTP reporting, mandatory integrated application evidence and the
critical/high threshold cannot be silently deferred. V1.0 requirements cannot be waived by relabelling
them as post-release work. No informal or silent deferral is permitted.

Gate 4 retains final regression evidence against the RC revision, final live-validation repetition
and explicitly assigned remaining release scenarios, release artefact/documentation finalisation,
final finding disposition, RC acceptance and final owner release approval under Sections 8-10. A later
Gate-3 PASS permits entry to that final validation; it does not approve publication. This boundary is not
a complete Gate-4 contract and does not approve an RC or allocate future Application/Run slices.

The Gate-3 record shall be referenced from a subsequent approved Release status update and identify the
assessed commit, governing document revisions, completed A-O matrix, Testing Section 9.1 evidence index,
G3-D1 to G3-D3 decisions, findings/deferrals, reviewer and dated owner decision. Signing off cannot replace
missing evidence or amend requirements implicitly. Current Gate-1/2 PASS, Gate-4 FUTURE and Version-1.0
PRE-RELEASE status remain unchanged. No Slice 10 has been allocated.

Release Sections 8 and 10 currently name critical defects while Testing Section 9 also names high-severity
defects. The proposed Gate-3 threshold explicitly uses the stricter existing Testing criterion. The broader
wording alignment remains documentation follow-up and shall not be interpreted as permission to relax
Testing acceptance. This task does not change the final release criteria or perform API/README reconciliation.

---

# 9. Release Preparation

Release preparation shall include:

- Verification of the approved documentation baseline.
- Confirmation of the software version.
- Validation of Version History.
- Execution of automated testing.
- Verification of release notes where applicable.
- Review of repository status.
- Confirmation of release readiness.

Release preparation shall be completed before release approval is requested.

---

# 10. Release Approval

A release shall be approved only after all release criteria have been satisfied.

Release approval shall confirm that:

- All approved functional requirements have been implemented.
- The approved documentation baseline has been completed.
- All planned testing activities have been successfully completed.
- No unresolved critical defects remain.
- Version History has been updated.
- The release is ready for publication.

Only approved releases shall be published.

---

# 11. Post-Release Activities

Following publication of a release, the following activities shall be completed:

- Verify successful publication.
- Verify repository integrity.
- Confirm release version tagging where applicable.
- Archive release documentation.
- Record release information in Version History.
- Review lessons learned for future releases.

Post-release activities shall ensure the integrity and traceability of released software.

---

# 12. Traceability

This Release Management document defines the governance activities supporting delivery of the approved documentation baseline.

Traceability shall be maintained between:

- Product Requirements Document
- Software Architecture Document
- Development Roadmap
- Development Standards
- API Specification
- Testing Strategy
- Release Management
- Azure DevOps Backlog
- Source Code
- Test Documentation

Release activities shall remain aligned with the approved documentation baseline and shall not introduce functionality that is not traceable to an approved requirement.

---

# 13. Approval

This document becomes part of the approved documentation baseline following:

- Completion of the editorial review.
- Approval of Version 1.0.
- Creation of the Version 1.0 Approved Baseline.
- Commit to the project repository using the agreed Git workflow.

Subsequent modifications shall follow the established documentation governance process and be recorded through Version History.
