# Azure DevOps Backlog Generator

# Operator Guide

> *This document explains how to configure and run the supported Version 1.0 application and interpret its operational outcomes.*

**Version:** 1.0

**Status:** Approved Baseline

**Last Updated:** 2026-09-19

**Target Release:** v1.0.0

**License:** MIT

**Author:** Jack Spaetjens

---

# Version History

| Version | Date | Status | Author | Description |
|----------|------------|-------------------|-----------------|------------------------------------------------|
| 1.0 | 2026-09-19 | Approved Baseline | Jack Spaetjens | Initial Gate-3 operator guide covering supported invocation, configuration, logging, persistence/reuse and controlled HTTP reporting. |

---

# Table of Contents

- [1. Purpose and Scope](#1-purpose-and-scope)
- [2. Prerequisites](#2-prerequisites)
- [3. Installation and Runtime Assumptions](#3-installation-and-runtime-assumptions)
- [4. Configuration](#4-configuration)
- [5. Credentials and Permissions](#5-credentials-and-permissions)
- [6. Running the Application](#6-running-the-application)
- [7. Exit Behaviour](#7-exit-behaviour)
- [8. Logging](#8-logging)
- [9. Execution Summary](#9-execution-summary)
- [10. Validation and Persistence Behaviour](#10-validation-and-persistence-behaviour)
- [11. Existing-Item Reuse and Relationship Handling](#11-existing-item-reuse-and-relationship-handling)
- [12. Failure and Recovery Behaviour](#12-failure-and-recovery-behaviour)
- [13. HTTP 401 / 403 / 429 Reporting](#13-http-401--403--429-reporting)
- [14. Operational Limitations](#14-operational-limitations)
- [15. Troubleshooting Boundaries](#15-troubleshooting-boundaries)
- [16. Security Considerations](#16-security-considerations)

---

# 1. Purpose and Scope

This guide supports operators configuring and running the existing package application
against Azure DevOps Services. It explains configuration, access, reporting and the
bounded handling of failures and later reruns.

Version 1.0 remains **PRE-RELEASE**. Gate 3 remains **NOT PASSED** and Gate 4 remains
**FUTURE**. Required live Azure DevOps Services validation remains incomplete. This
Draft supplies operator guidance; it does not establish release readiness, change any
acceptance status or authorise live validation.

The Approved Baseline remains authoritative. This guide follows
[Architecture Sections 13.3–13.5](02-Architecture.md#133-runtime-safety-and-recovery-boundaries),
including G3-OWN-D13 Option B, the [Configuration Specification](08-Configuration.md),
and [API Sections 6–8](05-API.md#6-communication-standards). The
[Roadmap](03-Roadmap.md#51-review-gate-3-next-governance-milestone),
[Testing Strategy](06-Testing.md#91-review-gate-3-evidence-requirements) and
[Release Management](07-Release.md#81-review-gate-3-operational-readiness-acceptance)
retain their separate evidence, approval and gate requirements.

---

# 2. Prerequisites

Use an existing Azure DevOps Services organisation and project with a supported Scrum
or compatible inherited/customised Scrum process. The fixed hierarchy is:

```text
Epic → Feature → Product Backlog Item → Task
```

All four work-item types must exist. The project must expose compatible standard fields:
`System.Title`, `System.Description`, `System.Tags`, and
`Microsoft.VSTS.Common.AcceptanceCriteria` for Epic, Feature and Product Backlog Item.
Task does not use Acceptance Criteria. The actual candidate values must also satisfy
the target project/process rules.

The following identity-field prerequisite must be provisioned outside the generator:

| Property | Required value |
|----------|----------------|
| Reference name | `Custom.BacklogGeneratorSourceIdentity` |
| Display name | `Backlog Generator Source Identity` |
| Type | Azure DevOps `String` / single-line text |
| Applicability | Epic, Feature, Product Backlog Item and Task |
| Writability | Writable during Create |
| Default | No configured default |
| Process requirement | Optional at process level; mandatory in every generator-created item |

The generator does not provision or repair the process, field, type associations or
field rules. Missing or incompatible prerequisites stop generation before persistence.
It does not select an alternative field or process mapping.

Prepare approved backlog-input Markdown in a dedicated readable source directory,
following the [Documentation Input Specification](09-Documentation-Input.md). Do not
select the repository's general `docs/` directory or a mixed directory of arbitrary
Markdown. Input descriptions are mandatory; optional Tags and Acceptance Criteria
must follow that specification.

The runtime needs direct HTTPS connectivity to Azure DevOps Services and a usable,
writable logging directory. Azure DevOps Server and ambient environment/system proxy
configuration are not supported by the current transport contract.

---

# 3. Installation and Runtime Assumptions

Use Python 3.14.x and the project's `.venv` virtual environment. The PowerShell
examples below assume the repository root is the current working directory and the
project is installed in that environment. They invoke `.venv` explicitly, so activation
is not required for these examples.

Follow [Local development setup](../README.md#local-development-setup) to create the
environment and install the project and its declared dependencies. The existing
editable installation command, expressed with the explicit environment path, is:

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

Dependencies are declared in `pyproject.toml`. This guide introduces no installation
method, dependency or additional launcher beyond the existing project setup and
supported package invocation.

---

# 4. Configuration

The default configuration file is `config/config.toml`, selected relative to the
process current working directory. This is local runtime configuration, not a tracked
repository file. If it has not already been created, copy the tracked template from
the repository root:

```powershell
Copy-Item -LiteralPath "config\config.example.toml" -Destination "config\config.toml"
```

Edit the required non-secret values for the target environment. The supported settings
are:

| TOML setting | Requirement or default |
|--------------|------------------------|
| `azure_devops.organization` | Required organisation value |
| `azure_devops.project` | Required project value |
| `documentation.source_directory` | Required dedicated backlog-input directory |
| `logging.level` | Optional; default `INFO` |
| `logging.log_directory` | Optional; default `../logs` |

The `[application]` and `[generator]` tables may be omitted; if present, they must be
empty. Unknown sections or keys are validation errors. There is no PAT TOML key.

`--config-file` selects one explicit file instead of default discovery. A relative
configuration-file operand resolves from the process working directory. Relative
paths **inside** the selected TOML file resolve from the directory containing that
file. For example, `../logs` in `config/config.toml` resolves to the repository's
`logs/` directory when using the repository-root examples.

Exactly one configuration file is used. There are no overlays or file merging.
`--config-file` accepts one file-path operand and has no short alias. Repeating the
option, omitting or emptying its operand, or selecting a missing, unreadable, non-file
or invalid TOML path causes a controlled failure; explicit-selection errors do not
fall back to the default file. The default file must also exist and be valid.

`AZDO_PAT` is the only supported environment configuration input. It supplies the
credential; it does not override TOML settings. No other environment or CLI setting
overrides are introduced. See [Configuration Sections 5–8](08-Configuration.md#5-configuration-structure).

---

# 5. Credentials and Permissions

Provide the PAT through `AZDO_PAT` in the runtime environment before invocation,
using approved operational credential handling. An absent or whitespace-only value
is a configuration error. The application uses the original credential value for
requests and does not persist it.

Do not put a PAT in TOML, CLI arguments, source files, logs or diagnostic evidence.
Do not print the value to verify that credential setup succeeded.

The required PAT scopes are:

- `Project and Team: Read`.
- `Work Items: Read & write`.

The identity owning the PAT must also have:

- `View project-level information` in the target project.
- `View work items in this node` for applicable Area Paths.
- `Edit work items in this node` for applicable Area Paths.
- `Create tag definition` only when submitting a previously undefined tag.

PAT scopes do not bypass project or Area Path permissions. Broader scopes, Work Items
full access, administrator roles, process administration and deletion permissions are
not required for generator execution. Prerequisite provisioning is external to the
generator. See [API Section 6.2](05-API.md#62-authorization-and-least-privilege-contract).

---

# 6. Running the Application

The supported invocation is `python -m azure_devops_backlog_generator`. After completing
configuration, prerequisites and credential setup, invoke it from the repository root
with the project environment:

```powershell
.\.venv\Scripts\python.exe -m azure_devops_backlog_generator
```

To select an explicit configuration file, use:

```powershell
.\.venv\Scripts\python.exe -m azure_devops_backlog_generator --config-file "config\config.toml"
```

These are alternative invocations. Each performs a normal run against the configured
target. Review the target and input before running: successful preflight permits real
work-item creation and relationship changes. There is no supported dry-run mode.

---

# 7. Exit Behaviour

| Process exit status | Meaning |
|---------------------|---------|
| `0` | Successful controlled execution |
| `1` | Handled application failure, including the bounded unexpected-error fallback |

There is no differentiated numeric exit taxonomy. Successful execution produces no
normal stdout or stderr output. Handled failures use the approved stderr report;
eligible failures also use the configured logfile as described below.

The package adapter owns process termination using the application result. The
processed-item count is not an exit code. Process-control exceptions and failures in
stderr delivery retain their separate propagation boundaries; the `0`/`1` contract
does not promise to translate every externally interrupted or broken-output execution.

---

# 8. Logging

The logfile is `azure-devops-backlog-generator.log` inside the configured
`logging.log_directory`. Records are appended using UTF-8. The default directory is
`../logs`, relative to the selected configuration file's directory.

The application creates a missing logging directory before file logging begins.
Failure to create or use it stops execution. There is no fallback logfile destination,
and the application does not provide configurable filenames, rotation or retention.

`logging.level` defaults to `INFO` and accepts `DEBUG`, `INFO`, `WARNING`, `ERROR` and
`CRITICAL` case-insensitively. START, SUMMARY and COMPLETION use INFO: they are eligible
at DEBUG/INFO and filtered at WARNING/ERROR/CRITICAL. Their delivery is best effort, so
an absent INFO record is not by itself proof of application failure.

START (`Application run started.`) follows successful configuration validation and
logger initialisation. It means application execution was reached; it does not prove
documentation processing, Azure DevOps connectivity or persistence. COMPLETION
(`Application run completed successfully.`) follows normal application return and is
separate from SUMMARY.

Configuration failures occur before logger initialisation and report
`Configuration error.` to stderr only. If logger initialisation fails after valid configuration,
`Application logging error.` is also reported without a configured-file event or
fallback destination. Other pre-initialisation failures likewise cannot use configured
logfile reporting.

Eligible post-initialisation controlled failures use one CRITICAL logfile emission
attempt and the process-boundary stderr report. CRITICAL is eligible at every supported
threshold. Only the current invocation's owned handler receives the logfile event;
there is no root/console/fallback logging or duplicate delivery. An ordinary secondary
logfile-write failure preserves the primary failure and stderr attempt without retry.
The unexpected-error fallback reports the fixed `Unexpected application error.` and
uses an eligible best-effort CRITICAL logfile attempt.

---

# 9. Execution Summary

After successful configured application execution, the exact logical summary is:

```text
Execution summary: outcome=success; source_items_processed=N.
```

`N` is the number of semantic source items whose processing completed in that
invocation. Each Epic, Feature, Product Backlog Item and Task counts once, whether
created or reused. Relationship repair and HTTP requests do not add items to the
count. It covers all processed documents and roots; a permitted zero-item success
reports `0`.

The summary is a processed-source-item count, not a created-item count or independently
inspected remote inventory. It supplies no created/reused/repaired breakdown.

SUMMARY is attempted before the separate COMPLETION event, only in the configured
logfile at INFO. Filtering and best-effort delivery apply. An ordinary summary-delivery
failure does not change domain success or prevent an independently eligible COMPLETION
attempt. Successful console output remains empty.

There is no SUMMARY on failed or partial execution, including a conflicting/global-stop
failure. **Absence of SUMMARY does not prove that no remote mutation occurred.** A later
successful rerun reports only its own processed-item count.

---

# 10. Validation and Persistence Behaviour

Version 1.0 has no supported dry-run mode. Internal preflight and validation-only
requests are not a dry-run and are not an operator-selectable mode.

The application validates configuration and processes the source documents. Before
persistence, it checks source identities, retrieves project and compatibility evidence,
and validates every actual candidate through non-persisting Create with
`validateOnly=true`. Each candidate must be accepted independently; a similar candidate
does not stand in for another.

All validation-only candidate checks must succeed before existing-item lookup,
existing-item GET, persistent Create, relationship-state GET or parent-child PATCH
begins. Invalid source input, incompatible prerequisites or rejected candidates stop
the run before persistence.

After that mutation barrier, deterministic parent-before-child processing performs
real persistence where needed. A newly created non-root item is immediately followed
by its parent-child PATCH; descendants begin only after the parent relationship is
eligible. A successful reused/CORRECT run may make no persistent changes, but still
makes Azure DevOps requests and is not a dry-run.

---

# 11. Existing-Item Reuse and Relationship Handling

Reuse is based on the configured project, exact supported work-item type and exact
persisted source-identity marker. Zero matches permits Create; one valid match is
reused; ambiguity, malformed evidence or lookup failure stops processing. An error
is not treated as permission to create a replacement item.

Source identity derives from the canonical relative source-file path and complete
normalised semantic-heading hierarchy. Matching titles or similar remote hierarchies
alone do not establish identity. Unmarked manual items are not automatically adopted.

Rediscovery does not perform ordinary field synchronisation. Description, Acceptance
Criteria or Tags changes retain identity but do not update reused fields. Heading,
ancestor-heading or identity-significant source-path changes produce changed identities;
old items are not automatically renamed, migrated or deleted. Do not alter or copy the
generator-reserved identity marker to force reuse.

For each reused non-root child, fresh relationship evidence determines the next action:

| State | Meaning | Behaviour |
|-------|---------|-----------|
| `MISSING` | No parent relationship exists. | Add the intended missing parent using the fresh child revision; continue only after successful PATCH. |
| `CORRECT` | Exactly one parent relationship exists and it identifies the intended parent. | Continue without relationship PATCH. |
| `CONFLICTING` | A valid non-empty parent state is not exactly one intended parent, including a wrong parent, multiple parents or duplicate same-parent relationships. | Stop without relationship repair or descendant processing beneath the blocked child. |

Malformed relationship evidence is a failure rather than a repair opportunity.
Root Epics do not require parent inspection or parent PATCH. A conflicting child also
stops later work elsewhere in the invocation under global fail-fast.

---

# 12. Failure and Recovery Behaviour

The first configuration, source-processing or Generator failure stops the invocation.
No later document, root, sibling, descendant or Azure DevOps generator operation begins.
Already accepted remote changes remain
legitimate partial persistence: there is no transaction-like undo, automatic rollback,
deletion compensation or other compensating mutation.

For example, child Create can succeed before its parent-child PATCH fails. A later
normal invocation can rediscover and reuse the child, inspect its current relationships
and add the missing intended parent through the MISSING path. The earlier successful
Create is not automatically repeated merely because the relationship operation failed.
An uncertain Create response can also leave a remote item even when the run reports
failure; do not assume a failed run made no changes.

Before choosing a later invocation, inspect the failure and relevant remote state
through approved operational means. Rerunning does not guarantee success if incompatible
configuration, access, source input or conflicting relationships remain.

The application performs no automatic retry, sleep/backoff, generic fallback recovery,
credential switching, rollback, compensation or automatic deletion. Broader Operational
Recovery / Disaster Recovery is outside Version 1.0 under G3-D3. The bounded later-run
reuse/relationship behaviour is not a generic disaster-recovery subsystem.

---

# 13. HTTP 401 / 403 / 429 Reporting

| HTTP status | Meaning | Exact logical message |
|-------------|---------|-----------------------|
| `401` | Authentication rejection | `Azure DevOps authentication failed.` |
| `403` | Authorisation failure | `Azure DevOps authorisation failed.` |
| `429` | Rate-limit rejection | `Azure DevOps rate limit reached.` |

For each status, the specific message replaces `Azure DevOps error.` in both logfile
and stderr. No additional generic report is emitted for the same failure. Logfile
severity is CRITICAL, the process outcome remains `1`, and the one-attempt delivery
and primary-failure protections in Section 8 apply.

Other Azure DevOps REST-client errors retain the generic `Azure DevOps error.` report.
The status-specific messages identify categories, not independently verified root causes.
A 401 report does not establish that a PAT is expired or revoked. A 403 report does not
identify an exact missing PAT scope, project permission, group or policy. Such diagnoses
require independent operational evidence.

`Retry-After` is omitted entirely from application reporting. It is not inspected or
parsed for reporting, propagated into reporting, echoed as raw header data or used for
header-derived diagnostics. A 429 ends the failed operation without application sleep,
retry or backoff.

---

# 14. Operational Limitations

The current Version 1.0 application provides no:

- Supported dry-run mode.
- Automatic retry, sleep/backoff, rollback or compensation.
- Ordinary field synchronisation of reused work items.
- Generator-managed process or identity-field provisioning/repair.
- Automatic deletion or generic relationship repair.
- Broader Operational Recovery / DR subsystem.

The supported executable surface described here is the package invocation. GUI
governance is unchanged: a functioning GUI remains mandatory for Version 1.0 release
readiness and outside the current Gate-3 closure scope.

Version 1.0 remains PRE-RELEASE; Gate 3 remains NOT PASSED and Gate 4 remains FUTURE.
Required live Services validation remains incomplete. This guide neither claims that
validation has completed nor changes any Release acceptance status. No Slice 11 is
allocated. Separate live-validation authorisation and release approval remain required.

---

# 15. Troubleshooting Boundaries

Fixed reports deliberately omit detailed diagnostics. Use the report category to
select an external check without treating it as proof of a particular cause.

| Observation | Operator check |
|-------------|----------------|
| `Configuration error.` | Inspect the selected file, TOML schema, documented path-resolution rules, required directories and runtime credential setup without displaying the PAT. |
| `Application logging error.` | Check the configured logging directory and logfile access. There is no fallback destination. |
| `Documentation processing error.` | Check the dedicated source directory and Markdown against the Documentation Input Specification. |
| HTTP 401 message | Verify credential setup through approved operational means; the report alone does not identify expiration, revocation or another cause. |
| HTTP 403 message | Verify the approved PAT scopes and project/Area Path permissions externally; the application does not name the missing permission or escalate access. |
| HTTP 429 message | Manage waiting and any decision to invoke again externally. The application supplies no Retry-After diagnostic and does not retry or back off. |
| `Conflicting reused child relationship error.` | Inspect the actual Azure DevOps parent relationships before deciding any authorised operator action. The application will not remove or replace conflicting relationships. |
| `Azure DevOps error.` or another handled failure | Review approved prerequisites and relevant remote state externally before deciding a later normal invocation; do not assume there was no persistence. |
| Missing SUMMARY or COMPLETION | Check process outcome, configured threshold and logfile availability. INFO filtering or delivery failure can suppress records; absence does not establish absence of mutation. |

Do not introduce an unapproved repair or repeated mutation merely to obtain a successful
run. These checks do not promise diagnostics or automatic recovery beyond the approved
behaviour. Keep any shared evidence within the restrictions below.

---

# 16. Security Considerations

Keep `AZDO_PAT` runtime-only. Do not place PAT values in TOML, command arguments, source
control, generated backlog content, screenshots, logs or evidence. Never include derived
Authorization headers or credential-bearing request dumps in troubleshooting material.

Use synthetic, non-secret evidence where possible. Inspect material before sharing it:
operational evidence must not expose PAT values, Authorization material, request/response
bodies, exception details, tracebacks or other prohibited diagnostics. Safe references
to an environment or input do not authorise raw diagnostic capture.

Runtime reports also exclude source titles/content, source identities/digests, local
paths, URLs, organisation/project/configuration values and remote IDs. The approved
summary count does not permit additional dynamic diagnostics. Do not infer that a safe
application report makes an accompanying screenshot or manually captured extract safe.

Use the least-privilege scopes and permissions in Section 5. The generator does not
switch credentials or elevate privileges after failure. Handle any external inspection
or operator action within its separately authorised scope.
