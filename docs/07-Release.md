# Azure DevOps Backlog Generator

# Release Management

> *This document defines the release management process, versioning strategy and deployment governance for Version 1.0 of the Azure DevOps Backlog Generator.*

**Version:** 1.9

**Status:** Approved Baseline

**Last Updated:** 2026-08-28

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

Version 1.0 has not been approved or published. The project is in implementation: its
configuration, documentation-processing, source-identity, REST foundation, compatibility,
candidate, JSON Patch, validation-only Create, WIQL identity lookup, Work Item GET evidence
retrieval, existing/new Work Item resolution, Persistent Work Item Create REST transport,
Parent-Child Relationship JSON Patch construction, Parent-Child Relationship HTTP PATCH
transport, reused-child relationship-state GET with structural relationship evidence validation
and reverse-parent target-ID extraction, generator-level intended-parent comparison with MISSING,
CORRECT and CONFLICTING classification, and MISSING missing-parent recovery coordination using
the existing Parent-Child Relationship PATCH with the fresh relationship-state revision are complete,
while generator/application lifecycle coordination for persistent Create, CORRECT continuation,
CONFLICTING lifecycle handling, descendant gating, persistent relationship lifecycle orchestration, run/application orchestration,
the CLI/logging/process-exit lifecycle, and
end-to-end/integration release validation remain incomplete. The release criteria in this
document remain unchanged.

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
