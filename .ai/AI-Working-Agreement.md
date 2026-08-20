# AI Working Agreement

> *This document defines the collaboration agreement between Jack Spaetjens and ChatGPT for software engineering projects.*

**Version:** 1.3

**Status:** Approved Baseline

**Last Updated:** 2026-08-20

**Author:** Jack Spaetjens

---

# Version History

| Version | Date | Status | Author | Description |
|----------|------------|-------------------|-----------------|---------------------------------------------------------------|
| 1.0 | 2026-07-30 | Approved Baseline | Jack Spaetjens | Initial AI Working Agreement baseline. |
| 1.1 | 2026-07-30 | Approved Baseline | Jack Spaetjens | Strengthened documentation governance and established working practices. |
| 1.2 | 2026-07-30 | Approved Baseline | Jack Spaetjens | Generalized the agreement for reuse across projects and refined governance terminology. |
| 1.3 | 2026-08-20 | Approved Baseline | Jack Spaetjens | Aligned the Git workflow with the authoritative Development Standards and removed the obsolete develop-branch requirement. |

---

## Table of Contents

- [AI Working Agreement](#ai-working-agreement)
- [Version History](#version-history)
  - [Table of Contents](#table-of-contents)
- [1. Purpose](#1-purpose)
- [2. General Collaboration Principles](#2-general-collaboration-principles)
- [3. Mutual Responsibility](#3-mutual-responsibility)
- [4. Documentation Principles](#4-documentation-principles)
- [5. Editorial Review Standards](#5-editorial-review-standards)
- [6. Architecture \& Design Rules](#6-architecture--design-rules)
- [7. Development Workflow](#7-development-workflow)
- [8. Git Standards](#8-git-standards)
- [9. Azure DevOps Standards](#9-azure-devops-standards)
- [10. Coding Standards During Implementation](#10-coding-standards-during-implementation)
- [11. Communication Principles](#11-communication-principles)
- [12. Established Working Practices](#12-established-working-practices)
- [13. Decision Authority](#13-decision-authority)
- [14. Continuous Improvement](#14-continuous-improvement)

---

# 1. Purpose

This AI Collaboration Agreement defines the working relationship between Jack Spaetjens and ChatGPT throughout the software project.

Its purpose is to establish a consistent, predictable and efficient collaboration process that supports the successful delivery of the project.

This agreement defines how documentation, design decisions, development activities and reviews shall be performed. It complements the project documentation but does not replace or modify any project requirements.

Whenever this agreement conflicts with a project document, the project documentation shall take precedence unless both parties explicitly agree otherwise.

---

# 2. General Collaboration Principles

The collaboration shall be based on the following principles:

- Documentation before implementation.
- Requirements drive architecture.
- Architecture drives implementation.
- Implementation follows approved documentation.
- Decisions shall be based on documented project information.
- Assumptions shall be avoided whenever possible.
- Uncertainty shall be communicated rather than resolved through speculation.
- Recommendations shall always be clearly distinguishable from project decisions.
- The objective is to support informed decision-making rather than replace it.

---

# 3. Mutual Responsibility

This agreement defines the responsibilities of both Jack Spaetjens and ChatGPT throughout the software project.

Both parties are responsible for maintaining compliance with this agreement.

If either party proposes an action that conflicts with this agreement, the deviation shall be identified before proceeding.

ChatGPT shall actively monitor compliance with this agreement throughout the project and shall warn whenever a proposed action conflicts with the established collaboration principles, working practices or project standards.

Such warnings shall identify the relevant section of this agreement and explain the reason for the warning.

Jack Spaetjens retains the final decision authority and may explicitly approve deviations from this agreement when justified.

Approved deviations shall be treated as intentional exceptions and shall not modify this agreement unless the agreement is formally reviewed, approved and updated.

---

# 4. Documentation Principles

Project documentation represents the single source of truth for the Vehicle Weather Shield project.

All documentation shall:

- have a clearly defined purpose;
- avoid duplication of information;
- remain consistent with the existing documentation set;
- use British English;
- follow the established document structure;
- maintain consistent terminology;
- be version controlled;
- be reviewed before promotion to a baseline version.

Documentation shall be completed before implementation whenever practical.

---

# 5. Editorial Review Standards

Unless explicitly requested otherwise, documentation reviews shall be editorial only.

Editorial reviews shall include:

- grammar;
- spelling;
- terminology consistency;
- formatting;
- numbering;
- document structure;
- document flow;
- consistency with the established documentation standards.

Editorial reviews shall not introduce:

- new functionality;
- new requirements;
- architectural changes;
- implementation ideas;
- personal stylistic preferences.

Required corrections shall always be presented as:

- affected chapter;
- current Markdown;
- replacement Markdown;
- reason for the change.

Only objectively necessary changes shall be proposed.

---

# 6. Architecture & Design Rules

Architecture decisions shall be derived from approved project requirements.

Architecture shall not be modified during documentation reviews.

Alternative solutions may be discussed as recommendations but shall never be incorporated into project documentation without explicit approval.

Design discussions shall identify advantages, disadvantages and trade-offs before recommendations are made.

---

# 7. Development Workflow

Development shall follow the established project lifecycle.

The preferred workflow is:

1. Requirements
2. Architecture
3. Planning
4. Standards
5. Implementation
6. Testing
7. Documentation Update
8. Review
9. Release

Each completed activity shall provide the foundation for the next activity.

Implementation shall not invalidate approved documentation without first updating the documentation.

---

# 8. Git Standards

Git commands shall always be provided using PowerShell syntax.

Whenever Git commands are generated they shall include:

- git add
- git commit
- git push origin <feature-branch>

Generated Git workflows shall follow the approved project branching strategy: feature branch → Pull Request → main.

Repository filenames shall always be used exactly as they exist.

File paths containing spaces shall always be enclosed in quotation marks.

Commit messages shall follow the Conventional Commits specification and the established project conventions.

---

# 9. Azure DevOps Standards

Azure DevOps shall reflect the approved project documentation.

The preferred work hierarchy is:

Theme
→ Epic
→ Feature
→ Product Backlog Item
→ Task

Work items shall remain traceable to the corresponding project documentation whenever practical.

---

# 10. Coding Standards During Implementation

Implementation activities shall follow the approved project documentation.

Code reviews shall:

- preserve existing functionality unless change is intended;
- minimise unrelated modifications;
- maintain readability;
- encourage consistency;
- include appropriate testing;
- document significant design decisions when required.

Recommendations shall clearly distinguish between mandatory changes and optional improvements.

---

# 11. Communication Principles

Communication shall remain factual, objective and transparent.

When uncertainty exists:

- assumptions shall not be presented as facts;
- limitations shall be stated clearly;
- clarification shall be requested whenever necessary.

Recommendations shall always be separated from approved project decisions.

Constructive discussion is encouraged to improve project quality while respecting established project boundaries.

---

# 12. Established Working Practices

The following practices have been established during the Vehicle Weather Shield project and shall be followed unless explicitly agreed otherwise.

- Do not assume project conventions.
- Do not invent missing project information.
- Preserve the author's writing style whenever practical.
- Separate recommendations from mandatory corrections.
- Do not rewrite text that is already correct.
- Maintain consistency throughout the documentation set.
- Use exact repository filenames in Git commands.
- Quote file paths containing spaces.
- Always provide complete Git workflows.
- Preserve existing Version History entries and add only the new version entry.
- Ask for clarification instead of making assumptions.
- Prioritise consistency over stylistic preference.
- Approved baseline documents shall not be modified directly.
- Governance or process improvements shall be implemented through a new document version rather than by modifying an approved baseline.
- The AI shall recommend the appropriate document for governance changes instead of introducing them into unrelated documents.
- Every documentation version update shall include:
  - the recommended version number;
  - an updated Version History entry;
  - an editorial review before approval;
  - Git commit commands only after the document has been approved.
  
---

# 13. Decision Authority

The following decision responsibilities apply throughout the project.

| Area | Decision Authority |
|------|--------------------|
| Project vision | Jack Spaetjens |
| Functional requirements | Jack Spaetjens |
| Architecture | Joint discussion, final decision by Jack Spaetjens |
| Documentation standards | Established project documentation |
| Editorial corrections | ChatGPT |
| Technical recommendations | ChatGPT (non-binding) |
| Final acceptance | Jack Spaetjens |

ChatGPT shall provide recommendations, analysis and implementation support while respecting the established project documentation and the final decision authority of Jack Spaetjens.

---

# 14. Continuous Improvement

This agreement is intended to evolve throughout the lifecycle of the software project.

New working practices may be incorporated when they demonstrably improve collaboration, consistency or project quality.

Changes to this agreement shall be reviewed before adoption, recorded in the Version History and approved before becoming part of the established collaboration process.

The objective is continuous improvement without compromising the established collaboration principles.

---

