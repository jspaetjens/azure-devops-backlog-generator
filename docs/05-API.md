# Azure DevOps Backlog Generator

# API Specification

> *This document defines the API architecture, communication standards and Azure DevOps REST API interactions for Version 1.0 of the Azure DevOps Backlog Generator.*

**Version:** 2.2

**Status:** Approved Baseline

**Last Updated:** 2026-08-23

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
| 1.9 | 2026-08-21 | Approved Baseline | Jack Spaetjens | Defined the Version 1.0 Work Item Create JSON Patch payload contract. |
| 2.0 | 2026-08-21 | Approved Baseline | Jack Spaetjens | Defined the Version 1.0 Parent-Child Relationship JSON Patch contract. |
| 2.1 | 2026-08-23 | Approved Baseline | Jack Spaetjens | Defined the Version 1.0 source-identity persistence and existing-item lookup contract. |
| 2.2 | 2026-08-23 | Approved Baseline | Jack Spaetjens | Defined the Version 1.0 reused-child relationship-state inspection and recovery contract. |

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
  - [8.1 Work Item Create Payload](#81-work-item-create-payload)
  - [8.2 Parent-Child Relationship Payload](#82-parent-child-relationship-payload)
  - [8.3 Persisted Source Identity](#83-persisted-source-identity)
  - [8.4 Existing Item Lookup](#84-existing-item-lookup)
  - [8.5 Existing Relationship State and Recovery](#85-existing-relationship-state-and-recovery)
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
| Parent-child relationship update | `PATCH` | `/{project}/_apis/wit/workitems/{childId}` | `https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{childId}?api-version=7.1` | `{organization}`, `{project}` and numeric `{childId}`; `api-version=7.1` | `application/json-patch+json` |
| Repeatability query | `POST` | `/{project}/_apis/wit/wiql` | `https://dev.azure.com/{organization}/{project}/_apis/wit/wiql?$top=2&api-version=7.1` | `{organization}` and `{project}`; `$top=2`; `api-version=7.1`; no team parameter | `application/json` |
| Existing-item retrieval | `GET` | `/{project}/_apis/wit/workitems/{id}` | `https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{id}?fields=System.TeamProject,System.WorkItemType,Custom.BacklogGeneratorSourceIdentity&api-version=7.1` | `{organization}`, `{project}` and numeric `{id}`; exact `fields`; `api-version=7.1` | None |
| Reused-child relationship-state retrieval | `GET` | `/{project}/_apis/wit/workitems/{childId}` | `https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{childId}?$expand=relations&api-version=7.1` | `{organization}`, `{project}` and numeric `{childId}`; `$expand=relations`; `api-version=7.1`; no `fields` parameter | None |

Work-item creation shall use the approved Version 1.0 work-item type values `Epic`, `Feature`, `Product Backlog Item` and `Task`. Work-item type values are URI path-segment values. Values containing spaces shall be correctly URI encoded when constructing the request.

Version 1.0 shall support Azure DevOps Services projects compatible with the Scrum work-item model `Epic` → `Feature` → `Product Backlog Item` → `Task`. Agile/User Story, Basic/Issue, CMMI/Requirement and arbitrary process-to-work-item-type mappings are outside the Version 1.0 API contract. Standard Scrum or an inherited/customised Scrum-compatible process may be used only when the approved work-item types, required field reference names and candidate payload remain compatible. Custom display names for standard fields do not affect compatibility when their required reference names and field contracts remain compatible; the generator-reserved custom identity field is the explicit exception and shall use its exact approved display name. Process mappings, work-item type mappings, field mappings and required-field overrides shall not be configurable.

Before persistent backlog generation, the Work Item Types Get operation shall be used for each required work-item type to verify its availability and inspect field metadata and required-field compatibility. The standard compatibility field reference names are `System.Title`, `System.Description`, `Microsoft.VSTS.Common.AcceptanceCriteria` where applicable, and `System.Tags`. The fixed custom integration field shall have reference name `Custom.BacklogGeneratorSourceIdentity`, display name `Backlog Generator Source Identity`, String/single-line-text type, no default value, applicability to all four supported work-item types, effective Create writability and optional process status. Reference names define API integration compatibility; the exact approved custom-field display name shall additionally be validated under this contract.

The custom identity field shall be provisioned manually outside the generator. The generator shall not create or modify an inherited process, field, work-item-type field association, project process or field rule; select another field; or accept a configurable field mapping. Missing, wrongly typed, read-only, inapplicable, process-required or otherwise incompatible identity-field support shall prevent persistent generation. Validation-only Create shall verify acceptance of the mandatory identity marker without weakening existing standard-field compatibility validation.

`System.Description` shall receive the normative HTML fragment prepared by the Documentation Processor under the approved Description Mapping Contract in `09-Documentation-Input.md`. This contract does not define JSON Patch add or replace semantics.

When present, the normative HTML fragment prepared by the Documentation Processor under the approved Acceptance Criteria Mapping Contract in `09-Documentation-Input.md` shall be mapped to `Microsoft.VSTS.Common.AcceptanceCriteria` for Epic, Feature and Product Backlog Item. When the approved source construct is absent, no Acceptance Criteria value shall be produced and the field shall be omitted. Task shall not receive Acceptance Criteria through a fallback field, Description or a custom field.

Tags shall apply to Epic, Feature, Product Backlog Item and Task. When present, the prepared plain-text Tags value from the approved Tags Mapping Contract in `09-Documentation-Input.md` shall be mapped to `System.Tags`. The value shall consist of normalised source-order tags joined by exactly `; `. When the approved source construct is absent, no Tags value shall be produced and the field shall be omitted. This contract does not define JSON Patch add or replace semantics, create or update payloads, or tag merge or replacement behaviour.

An additional field marked `alwaysRequired` shall not alone establish incompatibility. Its metadata shall be inspected and, when static metadata alone cannot establish whether the candidate payload satisfies project/process rules, the approved Work Items Create operation may use `validateOnly=true`. Validation-only creation requests shall not persist work items, shall use the same candidate field contract intended for persistent creation, and validation failure shall prevent persistent backlog generation. Validation errors shall be reported meaningfully without exposing secrets.

Version 1.0 shall use the configured project-scoped Work Items Update form consistently. Parent-child relationships shall be created or updated using the same Work Items Update endpoint, HTTP `PATCH` and `application/json-patch+json`. Version 1.0 does not require a separate relationship-creation endpoint. Relationship changes shall be performed through the work item's relations collection using the Work Items Update operation.

Version 1.0 shall use the project-scoped WIQL endpoint for repeatability queries and shall not require a team parameter.

Aside from the Work Item Create payload contract in Section 8.1, Parent-Child Relationship contract in Section 8.2, Persisted Source Identity contract in Section 8.3, Existing Item Lookup contract in Section 8.4 and Existing Relationship State and Recovery contract in Section 8.5, this section does not define tag taxonomy, ordinary work-item update operation semantics, PAT authentication transport or header details, general error classification or recovery, or retry and rate-limit policy.

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

## 8.1 Work Item Create Payload

Version 1.0 Work Item Create shall use `POST https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{type}`. Persistent Create requests shall include `api-version=7.1`. Validation-only Create requests shall include `api-version=7.1&validateOnly=true`. The Content-Type shall be `application/json-patch+json`.

The request body shall be an RFC 6902 JSON Patch array. For Version 1.0 Work Item Create, the only permitted JSON Patch operation shall be `add`. The operations `replace`, `remove`, `test`, `copy` and `move` shall not be used for Create. This constrained profile applies only to Work Item Create and does not define ordinary work-item update semantics.

Create payload operations shall use only the following field paths:

- `/fields/System.Title`
- `/fields/System.Description`
- `/fields/Microsoft.VSTS.Common.AcceptanceCriteria`
- `/fields/System.Tags`
- `/fields/Custom.BacklogGeneratorSourceIdentity`

No other field path shall be permitted. In particular, Create payloads shall not contain operations for `System.WorkItemType`, `System.State`, `System.AreaPath`, `System.IterationPath`, `System.AssignedTo`, `System.CreatedBy`, `System.Reason`, custom fields other than `Custom.BacklogGeneratorSourceIdentity`, other source-ID fields, other unapproved fields or server-managed fields. The work-item type shall be selected only through the approved `{type}` URI path parameter; no redundant `/fields/System.WorkItemType` operation shall be used. No relationship operation, including `/relations/-`, belongs in this Create field payload contract.

`System.Title`, `System.Description` and `Custom.BacklogGeneratorSourceIdentity` operations shall be present for every supported work-item type. The identity operation shall use `add`, contain the exact non-empty prepared marker, be generator-produced rather than user-authored, and always be final. `Microsoft.VSTS.Common.AcceptanceCriteria` shall be included only when prepared for Epic, Feature or Product Backlog Item and shall be omitted for Task. `System.Tags` shall be included only when prepared for any supported work-item type. Absent optional business fields shall be omitted and shall not produce empty placeholder operations.

When present, operations shall appear in exactly this order:

1. `/fields/System.Title`
2. `/fields/System.Description`
3. `/fields/Microsoft.VSTS.Common.AcceptanceCriteria`
4. `/fields/System.Tags`
5. `/fields/Custom.BacklogGeneratorSourceIdentity`

The identity operation shall remain final when either or both optional business fields are absent. The five-field allowlist does not require five operations: valid Create payloads contain three operations for Title, Description and identity; four operations when one optional business field is present; or five operations when both are present. This order is deterministic transport representation only. It does not imply priority, backlog rank, business importance, field importance or processing priority.

Persistent Create requests shall not include `validateOnly`, `bypassRules`, `suppressNotifications` or `$expand`. Validation-only Create requests shall include `validateOnly=true` and shall never include `bypassRules`, `suppressNotifications` or `$expand`. No configuration shall be introduced for these options.

Validation-only and persistent creation shall use the exact same logical candidate JSON Patch document, including the work-item type, operation count, operation order, operation types, field paths, prepared values, optional-field omissions and Content-Type. The presence of `validateOnly=true` is the only approved Create-payload contract difference. A separate validation payload shall not be defined.

The Documentation Processor shall prepare and validate the normalised Title, normative Description HTML, normative Acceptance Criteria HTML and normalised plain-text `System.Tags` content under the approved source contracts. The Backlog Generator shall supply the exact prepared identity marker. The REST Client shall exclusively construct the JSON Patch request representation from those prepared values. It may select approved paths, construct the canonical operation array, omit absent optional business fields, JSON-serialize the request, apply JSON-required escaping and transmit the request. It shall not compute or alter the identity marker, trim or normalise prepared values, re-render Markdown, transform or HTML-escape prepared HTML before JSON serialization, split, reorder or renormalise Tags, reinterpret Acceptance Criteria, invent missing values or add unapproved fields. JSON serialization escaping shall be transport encoding only and shall preserve each prepared semantic value after decoding.

The following representative payload is illustrative of the normative contract for Epic, Feature or Product Backlog Item when all optional values are prepared:

```json
[
  {
    "op": "add",
    "path": "/fields/System.Title",
    "value": "<prepared title>"
  },
  {
    "op": "add",
    "path": "/fields/System.Description",
    "value": "<prepared normative Description HTML>"
  },
  {
    "op": "add",
    "path": "/fields/Microsoft.VSTS.Common.AcceptanceCriteria",
    "value": "<prepared normative Acceptance Criteria HTML>"
  },
  {
    "op": "add",
    "path": "/fields/System.Tags",
    "value": "<prepared plain-text System.Tags content>"
  },
  {
    "op": "add",
    "path": "/fields/Custom.BacklogGeneratorSourceIdentity",
    "value": "<prepared identity marker>"
  }
]
```

The following representative Task payload shows that Acceptance Criteria shall be omitted:

```json
[
  {
    "op": "add",
    "path": "/fields/System.Title",
    "value": "<prepared title>"
  },
  {
    "op": "add",
    "path": "/fields/System.Description",
    "value": "<prepared normative Description HTML>"
  },
  {
    "op": "add",
    "path": "/fields/System.Tags",
    "value": "<prepared plain-text System.Tags content>"
  },
  {
    "op": "add",
    "path": "/fields/Custom.BacklogGeneratorSourceIdentity",
    "value": "<prepared identity marker>"
  }
]
```

When Acceptance Criteria and Tags are both absent, only the required Title, Description and identity operations shall be present:

```json
[
  {
    "op": "add",
    "path": "/fields/System.Title",
    "value": "<prepared title>"
  },
  {
    "op": "add",
    "path": "/fields/System.Description",
    "value": "<prepared normative Description HTML>"
  },
  {
    "op": "add",
    "path": "/fields/Custom.BacklogGeneratorSourceIdentity",
    "value": "<prepared identity marker>"
  }
]
```

Incomplete or incompatible candidate payloads shall not proceed to persistent creation under the approved validation behaviour. This contract does not define retry, rollback, HTTP error mapping or recovery policy.

---

## 8.2 Parent-Child Relationship Payload

Version 1.0 shall create each parent-child relationship by PATCHing the child work item using `PATCH https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{childId}?api-version=7.1`. `{childId}` shall be the numeric Azure DevOps child work-item ID. The Content-Type shall be `application/json-patch+json`.

The relation shall point from the child to its immediate parent and shall use only `System.LinkTypes.Hierarchy-Reverse`. `System.LinkTypes.Hierarchy-Forward` and all other relation types are prohibited by this contract.

The relationship JSON Patch document shall contain exactly two operations in this order:

1. A relationship-specific optimistic-concurrency `test` operation at `/rev`, with the current numeric child revision.
2. An `add` operation at `/relations/-`.

The `/rev` `test` operation shall be first and shall not define ordinary field-update concurrency semantics. The relation `add` operation shall be second. Its value shall contain exactly `rel` and `url`; relation attributes and all other relation-specific fields, including `attributes`, `comment`, `name` and `metadata`, shall not be included.

The parent relation target URL shall be `https://dev.azure.com/{organization}/_apis/wit/workItems/{parentId}`, where `{parentId}` is the numeric Azure DevOps parent work-item ID. The target URL shall not contain a project segment, `api-version`, query parameters or a browser/UI URL. The contractual `workItems` path spelling and casing shall be preserved.

The representative payload below illustrates the normative contract:

```json
[
  {
    "op": "test",
    "path": "/rev",
    "value": <childRevision>
  },
  {
    "op": "add",
    "path": "/relations/-",
    "value": {
      "rel": "System.LinkTypes.Hierarchy-Reverse",
      "url": "https://dev.azure.com/{organization}/_apis/wit/workItems/{parentId}"
    }
  }
]
```

Relationship PATCH requests shall include only `api-version=7.1`. They shall not include `validateOnly`, `bypassRules`, `suppressNotifications` or `$expand`, and no configuration shall be introduced for these options. Version 1.0 shall not use or define a validation-only Parent-Child Relationship PATCH; the approved validation-only Work Item Create contract remains unchanged.

Only the following direct hierarchy edges are permitted: Epic → Feature, Feature → Product Backlog Item and Product Backlog Item → Task. Each newly created Feature, Product Backlog Item and Task shall have exactly one intended immediate parent in the candidate hierarchy and shall receive exactly one relationship PATCH. A reused non-root item classified MISSING under Section 8.5 shall receive the same relationship PATCH unchanged. Root Epic items shall receive no relationship PATCH. Direct hierarchy shortcuts, including Epic → Product Backlog Item, Epic → Task and Feature → Task, are prohibited. Relationship operations shall not be batched for multiple children.

Relationship creation requires the numeric parent Azure DevOps work-item ID, numeric child Azure DevOps work-item ID and current numeric child revision. The successful child Create response supplies the child ID and revision. Approved source identity shall not substitute for Azure DevOps numeric IDs.

Persistent orchestration shall resolve or create the parent before resolving or creating its child. For every newly created non-root child, the relationship PATCH shall occur immediately after successful child creation once the parent ID, child ID and child revision are known: resolve-or-create parent → create child → PATCH newly created child-to-parent relationship → continue generation. Relationship creation for newly created children shall not be deferred until all work items have been created. Reused non-root children shall follow Section 8.5 and shall not alter this newly created child flow.

If a Parent-Child Relationship PATCH fails, persistent backlog generation shall stop immediately. The failure shall be reported clearly without exposing secrets; later work items and relationships shall not be created. Version 1.0 shall not automatically retry, roll back, delete created work items, remove created relationships, repair remote state or continue collecting later relationship failures. Already-created work items and relationships shall remain as accepted partial persistent state.

Section 8.5 defines purpose-specific relation retrieval and missing-parent recovery for reused non-root children. Neither section defines relation merge, replacement or deletion, relation-index PATCH operations, WIQL relation detection, retry behaviour, rollback, ordinary work-item field-update semantics, generic update concurrency, or Tags merge or replacement behaviour. Parent-child relationships remain excluded from the Work Item Create payload contract and are established only through this subsequent relationship PATCH.

---

## 8.3 Persisted Source Identity

`09-Documentation-Input.md` shall remain the sole authority for logical source identity. The persisted identity marker shall be only an Azure DevOps-side deterministic representation of the canonical relative file path plus complete normalised semantic-heading hierarchy and shall not redefine that logical identity.

The Backlog Generator shall construct the SHA-256 input as this exact byte sequence:

1. ASCII bytes for `adbg-source-identity-v1`.
2. One zero byte, `0x00`.
3. The unsigned 32-bit big-endian byte length of the canonical relative path.
4. The canonical relative path encoded as UTF-8 without a byte-order mark.
5. The unsigned 32-bit big-endian number of semantic-heading components.
6. For each hierarchy component in order:
   1. one unsigned 8-bit semantic heading level, restricted to 1, 2, 3 or 4;
   2. the unsigned 32-bit big-endian UTF-8 byte length of the already-normalised title; and
   3. the already-normalised title encoded as UTF-8 without a byte-order mark.

Lengths shall count UTF-8 bytes rather than Unicode code points. The canonical relative path and normalised titles shall be used exactly as defined by Document 09. No Unicode re-normalisation, newline, delimiter text, JSON framing, locale encoding, platform path-separator conversion or additional whitespace shall be applied. The heading-level byte is structural framing only and shall not redefine source identity.

No Description, Acceptance Criteria, Tags, Azure DevOps ID, project name, organisation, work-item type label, parent Azure DevOps ID, remote state or configuration value shall participate in the digest.

SHA-256 shall be computed over the framed bytes and encoded as exactly 64 lowercase hexadecimal ASCII characters. The complete persisted marker shall be:

```text
adbg:source-id:v1:sha256:<64-lowercase-hex-digits>
```

It shall match exactly `adbg:source-id:v1:sha256:[0-9a-f]{64}` and shall be compared ordinally and case-sensitively. Uppercase hexadecimal shall not be equivalent. A malformed marker shall be rejected rather than sanitised or repaired.

If two distinct logical source identities produce the same complete marker within one execution, validation shall fail before persistent generation. The generator shall not select one identity, alter the digest or continue persistent generation.

---

## 8.4 Existing Item Lookup

The authoritative existing-item lookup key shall consist only of the configured Azure DevOps project, exact supported work-item type and exact persisted identity marker. Title, parent Azure DevOps ID, State, Area Path and manual hierarchy similarity shall not participate.

Lookup shall use:

```http
POST https://dev.azure.com/{organization}/{project}/_apis/wit/wiql?$top=2&api-version=7.1
Content-Type: application/json
```

The JSON request shall contain a fixed WIQL query of this canonical shape:

```sql
SELECT [System.Id]
FROM WorkItems
WHERE [System.TeamProject] = @project
  AND [System.WorkItemType] = '<fixed-supported-type>'
  AND [Custom.BacklogGeneratorSourceIdentity] = '<validated-marker>'
```

The supported type literal shall be exactly `Epic`, `Feature`, `Product Backlog Item` or `Task`. The custom field reference, query structure and operators shall be application constants. The marker shall be validated against the contractual format before insertion. Caller-controlled fields, operators or WIQL fragments and source-derived titles, paths, headings, parent IDs, State or Area values shall not be interpolated. `$top=2` shall distinguish zero, one and ambiguous multi-match outcomes without unbounded retrieval.

WIQL results shall be handled as follows:

- Zero returned IDs shall authorise Create using Section 8.1.
- Exactly one returned ID shall require the Work Item GET below and shall not yet authorise Create or reuse.
- Two returned IDs shall be ambiguous and shall fail before Create without retrieving additional candidates.
- Duplicate ID entries, missing IDs or non-numeric IDs shall be malformed or conflicting responses and shall fail before Create.
- WIQL transport or API failure shall fail before Create.

After exactly one candidate, the REST Client shall request:

```http
GET https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{id}?fields=System.TeamProject,System.WorkItemType,Custom.BacklogGeneratorSourceIdentity&api-version=7.1
```

The accepted response shall provide a numeric `id`, numeric `rev`, `System.TeamProject`, `System.WorkItemType` and `Custom.BacklogGeneratorSourceIdentity`. Before reuse, the configured project shall have been resolved through the approved Project retrieval operation and its canonical Azure DevOps project name and ID retained. `System.TeamProject` shall equal that canonical project name rather than being compared blindly with the raw configured project value. Work-item type shall equal the requested fixed type exactly, including case. The marker shall equal the prepared marker ordinally and case-sensitively.

A missing, null, malformed or non-numeric required property; wrong project; wrong type or type case; missing marker; or marker value or case mismatch shall be conflicting identity evidence. Candidate retrieval or validation failure shall fail before Create and shall not be reinterpreted as zero matches.

After successful candidate validation, the Backlog Generator shall retain the numeric ID and revision, associate the existing item with the source item and skip Create. No Create request shall occur for that source item after successful resolution. Reuse shall not compare business fields for update purposes, update Title, Description, Acceptance Criteria, Tags or identity, or send an ordinary Work Item PATCH. The retained revision is remote state only and shall not authorise an update.

Unmarked manual items shall remain outside the generator identity domain. They shall not be adopted through Title or hierarchy, queried heuristically for Title collisions, warned about solely for matching Title, or cause failure solely for matching Title. A sole valid item carrying the exact marker shall be authoritative identity evidence regardless of provenance. The identity field is generator-reserved; humans and other integrations shall not set, copy, alter or reuse a marker unless intentionally representing the same generated source identity.

Description-only, Acceptance Criteria-only and Tags-only changes shall preserve identity and cause reuse without update. Heading, ancestor-heading, canonical source-file or path, and identity-significant canonical-path case changes shall change identity under Document 09. Old generated items shall not be automatically renamed, migrated, updated, deleted, superseded or cleaned up.

Successful reuse under this section authorises only the subsequent purpose-specific relationship-state handling in Section 8.5 for a non-root child. It shall not authorise ordinary field updates, identity migration, WIQL changes, relationship replacement or deletion, retry or rollback.

Identity lookup diagnostics shall remain secret-safe. PATs and Authorization headers shall never be logged. Full remote response bodies shall not be logged by default, and raw logical source identities shall not be logged unnecessarily. Permitted diagnostics may include the work-item type, candidate count, numeric Azure DevOps ID, shortened digest fingerprint and source processing context where already permitted.

---

## 8.5 Existing Relationship State and Recovery

This contract applies only to a reused non-root work item after successful Existing Item Lookup under Section 8.4. It provides deterministic recovery from a prior partial relationship-generation failure without introducing ordinary field updates or generic relation editing. Root Epic items and newly created non-root children shall bypass this relationship-state GET.

For every reused non-root child, the REST Client shall request exactly:

```http
GET https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{childId}?$expand=relations&api-version=7.1
```

No `fields` parameter shall be included. The accepted response shall provide a numeric `id` equal to the reused numeric child ID and a numeric `rev`. A missing, null, malformed or non-numeric required ID or revision, or an ID mismatch, shall fail immediately.

The `relations` property shall be interpreted and validated as follows:

- An omitted `relations` property shall represent zero returned relations.
- A present empty JSON array shall represent zero returned relations.
- A present `null` value or any other non-array value shall be malformed and shall fail.
- Every member of a non-empty relation array shall be a JSON object containing a non-empty string `rel` and a non-empty string `url`.
- Any invalid member shall invalidate the complete response; malformed relation data shall not be ignored or repaired.
- `attributes` shall be optional and irrelevant to Version 1.0 parent-state evaluation.

Only the exact case-sensitive relation reference `System.LinkTypes.Hierarchy-Reverse` shall count as parent evidence. A case-altered form shall be malformed or conflicting evidence and shall fail. Structurally valid non-parent relations, including `System.LinkTypes.Hierarchy-Forward`, Related, Dependency, Hyperlink, ArtifactLink and other well-formed non-parent relations, shall be ignored for parent-state classification.

For every `System.LinkTypes.Hierarchy-Reverse` relation, the REST Client shall parse `url` as an absolute URI and require all of the following:

- the scheme is HTTPS;
- the host is `dev.azure.com`;
- the first path component is the configured organisation;
- the remaining route is exactly `_apis/wit/workItems/{id}`;
- no query or fragment is present;
- no extra path segment follows `{id}`; and
- `{id}` is a positive base-10 integer.

URI scheme and host shall use normal case-insensitive URI comparison. The contractual work-item route structure shall remain fixed. The REST Client shall extract the numeric target ID only after complete structural validation. It shall not use unconstrained terminal-ID parsing. The Backlog Generator shall compare the extracted numeric target ID with the intended numeric parent ID rather than requiring raw full-URL string equality. No separate parent GET shall be performed.

The Backlog Generator shall classify the validated parent state as follows:

- MISSING: zero `System.LinkTypes.Hierarchy-Reverse` relations, including when only well-formed unrelated or `System.LinkTypes.Hierarchy-Forward` relations exist.
- CORRECT: exactly one valid `System.LinkTypes.Hierarchy-Reverse` relation whose parsed numeric target ID equals the intended parent ID. Well-formed unrelated or forward relations may coexist.
- CONFLICTING: exactly one reverse relation points to a different parent, two or more reverse relations exist, duplicate same-parent reverse relations exist, the correct parent coexists with another reverse relation, or malformed reverse-hierarchy evidence exists.

Malformed overall response structure shall fail immediately rather than becoming a normal classification.

For MISSING, the REST Client shall automatically add the intended parent using the Parent-Child Relationship PATCH in Section 8.2 unchanged. The relationship-specific `/rev` `test` value shall be the fresh numeric revision returned by the relationship-state GET. That revision shall supersede the earlier Existing Item Lookup revision only for this recovery request. Successful recovery permits descendant processing.

For CORRECT, no relationship PATCH or `/rev` test shall occur, and descendant processing may continue. A difference between the fresh relationship-state revision and the earlier Existing Item Lookup revision shall not itself be a failure.

For CONFLICTING, processing shall fail immediately without mutating remote state or processing descendants. The application shall not add a second parent, deduplicate relationships, remove, replace or move a relationship, modify identity or use a relation-index PATCH operation.

If the relationship-state GET fails, its response is malformed, target URI validation fails, the state is CONFLICTING, the recovery `/rev` test fails or the recovery PATCH fails, processing shall stop immediately and descendants shall remain blocked. The application shall not automatically re-read, retry, roll back, delete, remove or replace remote state.

No descendants of a non-root item shall be persistently processed until its intended parent relationship is known to be correct. Eligibility shall occur only after a newly created child's immediate relationship PATCH succeeds, a reused child is observed as CORRECT or a reused child classified MISSING is successfully repaired.

The approved partial-run recovery lifecycle shall be:

```text
Run 1: parent created → child created → relationship PATCH fails → stop
Run 2: parent resolved → child resolved → relationship-state GET → MISSING
       → repair using fresh revision → repair succeeds → continue descendants
```

Permitted diagnostics may include the numeric child ID, intended parent ID, classification, reverse-parent count, repair result and revision where useful. PATs, Authorization headers, unnecessary full response bodies and relation URLs when numeric target IDs suffice shall not be logged.

This section shall not change logical source identity, persisted marker construction, WIQL lookup, Work Item Create, the newly created child relationship payload or ordinary update semantics. It shall not authorise arbitrary relation editing, removal, replacement, move, relation-index operations, retry, rollback or new configuration.

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
