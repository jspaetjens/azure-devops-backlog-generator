# Azure DevOps Backlog Generator

# Testing Strategy

> *This document defines the testing approach, quality assurance strategy and validation processes for Version 1.0 of the Azure DevOps Backlog Generator.*

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
- Validation-only candidate creation where static metadata is insufficient.

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

Work Item Create Payload validation shall additionally cover:

- the exact Create endpoint, HTTP `POST`, `application/json-patch+json` Content-Type, `api-version=7.1` and validation-only query behaviour;
- RFC 6902 JSON Patch array structure, the `add`-only Create profile and exclusion of `replace`, `remove`, `test`, `copy` and `move`;
- the exact four-field allowlist, canonical field order, mandatory Title and mandatory Description;
- optional Acceptance Criteria, mandatory Task Acceptance Criteria omission, optional Tags, absent optional-field omission and no empty placeholder operations;
- exact prepared-value preservation, JSON escaping without semantic transformation, no double HTML escaping, no Markdown re-rendering and no Tags splitting, reordering or renormalisation;
- exclusion of `System.WorkItemType`, additional fields, server-managed fields and relationship operations;
- exclusion of `bypassRules`, `suppressNotifications` and `$expand`;
- validation-only and persistent candidate-payload equivalence; and
- pre-persistence failure for incomplete or incompatible candidates.

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
- Missing required work-item types, missing or incompatible standard fields, additional project/process rules that prevent candidate creation, validation-only failures and metadata retrieval failures have been validated to stop persistent backlog generation.
- No critical or high-severity defects remain unresolved.
- Complete traceability has been maintained between requirements, implementation and testing.

Acceptance shall be based on the successful completion of the planned validation activities.

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

