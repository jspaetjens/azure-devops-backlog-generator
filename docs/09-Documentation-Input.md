# Azure DevOps Backlog Generator

# Documentation Input Specification

> *This document defines the Version 1.0 source-document discovery, Markdown parsing, hierarchy interpretation, title extraction, validation, deterministic ordering and source-side traceability contract for the Azure DevOps Backlog Generator.*

**Version:** 0.2

**Status:** Approved Baseline

**Last Updated:** 2026-08-21

**Target Release:** v1.0.0

**License:** MIT

**Author:** Jack Spaetjens

---

# Version History

| Version | Date | Status | Author | Description |
|----------|------------|-------------------|-----------------|------------------------------------------------|
| 0.1 | 2026-08-20 | Approved Baseline | Jack Spaetjens | Initial Documentation Input Specification. |
| 0.2 | 2026-08-21 | Approved Baseline | Jack Spaetjens | Standardised the Approval section to remain valid across Draft and Approved Baseline states. |

---

# Table of Contents

- [Azure DevOps Backlog Generator](#azure-devops-backlog-generator)
- [Documentation Input Specification](#documentation-input-specification)
- [Version History](#version-history)
- [Table of Contents](#table-of-contents)
- [1. Introduction](#1-introduction)
- [2. Purpose](#2-purpose)
- [3. Scope and Authority](#3-scope-and-authority)
- [4. Source Directory](#4-source-directory)
- [5. File Discovery and Encoding](#5-file-discovery-and-encoding)
- [6. Normative Markdown Basis](#6-normative-markdown-basis)
- [7. Semantic Hierarchy](#7-semantic-hierarchy)
  - [7.1 Hierarchy Grammar](#71-hierarchy-grammar)
  - [7.2 Nested and Excluded Markdown Contexts](#72-nested-and-excluded-markdown-contexts)
  - [7.3 Hierarchy Validation](#73-hierarchy-validation)
- [8. Title Extraction](#8-title-extraction)
- [9. Item Boundaries](#9-item-boundaries)
- [10. Duplicate Sibling Titles](#10-duplicate-sibling-titles)
- [11. Deterministic File Ordering](#11-deterministic-file-ordering)
- [12. Source Identity and Traceability](#12-source-identity-and-traceability)
- [13. Validation Behaviour](#13-validation-behaviour)
- [14. Explicitly Unresolved Contracts](#14-explicitly-unresolved-contracts)
- [15. Approval](#15-approval)

---

# 1. Introduction

This document defines the Version 1.0 input contract for approved backlog-input Markdown documents.

It establishes the rules for discovering source documents, interpreting their Markdown structure, deriving the fixed Scrum work-item hierarchy, validating source input, determining processing order and maintaining source-side traceability.

---

# 2. Purpose

The purpose of this specification is to provide a deterministic and reusable contract for translating approved backlog-input Markdown documents into source work-item structures.

This document is the authoritative Version 1.0 specification for source-document discovery, parsing, hierarchy interpretation, title extraction, validation, deterministic ordering and source-side identity.

---

# 3. Scope and Authority

This specification applies only to Version 1.0 backlog-input Markdown documents used for backlog generation.

It supplements the approved Product Requirements Document, Software Architecture Document, Testing Strategy and Configuration Specification without changing their approved product, architecture, testing or configuration scope.

The source hierarchy defined by this specification is fixed to the Version 1.0 Scrum work-item model: Epic, Feature, Product Backlog Item and Task.

This specification does not introduce Theme, additional work-item types, configurable hierarchy mappings, configurable grammar, parser-library configuration, source identifiers, recursive discovery, cross-file hierarchy or new configuration parameters.

---

# 4. Source Directory

`documentation.source_directory` shall identify a dedicated directory containing only approved backlog-input Markdown documents.

Every discovered matching Markdown file shall:

- be generator input;
- be approved project documentation before generation; and
- conform completely to this specification.

The source directory shall not be:

- the general project `docs/` directory;
- a mixed directory containing arbitrary Markdown documents; or
- a recursive documentation tree.

This specification does not introduce a configuration parameter beyond `documentation.source_directory`.

---

# 5. File Discovery and Encoding

Only direct regular files inside `documentation.source_directory` shall be considered as backlog-input files.

File discovery shall follow these rules:

- Directory traversal shall not be recursive.
- Symbolic links shall not be followed and shall not be input files.
- The `.md` extension shall be matched case-insensitively.
- At least one matching input file shall be present.

Input files shall use UTF-8 encoding. A UTF-8 byte order mark is permitted and shall be ignored as an encoding marker.

The following conditions shall be validation failures:

- no matching Markdown input files;
- an unreadable matching file; or
- invalid UTF-8 in a matching file.

---

# 6. Normative Markdown Basis

Version 1.0 backlog-input documents shall use CommonMark 0.31.2 as the normative Markdown syntax basis.

Parsing semantics shall be determined using CommonMark 0.31.2 block and inline nodes rather than naive line-prefix matching.

No Markdown extensions are part of the Version 1.0 input contract unless explicitly defined by this specification.

An implementation parser shall conform to CommonMark 0.31.2 and to the additional restrictions and validation rules defined by this specification. This specification shall not prescribe a specific Python Markdown parser library.

For this specification, a top-level Markdown node is a node that is a direct child of the parsed document root.

---

# 7. Semantic Hierarchy

Only top-level ATX heading nodes shall participate in the Version 1.0 backlog hierarchy.

## 7.1 Hierarchy Grammar

The fixed semantic hierarchy is:

| Top-level ATX heading level | Source work-item type |
|-----------------------------|-----------------------|
| `#` | Epic |
| `##` | Feature |
| `###` | Product Backlog Item |
| `####` | Task |

Theme does not exist in the Version 1.0 source grammar.

Top-level ATX heading nodes shall be reserved exclusively for semantic backlog hierarchy. A top-level ATX heading deeper than level 4 shall be a validation failure. A top-level setext heading shall be a validation failure.

## 7.2 Nested and Excluded Markdown Contexts

ATX headings or heading-like text that CommonMark 0.31.2 does not classify as top-level ATX heading nodes shall not participate in backlog hierarchy and shall be permitted as ordinary item content.

This includes content occurring in:

- fenced code blocks;
- block quotes;
- list-item or other container contexts;
- HTML blocks; and
- other contexts that do not produce a top-level ATX heading node.

Nested setext headings shall be ordinary content and shall not be hierarchy nodes.

The prohibition on non-semantic headings applies specifically to top-level heading nodes. Top-level ATX heading nodes are reserved exclusively for the semantic backlog hierarchy.

## 7.3 Hierarchy Validation

Hierarchy shall be inferred only from the permitted top-level ATX headings in source order.

The following rules shall apply:

- Hierarchy levels shall not be skipped.
- A Feature shall require an active parent Epic.
- A Product Backlog Item shall require an active parent Feature.
- A Task shall require an active parent Product Backlog Item.
- Sibling items at the same hierarchy level shall share the current valid parent.
- Each source file shall contain a self-contained hierarchy.
- Cross-file parent-child relationships shall be prohibited.

---

# 8. Title Extraction

Each semantic heading shall define the source title for its corresponding source item.

Visible title text shall be derived from the heading's CommonMark inline content as follows:

- Plain text shall remain text.
- Emphasis and strong-emphasis formatting markers shall be removed while visible text remains.
- Code spans shall contribute visible code text.
- Links shall contribute link text only.
- Link destinations and link titles shall be excluded.
- Character and entity references shall contribute their decoded visible text according to CommonMark semantics.
- Escaped punctuation shall contribute the visible escaped character.
- Images shall contribute alt text only.
- Inline HTML in a semantic heading shall be a validation failure.

After inline extraction, the title shall be normalised by trimming leading and trailing whitespace and collapsing each internal Unicode whitespace run to one ASCII space.

The normalised title shall not be empty and shall not exceed 255 characters. Titles shall never be truncated.

Version 1.0 shall not introduce explicit source identifiers or insert identifiers into Azure DevOps titles.

---

# 9. Item Boundaries

Each semantic heading shall define one source item.

The item's direct body shall:

- begin after its semantic heading;
- end before the next semantic heading of the same or higher hierarchy level, or at end of file;
- exclude all child semantic headings; and
- exclude all child-item content.

This specification does not define Description mapping from the direct body.

---

# 10. Duplicate Sibling Titles

Within one source file and one parent hierarchy node, siblings of the same work-item type shall have unique normalised titles.

Duplicate normalised sibling titles shall be validation failures.

The same normalised title under different parents shall be permitted.

---

# 11. Deterministic File Ordering

For every discovered filename, processing order shall be determined as follows:

1. Normalise the filename to Unicode NFC.
2. Use `casefold()` of the NFC-normalised filename as the primary sort key.
3. Use the original-case NFC-normalised filename as the secondary sort key.
4. Compare sort keys using ordinal Unicode code-point ordering.
5. Locale-specific collation shall not be used.

Items within each file shall retain source order.

Processing order shall control processing only. It shall not imply Azure DevOps rank, priority, state, iteration or business-priority semantics.

---

# 12. Source Identity and Traceability

The deterministic Version 1.0 source-side identity shall consist of:

```text
canonical relative file path
+
complete normalised semantic heading hierarchy
```

The canonical relative file path shall:

- be relative to `documentation.source_directory`;
- use Unicode NFC normalisation;
- use `/` as the canonical separator; and
- preserve original filename case.

The semantic heading hierarchy shall use the normalised titles defined by this specification.

Rename sensitivity is explicitly accepted. Changing a filename or a semantic heading shall change the source identity. Version 1.0 shall not track renames.

This source identity does not define Azure DevOps WIQL duplicate-detection or query semantics.

---

# 13. Validation Behaviour

All source validation shall occur before persistent backlog generation. A source-validation failure shall prevent persistent generation.

At minimum, the following shall be source-validation failures:

- no matching input files;
- an unreadable matching file;
- invalid UTF-8;
- a top-level setext heading;
- a top-level ATX heading deeper than level 4;
- an invalid hierarchy level;
- an orphan Feature;
- an orphan Product Backlog Item;
- an orphan Task;
- an empty normalised title;
- a title longer than 255 characters;
- a duplicate normalised sibling title;
- inline HTML in a semantic heading;
- a cross-file hierarchy dependency; or
- any discovered input document that violates this specification.

This specification does not define numeric exit codes.

---

# 14. Explicitly Unresolved Contracts

This specification does not define:

- Description source syntax or mapping;
- Acceptance Criteria source syntax or mapping;
- Tags source syntax or taxonomy;
- Markdown-to-HTML body conversion;
- Azure DevOps JSON Patch payloads;
- parent-child relation payload semantics;
- WIQL duplicate-detection or query semantics;
- PAT authentication transport;
- retry or rate-limit behaviour; or
- ordinary work-item update semantics.

These areas shall not be inferred from this specification.

---

# 15. Approval

Approval of a document version requires:

- Completion of the editorial review.
- Approval of that document version.
- Creation of the corresponding Approved Baseline.
- Commit to the project repository using the agreed Git workflow.

The document metadata and Version History record whether the current version has completed this approval process.

Subsequent modifications shall follow the established documentation governance process and be recorded through Version History.
