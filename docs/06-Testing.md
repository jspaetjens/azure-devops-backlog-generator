# Azure DevOps Backlog Generator

# Testing Strategy

> *This document defines the testing approach, quality assurance strategy and validation processes for Version 1.0 of the Azure DevOps Backlog Generator.*

**Version:** 2.7

**Status:** Approved Baseline

**Last Updated:** 2026-08-28

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
| 1.9 | 2026-08-21 | Approved Baseline | Jack Spaetjens | Defined test coverage for the Version 1.0 Parent-Child Relationship contract. |
| 2.0 | 2026-08-23 | Approved Baseline | Jack Spaetjens | Defined test coverage for source identity, lookup and existing-item resolution. |
| 2.1 | 2026-08-23 | Approved Baseline | Jack Spaetjens | Defined test coverage for reused-child relationship-state inspection and recovery. |
| 2.2 | 2026-08-25 | Draft | Jack Spaetjens | Defined test coverage for run-level duplicate logical identity and persisted-marker collision validation. |
| 2.3 | 2026-08-25 | Approved Baseline | Jack Spaetjens | Defined test coverage for the urllib REST Client Foundation and redirect behaviour. |
| 2.4 | 2026-08-25 | Approved Baseline | Jack Spaetjens | Defined test coverage for the REST Client Foundation proxy contract. |
| 2.5 | 2026-08-27 | Approved Baseline | Jack Spaetjens | Clarified test coverage for Scrum compatibility evidence and mandatory validation-only candidate checks. |
| 2.6 | 2026-08-28 | Approved Baseline | Jack Spaetjens | Defined test coverage for successful Parent-Child Relationship PATCH response validation. |
| 2.7 | 2026-08-28 | Approved Baseline | Jack Spaetjens | Defined authorization-failure and least-privilege test coverage for Version 1.0. |

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
- future generator/application orchestration coverage confirming that no later mutation occurs after an authorization failure.

Scrum Compatibility validation shall additionally cover:

- Work Item Types Get evidence for the fixed Epic, Feature, Product Backlog Item and Task types;
- Work Item Type Field Get with `$expand=All` as type-specific evidence, and Fields Get as global field-definition evidence, without treating global metadata as proof of type applicability;
- structural validation of required standard fields and the fixed `Custom.BacklogGeneratorSourceIdentity` reference name, display name, String type, non-read-only state, applicability, no-default state and `alwaysRequired=false` optional process-level state, using only properties returned by the approved endpoints;
- failure before persistent generation for absent, malformed, wrongly typed, read-only, inapplicable, defaulted, process-required or otherwise incompatible required-field evidence;
- additional `alwaysRequired` fields not causing compatibility failure solely from that property;
- mandatory non-persisting validation-only Create checks after structural compatibility and before existing-item resolution or persistent generation for every work-item type occurring in processed input;
- use of the exact candidate JSON Patch contract, including the identity marker and all fields emitted for the candidate, with `validateOnly=true` as the only approved request difference from persistent Create;
- validation-only rejection caused by an additional required field or other process rule stopping processing before persistent generation;
- no automatic retry, no persistent work-item creation and secret-safe diagnostics throughout compatibility validation; and
- explicit handling of materially different optional-field candidate shapes within one work-item type when representative coverage is defined by a later approved decision.

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
