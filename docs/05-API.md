# Azure DevOps Backlog Generator

# API Specification

> *This document defines the API architecture, communication standards and Azure DevOps REST API interactions for Version 1.0 of the Azure DevOps Backlog Generator.*

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
| 0.1 | 2026-07-31 | Draft | Jack Spaetjens | Initial API Specification. |
| 1.0 | 2026-07-31 | Approved Baseline | Jack Spaetjens | Initial approved API Specification baseline. |
| 1.1 | 2026-08-20 | Approved Baseline | Jack Spaetjens | Clarified the Azure DevOps Services-only API deployment scope for Version 1.0. |
| 1.2 | 2026-08-20 | Approved Baseline | Jack Spaetjens | Defined Azure DevOps REST API version 7.1 as the Version 1.0 API-contract constant. |
| 1.3 | 2026-08-20 | Approved Baseline | Jack Spaetjens | Defined the Version 1.0 Azure DevOps REST endpoint and HTTP-method contract. |
| 1.4 | 2026-08-20 | Approved Baseline | Jack Spaetjens | Defined stable Scrum compatibility validation through work-item type metadata and validation-only creation. |
| 1.5 | 2026-08-21 | Approved Baseline | Jack Spaetjens | Standardised the Approval section to remain valid across Draft and Approved Baseline states. |
| 1.6 | 2026-08-21 | Approved Baseline | Jack Spaetjens | Defined the Version 1.0 `System.Description` content-representation contract. |
| 1.7 | 2026-08-21 | Approved Baseline | Jack Spaetjens | Defined the Version 1.0 Acceptance Criteria content-representation contract. |
| 1.8 | 2026-08-21 | Approved Baseline | Jack Spaetjens | Defined the Version 1.0 `System.Tags` content-representation contract. |

---

# Table of Contents

- [Azure DevOps Backlog Generator](#azure-devops-backlog-generator)
- [API Specification](#api-specification)
- [Version History](#version-history)
- [Table of Contents](#table-of-contents)
- [1. Introduction](#1-introduction)
- [2. Purpose](#2-purpose)
- [3. API Objectives](#3-api-objectives)
- [4. API Principles](#4-api-principles)
- [5. Authentication](#5-authentication)
- [6. Communication Standards](#6-communication-standards)
- [7. API Endpoints](#7-api-endpoints)
- [8. Request Model](#8-request-model)
- [9. Response Model](#9-response-model)
- [10. Error Handling](#10-error-handling)
- [11. Rate Limiting](#11-rate-limiting)
- [12. Traceability](#12-traceability)
- [13. Approval](#13-approval)


---

# 1. Introduction

This document defines the API interactions required by Version 1.0 of the Azure DevOps Backlog Generator.

It describes how the application communicates with Azure DevOps using the REST API while maintaining consistency with the approved Product Requirements Document and Software Architecture Document.

---

# 2. Purpose

The purpose of this document is to define the communication standards between the application and Azure DevOps.

The API Specification establishes the architectural guidelines for authentication, request handling, response processing and error management.

---

# 3. API Objectives

Version 1.0 shall achieve the following API objectives:

- Provide reliable communication with Azure DevOps.
- Support secure authentication.
- Support creation of Azure DevOps work items.
- Support creation of work item relationships.
- Provide consistent request handling.
- Provide consistent response handling.
- Support reliable error reporting.
- Maintain complete traceability to approved documentation.

---

# 4. API Principles

API communication shall follow the following principles:

- Use the Azure DevOps REST API.
- Use secure HTTPS communication.
- Maintain stateless communication.
- Validate requests before transmission.
- Validate responses before processing.
- Handle failures consistently.
- Protect sensitive information.
- Maintain traceability between requests and generated work items.

---

# 5. Authentication

Version 1.0 shall authenticate using an Azure DevOps Personal Access Token (PAT).

Authentication shall:

- Be performed before API requests are executed.
- Use HTTPS for all communication.
- Keep authentication credentials outside the application source code.
- Prevent authentication credentials from being written to application logs.

Authentication failures shall terminate execution with an appropriate error message.

---

# 6. Communication Standards

Version 1.0 shall communicate with Azure DevOps using the official REST API.

The Version 1.0 API contract targets Azure DevOps Services. Azure DevOps Server is not supported by the Version 1.0 API contract. REST requests shall use the Azure DevOps Services organisation/project addressing model.

Version 1.0 shall derive the Azure DevOps Services base URL as `https://dev.azure.com/{organization}`, where `{organization}` is the configured Azure DevOps Services organisation. No configurable base URL shall be introduced.

Communication shall adhere to the following standards:

- All communication shall use HTTPS.
- Requests shall use JSON payloads where required.
- API requests shall be validated before transmission.
- API responses shall be validated before processing.
- Communication shall be stateless.
- All supported Version 1.0 Azure DevOps REST requests shall use API version `7.1`.
- API version `7.1` shall be a single application-controlled API-contract constant.
- API version `7.1` shall not be configurable through TOML, environment variables or CLI.
- The same API version shall be used for all supported Version 1.0 REST operations unless authoritative Microsoft Azure DevOps documentation demonstrates that a supported operation requires a different version.
- Version 1.0 shall not require preview APIs.

Communication failures shall be detected, logged and reported through the application's error handling mechanism.

---

# 7. API Endpoints

Version 1.0 shall use the following Azure DevOps REST API endpoints required to support approved functionality.

| Operation | HTTP method | Endpoint path | Full pattern | Parameters | Content type |
|-----------|-------------|---------------|--------------|------------|--------------|
| Project retrieval | `GET` | `/_apis/projects/{projectId}` | `https://dev.azure.com/{organization}/_apis/projects/{projectId}?api-version=7.1` | `{organization}` is the configured Azure DevOps Services organisation; `{projectId}` is the configured project name or identifier accepted by the Azure DevOps Projects Get operation; `api-version=7.1` | None |
| Work-item type compatibility metadata | `GET` | `/{project}/_apis/wit/workitemtypes/{type}` | `https://dev.azure.com/{organization}/{project}/_apis/wit/workitemtypes/{type}?api-version=7.1` | `{organization}`, `{project}` and `{type}`; `api-version=7.1` | None |
| Work-item creation | `POST` | `/{project}/_apis/wit/workitems/{type}` | `https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{type}?api-version=7.1` | `{organization}`, `{project}` and `{type}`; `api-version=7.1` | `application/json-patch+json` |
| Work-item update | `PATCH` | `/{project}/_apis/wit/workitems/{id}` | `https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{id}?api-version=7.1` | `{organization}`, `{project}` and `{id}`; `api-version=7.1` | `application/json-patch+json` |
| Parent-child relationship update | `PATCH` | `/{project}/_apis/wit/workitems/{id}` | `https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{id}?api-version=7.1` | `{organization}`, `{project}` and `{id}`; `api-version=7.1` | `application/json-patch+json` |
| Repeatability query | `POST` | `/{project}/_apis/wit/wiql` | `https://dev.azure.com/{organization}/{project}/_apis/wit/wiql?api-version=7.1` | `{organization}` and `{project}`; `api-version=7.1`; no team parameter | `application/json` |

Work-item creation shall use the approved Version 1.0 work-item type values `Epic`, `Feature`, `Product Backlog Item` and `Task`. Work-item type values are URI path-segment values. Values containing spaces shall be correctly URI encoded when constructing the request.

Version 1.0 shall support Azure DevOps Services projects compatible with the Scrum work-item model `Epic` → `Feature` → `Product Backlog Item` → `Task`. Agile/User Story, Basic/Issue, CMMI/Requirement and arbitrary process-to-work-item-type mappings are outside the Version 1.0 API contract. Standard Scrum or an inherited/customised Scrum-compatible process may be used only when the approved work-item types, required standard field reference names and candidate payload remain compatible. Custom display names do not affect compatibility when the required reference names and field contracts remain compatible. Process mappings, work-item type mappings, field mappings and required-field overrides shall not be configurable.

Before persistent backlog generation, the Work Item Types Get operation shall be used for each required work-item type to verify its availability and inspect field metadata and required-field compatibility. The standard compatibility field reference names are `System.Title`, `System.Description`, `Microsoft.VSTS.Common.AcceptanceCriteria` where applicable, and `System.Tags`. Reference names, rather than display names, define compatibility.

`System.Description` shall receive the normative HTML fragment prepared by the Documentation Processor under the approved Description Mapping Contract in `09-Documentation-Input.md`. This contract does not define JSON Patch add or replace semantics.

When present, the normative HTML fragment prepared by the Documentation Processor under the approved Acceptance Criteria Mapping Contract in `09-Documentation-Input.md` shall be mapped to `Microsoft.VSTS.Common.AcceptanceCriteria` for Epic, Feature and Product Backlog Item. When the approved source construct is absent, no Acceptance Criteria value shall be produced and the field shall be omitted. Task shall not receive Acceptance Criteria through a fallback field, Description or a custom field.

Tags shall apply to Epic, Feature, Product Backlog Item and Task. When present, the prepared plain-text Tags value from the approved Tags Mapping Contract in `09-Documentation-Input.md` shall be mapped to `System.Tags`. The value shall consist of normalised source-order tags joined by exactly `; `. When the approved source construct is absent, no Tags value shall be produced and the field shall be omitted. This contract does not define JSON Patch add or replace semantics, create or update payloads, or tag merge or replacement behaviour.

An additional field marked `alwaysRequired` shall not alone establish incompatibility. Its metadata shall be inspected and, when static metadata alone cannot establish whether the candidate payload satisfies project/process rules, the approved Work Items Create operation may use `validateOnly=true`. Validation-only creation requests shall not persist work items, shall use the same candidate field contract intended for persistent creation, and validation failure shall prevent persistent backlog generation. Validation errors shall be reported meaningfully without exposing secrets.

Version 1.0 shall use the configured project-scoped Work Items Update form consistently. Parent-child relationships shall be created or updated using the same Work Items Update endpoint, HTTP `PATCH` and `application/json-patch+json`. Version 1.0 does not require a separate relationship-creation endpoint. Relationship changes shall be performed through the work item's relations collection using the Work Items Update operation.

Version 1.0 shall use the project-scoped WIQL endpoint for repeatability queries and shall not require a team parameter.

This section does not define detailed request payload structures, tag taxonomy, ordinary work-item update operation semantics, concrete response fields or response-validation rules, parent-child relation payload semantics, WIQL duplicate-detection semantics, PAT authentication transport or header details, error classification or recovery, or retry and rate-limit policy.

Endpoint definitions shall remain configurable where practical to support future Azure DevOps API versions. This shall not make the Version 1.0 API version externally configurable.

---

# 8. Request Model

API requests shall be constructed in a consistent manner.

Each request shall include, where applicable:

- Authentication credentials.
- Target Azure DevOps organisation.
- Target Azure DevOps project.
- Work item type.
- Work item fields.
- Parent-child relationship information.
- Request metadata.

Requests shall be validated before transmission to minimise API failures.

Where static compatibility metadata is insufficient, validation-only creation requests shall be used before persistent backlog generation to validate the candidate work-item request against project/process rules. A validation-only request shall include `validateOnly=true`, shall not persist a work item and shall use the same candidate field contract intended for persistent creation.

---

# 9. Response Model

API responses shall be validated before application processing.

The application shall process:

- Successful responses.
- Validation failures.
- Authentication failures.
- Authorisation failures.
- Resource not found responses.
- Server-side failures.

Response processing shall extract all information required for subsequent application processing while recording appropriate execution details in the application log.

---

# 10. Error Handling

Version 1.0 shall implement a consistent API error handling strategy.

The application shall:

- Detect communication failures.
- Detect authentication failures.
- Detect authorisation failures.
- Detect invalid API requests.
- Detect Azure DevOps Scrum compatibility failures before persistent backlog generation.
- Detect unexpected API responses.
- Record API failures in the application log.
- Provide meaningful error messages to the user.
- Terminate gracefully when recovery is not possible.

API error handling shall remain consistent throughout the application to support reliability, maintainability and effective diagnostics.

---

# 11. Rate Limiting

The application shall operate in a manner that respects Azure DevOps REST API usage limitations.

Version 1.0 shall:

- Detect API rate limiting where applicable.
- Report rate limiting events through the logging mechanism.
- Avoid unnecessary API requests through efficient request handling.
- Support future implementation of retry strategies if required.

Rate limiting shall not compromise application stability.

---

# 12. Traceability

This API Specification defines the communication standards supporting implementation of the approved documentation baseline.

Traceability shall be maintained between:

- Product Requirements Document
- Software Architecture Document
- Development Roadmap
- Development Standards
- API Specification
- Azure DevOps Backlog
- Source Code
- Test Documentation

The API implementation shall remain aligned with the approved Product Requirements Document and shall not introduce functionality that is not traceable to an approved requirement.

---

# 13. Approval

Approval of a document version requires:

- Completion of the editorial review.
- Approval of that document version.
- Creation of the corresponding Approved Baseline.
- Commit to the project repository using the agreed Git workflow.

The document metadata and Version History record whether the current version has completed this approval process.

Subsequent modifications shall follow the established documentation governance process and be recorded through Version History.
