# Azure DevOps Backlog Generator

# Product Requirements Document

> *This document defines the functional and non-functional requirements for the Azure DevOps Backlog Generator.*

**Version:** 1.9

**Status:** Approved Baseline

**Last Updated:** 2026-08-23

**Target Release:** v1.0.0

**License:** MIT

**Author:** Jack Spaetjens

---

# Version History

| Version | Date | Status | Author | Description |
|----------|------------|-------------------|-----------------|------------------------------------------------|
| 0.1 | 2026-07-30 | Draft | Jack Spaetjens | Initial Product Requirements Document. |
| 1.0 | 2026-07-30 | Approved Baseline | Jack Spaetjens | Initial approved Product Requirements Document baseline. |
| 1.1 | 2026-08-20 | Approved Baseline | Jack Spaetjens | Clarified Azure DevOps Services-only deployment scope for Version 1.0. |
| 1.2 | 2026-08-20 | Approved Baseline | Jack Spaetjens | Defined the Version 1.0 Scrum-compatible Azure DevOps process boundary and pre-generation compatibility validation. |
| 1.3 | 2026-08-21 | Approved Baseline | Jack Spaetjens | Integrated the approved Documentation Input Specification into the Version 1.0 product requirements. |
| 1.4 | 2026-08-21 | Approved Baseline | Jack Spaetjens | Standardised the Approval section to remain valid across Draft and Approved Baseline states. |
| 1.5 | 2026-08-21 | Approved Baseline | Jack Spaetjens | Defined the Version 1.0 mandatory Description Mapping contract. |
| 1.6 | 2026-08-21 | Approved Baseline | Jack Spaetjens | Defined the Version 1.0 Acceptance Criteria Mapping contract. |
| 1.7 | 2026-08-21 | Approved Baseline | Jack Spaetjens | Defined the Version 1.0 Tags Mapping contract. |
| 1.8 | 2026-08-23 | Approved Baseline | Jack Spaetjens | Defined the Version 1.0 Work Item Identity and Existing Item Resolution contract. |
| 1.9 | 2026-08-23 | Approved Baseline | Jack Spaetjens | Defined the Version 1.0 Existing Relationship State and Recovery contract. |

---

# Table of Contents

- [Azure DevOps Backlog Generator](#azure-devops-backlog-generator)
- [Product Requirements Document](#product-requirements-document)
- [Version History](#version-history)
- [Table of Contents](#table-of-contents)
- [1. Introduction](#1-introduction)
- [2. Purpose](#2-purpose)
- [3. Product Vision](#3-product-vision)
- [4. Project Objectives](#4-project-objectives)
- [5. Stakeholders](#5-stakeholders)
- [6. Scope](#6-scope)
  - [6.1 In Scope](#61-in-scope)
  - [6.2 Out of Scope](#62-out-of-scope)
- [7. Functional Requirements](#7-functional-requirements)
  - [FR-001 Authentication](#fr-001-authentication)
  - [FR-002 Azure DevOps Connectivity](#fr-002-azure-devops-connectivity)
  - [FR-003 Project Configuration](#fr-003-project-configuration)
  - [FR-004 Work Item Creation](#fr-004-work-item-creation)
  - [FR-005 Work Item Hierarchy](#fr-005-work-item-hierarchy)
  - [FR-006 Work Item Attributes](#fr-006-work-item-attributes)
  - [FR-007 Repeatable Execution](#fr-007-repeatable-execution)
  - [FR-008 Configuration Management](#fr-008-configuration-management)
  - [FR-009 Logging](#fr-009-logging)
  - [FR-010 Error Handling](#fr-010-error-handling)
- [8. Non-Functional Requirements](#8-non-functional-requirements)
  - [NFR-001 Maintainability](#nfr-001-maintainability)
  - [NFR-002 Reusability](#nfr-002-reusability)
  - [NFR-003 Reliability](#nfr-003-reliability)
  - [NFR-004 Performance](#nfr-004-performance)
  - [NFR-005 Security](#nfr-005-security)
  - [NFR-006 Traceability](#nfr-006-traceability)
  - [NFR-007 Testability](#nfr-007-testability)
- [9. Assumptions](#9-assumptions)
- [10. Constraints](#10-constraints)
- [11. Risks](#11-risks)
- [12. Success Criteria](#12-success-criteria)
- [13. Future Considerations](#13-future-considerations)
- [14. Requirements Traceability](#14-requirements-traceability)
- [15. Approval](#15-approval)

---

# 1. Introduction

The Azure DevOps Backlog Generator is a reusable software application that automates the creation and maintenance of Azure DevOps work items from approved project documentation.

The project aims to reduce manual backlog administration while improving consistency, repeatability and traceability throughout the software development lifecycle.

This Product Requirements Document defines the requirements for Version 1.0 of the product and serves as the functional baseline for subsequent architecture, implementation, testing and backlog planning activities.

---

# 2. Purpose

The purpose of the Azure DevOps Backlog Generator is to provide an automated mechanism for translating approved project documentation into a structured Azure DevOps backlog.

The product shall support repeatable backlog generation while maintaining alignment between documentation and Azure DevOps.

The generator is intended to minimise manual effort, improve consistency and provide complete traceability between project requirements and implementation planning.

---

# 3. Product Vision

The vision of this project is to provide a reusable and maintainable automation tool capable of generating and maintaining Azure DevOps backlogs for software projects.

The solution shall be independent of any individual project and shall support reuse across multiple repositories without requiring changes to the underlying architecture.

The product shall promote documentation-driven project planning by treating approved documentation as the authoritative source for backlog generation.

---

# 4. Project Objectives

The objectives of Version 1.0 are:

- Automate Azure DevOps backlog creation.
- Reduce manual backlog administration.
- Maintain complete traceability between approved documentation and Azure DevOps.
- Support repeatable backlog generation.
- Ensure consistent Azure DevOps work item structures.
- Maintain parent-child relationships between work items.
- Support reusable project configuration.
- Provide a maintainable Python-based solution.
- Establish a foundation for future product enhancements.

---

# 5. Stakeholders

The intended stakeholders include:

- Software Developers
- DevOps Engineers
- Scrum Masters
- Product Owners
- Solution Architects
- Technical Leads
- Project Managers

These stakeholders may use the generated Azure DevOps backlog as the operational representation of the approved project documentation.

---

# 6. Scope

This chapter defines the functional boundaries of Version 1.0 of the Azure DevOps Backlog Generator.

The scope establishes which capabilities are included in the initial release and which capabilities are intentionally excluded to maintain a manageable and well-defined product scope.

## 6.1 In Scope

Version 1.0 shall support the following capabilities:

- Authentication using an Azure DevOps Personal Access Token (PAT).
- Version 1.0 supports Azure DevOps Services.
- Support for Azure DevOps Services projects compatible with the Scrum work-item model: Epic → Feature → Product Backlog Item → Task.
- Connection to Azure DevOps through the REST API.
- Project selection through configuration.
- Creation of Epics.
- Creation of Features.
- Creation of Product Backlog Items (PBIs).
- Creation of Tasks.
- Creation of parent-child relationships between work items.
- Population of work item titles.
- Population of work item descriptions.
- Population of Acceptance Criteria.
- Application of work item tags.
- Repeatable backlog generation without creating duplicate work items.
- Backlog generation from approved backlog-input Markdown documents in the configured dedicated source directory.
- Configuration through external configuration files.
- Execution as a command-line application.

## 6.2 Out of Scope

The following capabilities are intentionally excluded from Version 1.0:

- Azure Test Plans integration.
- Azure Repos integration.
- Azure Pipelines integration.
- Azure DevOps Wiki integration.
- Azure DevOps Server deployments are not supported in Version 1.0.
- Agile/User Story mappings.
- Basic/Issue mappings.
- CMMI/Requirement mappings.
- Arbitrary process-to-work-item-type mappings.
- Microsoft Entra ID authentication.
- Graphical User Interface (GUI).
- Web application deployment.
- AI-generated project requirements.
- Automatic project documentation generation.
- Sprint planning automation.
- Release planning automation.

---

# 7. Functional Requirements

The Azure DevOps Backlog Generator shall provide the following functional requirements for Version 1.0.

Each functional requirement represents behaviour that shall be implemented by the application and serves as the primary source for the Azure DevOps backlog.

## FR-001 Authentication

The application shall authenticate with Azure DevOps using a Personal Access Token (PAT).

## FR-002 Azure DevOps Connectivity

The application shall communicate with Azure DevOps through the official REST API.

## FR-003 Project Configuration

The application shall allow project-specific configuration without requiring changes to the application source code.

## FR-004 Work Item Creation

The application shall create Azure DevOps work items.

Version 1.0 shall use the fixed Scrum work-item model:

Supported work item types include:

- Epic
- Feature
- Product Backlog Item (PBI)
- Task

Version 1.0 may operate with standard Scrum or an inherited/customised Scrum-compatible process only when the approved work-item types and required standard field contracts remain compatible and the candidate payload can satisfy the project/process rules. Process-to-work-item-type mappings shall not be configurable.

The source hierarchy and source-title interpretation for backlog generation shall be governed by `09-Documentation-Input.md`.

## FR-005 Work Item Hierarchy

The application shall create parent-child relationships between generated work items.

## FR-006 Work Item Attributes

The application shall populate supported Azure DevOps work item fields, including:

- Title
- Description
- Acceptance Criteria
- Tags

Acceptance Criteria shall be populated only where applicable to the target work-item type. Version 1.0 shall use `Microsoft.VSTS.Common.AcceptanceCriteria` where the target type exposes it: Epic, Feature and Product Backlog Item. Acceptance Criteria shall be optional for those types; when the approved Document 09 source construct is absent, no Acceptance Criteria value shall be produced and the field shall be omitted. Task does not use this field. A recognised Acceptance Criteria construct on a Task shall be invalid source input. Version 1.0 shall not invent a fallback Acceptance Criteria field for Task or automatically place Task Acceptance Criteria in Description or a custom field.

Tags shall be optional for Epic, Feature, Product Backlog Item and Task. Valid Tags derived from the approved Document 09 source construct shall be prepared for `System.Tags`. When the construct is absent, no Tags value shall be produced and the field shall be omitted. Invalid Tags source input shall prevent persistent backlog generation.

For Epic, Feature, Product Backlog Item and Task, `System.Description` shall be derived from the complete direct body of the corresponding Document 09 source item, excluding the approved reserved Tags and Acceptance Criteria constructs where present. Child semantic headings and child-item content shall be excluded according to the approved item-boundary rules. No reserved Description subsection shall be introduced.

Description shall be mandatory after Tags and Acceptance Criteria exclusion. Missing Description content, whitespace-only Description content, Description-rendering failure or an empty rendered HTML fragment shall be validation failures that prevent persistent backlog generation. `System.Description` shall not be omitted or deliberately sent as an empty value. The detailed Description Mapping, Acceptance Criteria Mapping, Tags Mapping and rendering rules are defined by `09-Documentation-Input.md`.

## FR-007 Repeatable Execution

The application shall support repeatable execution without creating duplicate work items.

Document 09 shall remain the sole authority for the logical source identity, consisting of the canonical relative file path and complete normalised semantic-heading hierarchy. Version 1.0 shall persist a deterministic, versioned SHA-256 representation of that logical identity in the generator-reserved Azure DevOps field `Custom.BacklogGeneratorSourceIdentity`. The persisted representation shall not redefine logical source identity.

`Custom.BacklogGeneratorSourceIdentity` shall have the display name `Backlog Generator Source Identity`, use the Azure DevOps String/single-line-text type and apply to Epic, Feature, Product Backlog Item and Task. It shall remain optional at Azure DevOps process level, have no default value and be mandatory in every generator-created work item. The field reference shall be fixed Version 1.0 behaviour and shall not be configurable.

The required custom field shall be provisioned outside the generator. The generator shall not create an inherited process, create the field, add it to work-item types, change the project process or field rules, choose another field, or accept a configurable field mapping. Missing or incompatible identity-field support shall be a compatibility-validation failure before persistent generation.

For every source item in deterministic source order, the application shall compute the persisted identity marker and resolve an existing work item using only the configured Azure DevOps project, exact supported work-item type and exact marker. Zero candidates shall cause Create; exactly one candidate shall be validated and its numeric Azure DevOps ID and revision reused without Create; and two or more candidates shall cause failure before Create. A malformed response, lookup failure or conflicting candidate identity shall cause failure and shall not be reinterpreted as zero candidates.

Title, parent Azure DevOps ID, State, Area Path and hierarchy similarity shall not be authoritative identity evidence. Unmarked manual work items shall not be adopted, queried heuristically by Title or hierarchy, warned about solely for matching Title, or treated as failures solely for matching Title. A sole valid item carrying the exact marker shall be authoritative identity evidence regardless of its original provenance. Humans and other integrations shall not set, copy, alter or reuse the generator-reserved marker unless intentionally representing the same generated source identity.

Reuse shall not constitute an ordinary work-item update. The application shall not compare or update Title, Description, Acceptance Criteria or Tags for synchronisation purposes, update the identity field, or send an ordinary Work Item PATCH under this contract. Description-only, Acceptance Criteria-only and Tags-only changes shall retain identity and cause reuse without update. Heading changes, ancestor-heading changes, canonical source-file or path renames, and identity-significant canonical-path case changes shall produce changed identities as defined by Document 09. Old generated items shall not be automatically renamed, migrated, updated, deleted, superseded or cleaned up.

After successful identity resolution, every reused non-root work item shall have its existing parent-relationship state inspected against its intended immediate parent. The application shall classify that state as MISSING, CORRECT or CONFLICTING. Well-formed non-parent relationships shall not affect parent-state classification, while malformed relationship data shall cause failure.

For MISSING, the application shall automatically add the intended parent by reusing the approved Parent-Child Relationship PATCH with the fresh child revision returned by relationship-state inspection. This recovery is limited to adding a missing intended parent relationship and shall not authorise ordinary field updates or generic relationship editing.

For CORRECT, the application shall perform no relationship PATCH and may continue processing descendants. For CONFLICTING, including a wrong parent, multiple parent relationships or duplicate same-parent relationships, the application shall fail without mutating remote state and shall not process descendants.

No descendants of a non-root item shall be persistently processed until its intended parent relationship has either been observed as correct or successfully established. This permits a later execution to recover when a previous execution created a child but failed to establish its parent relationship. Newly created non-root children shall retain the approved immediate relationship PATCH flow, and root Epic items shall require neither parent inspection nor a parent relationship PATCH.

Relationship-state recovery shall not change logical source identity, persisted identity markers, WIQL lookup, Work Item Create payloads, ordinary update semantics, relationship removal or replacement, retry or rollback behaviour.

## FR-008 Configuration Management

The application shall support external configuration files to enable reuse across multiple software projects.

## FR-009 Logging

The application shall provide logging sufficient to monitor execution and diagnose failures.

## FR-010 Error Handling

The application shall detect, report and handle execution errors without causing unexpected application termination where recovery is possible.

Before persistent backlog generation, the application shall validate that the configured Azure DevOps Services project is compatible with the Version 1.0 Scrum work-item model. Validation shall confirm that the configured project and the required work-item types Epic, Feature, Product Backlog Item and Task exist; that required standard fields are available and compatible where applicable; that `Custom.BacklogGeneratorSourceIdentity` has the exact approved reference name, display name and String/single-line-text contract, applies to all four supported types, is writable during Create and is not process-required; and that a candidate payload including the mandatory identity marker can satisfy project/process rules when static metadata alone is insufficient. If required compatibility metadata cannot be retrieved or compatibility cannot be established, the application shall stop before persistent backlog generation, report the incompatibility clearly and shall not fall back to another process or invent type or field mappings.

An additional field marked `alwaysRequired` shall not alone establish incompatibility. The application shall inspect the metadata and, where necessary, validate a candidate payload rather than inventing a value for an unsupported custom field.

Before persistent backlog generation, the application shall validate that approved backlog-input Markdown documents from the configured dedicated source directory conform to `09-Documentation-Input.md`. Invalid source input shall prevent persistent backlog generation.

---

# 8. Non-Functional Requirements

The Azure DevOps Backlog Generator shall satisfy the following non-functional requirements.

## NFR-001 Maintainability

The application shall be designed to support future extension and maintenance.

## NFR-002 Reusability

The application shall be reusable across multiple software projects.

## NFR-003 Reliability

The application shall produce consistent results for identical input.

## NFR-004 Performance

The application shall complete backlog generation within a reasonable execution time for typical software projects.

## NFR-005 Security

Sensitive information, including Personal Access Tokens, shall not be hard-coded into the application.

## NFR-006 Traceability

Generated Azure DevOps work items shall maintain traceability to the approved project documentation.

## NFR-007 Testability

The application shall support automated testing.

---

# 9. Assumptions

The following assumptions apply to Version 1.0:

- Azure DevOps REST APIs remain available.
- Users possess appropriate Azure DevOps permissions.
- Users can create Personal Access Tokens.
- Approved project documentation is available prior to backlog generation.
- Azure DevOps projects already exist.
- Internet connectivity is available during execution.

---

# 10. Constraints

Version 1.0 is subject to the following constraints:

- Azure DevOps REST API capabilities.
- Azure DevOps work item model.
- Python programming language.
- Git version control.
- GitHub as the source code repository.
- Personal Access Token authentication.
- Project documentation as the authoritative source for backlog generation.

---

# 11. Risks

The following risks have been identified for Version 1.0.

| ID | Risk | Impact | Mitigation |
|----|------|--------|------------|
| R-001 | Azure DevOps REST API changes | High | Monitor Microsoft API changes and update the application accordingly. |
| R-002 | Insufficient Azure DevOps permissions | Medium | Validate permissions before execution and provide clear error reporting. |
| R-003 | Incorrect project configuration | Medium | Validate configuration before backlog generation. |
| R-004 | Invalid or incomplete project documentation | High | Validate input documentation prior to generating work items. |
| R-005 | Duplicate work item creation | High | Implement repeatable execution with duplicate detection. |

---

# 12. Success Criteria

Version 1.0 shall be considered successful when the following criteria have been achieved:

- Successful authentication with Azure DevOps.
- Successful creation of Epics, Features, Product Backlog Items (PBIs) and Tasks.
- Correct creation of parent-child relationships.
- Successful population of required work item fields.
- Repeatable execution without creating duplicate work items.
- Reusable configuration supporting multiple software projects.
- Successful execution of automated tests.
- Complete traceability between approved documentation and Azure DevOps.

---

# 13. Future Considerations

The following capabilities may be considered for future versions but are intentionally excluded from Version 1.0:

- Microsoft Entra ID authentication.
- Azure DevOps Wiki integration.
- Azure Pipelines integration.
- Azure Test Plans integration.
- Graphical User Interface (GUI).
- Web application deployment.
- Additional Azure DevOps work item types.
- Support for multiple backlog templates.
- Synchronisation of existing work items.
- Support for additional project management platforms.

These items are documented to provide future direction and shall not be interpreted as requirements for Version 1.0.

---

# 14. Requirements Traceability

This Product Requirements Document is the authoritative source for all functional requirements within the project.

Traceability shall be maintained between:

- Product Requirements Document
- Software Architecture Document
- Development Roadmap
- Azure DevOps Backlog
- Source Code
- Test Documentation

The Azure DevOps backlog shall be derived exclusively from the approved documentation baseline.

No implementation, backlog item or test case shall introduce functionality that is not traceable to an approved requirement.

---

# 15. Approval

Approval of a document version requires:

- Completion of the editorial review.
- Approval of that document version.
- Creation of the corresponding Approved Baseline.
- Commit to the project repository using the agreed Git workflow.

The document metadata and Version History record whether the current version has completed this approval process.

Subsequent modifications shall follow the established documentation governance process and be recorded through Version History.
