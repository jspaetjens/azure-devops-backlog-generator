# Azure DevOps Backlog Generator

# Release Management

> *This document defines the release management process, versioning strategy and deployment governance for Version 1.0 of the Azure DevOps Backlog Generator.*

**Version:** 1.21

**Status:** Approved Baseline

**Last Updated:** 2026-09-03

**Target Release:** v1.0.0

**License:** MIT

**Author:** Jack Spaetjens

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
controlled failure set without re-raising it, and propagates an unexpected exception unchanged. It adds no
retry, fallback, stdout/stderr output, reporting, logging, `SystemExit`, executable adapter, direct execution
or packaging. Application/Run Slice 5 — Controlled Failure Reporting to Standard Error is approved for
implementation but is not implemented. It shall add only category-only stderr reporting for the existing controlled
set: exactly one fixed message and newline, no stdout and existing return `1`; successful `run_process()` execution
shall remain silent and return `0`. No exception detail may be rendered. The wider Application/Run phase is not yet
complete. Version 1.0 remains pre-release: runtime logging initialisation and failure logging, execution summary,
unexpected-exception handling, traceback diagnostics, an executable process/CLI adapter, `SystemExit` ownership,
`__main__.py` and/or console-script packaging if later approved, integration/end-to-end validation, Operational
Readiness, Operational Recovery / DR, Review Gate 3 and final release-readiness work remain incomplete. The release
criteria in this document remain unchanged.

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
