# Codex Working Instructions

## Authority and documentation

- Project documentation is authoritative. Respect all approved specifications,
  architecture, standards, contracts and documented decisions.
- Follow `.ai/AI-Working-Agreement.md`. When it conflicts with project
  documentation, project documentation takes precedence unless explicitly
  agreed otherwise.
- Do not silently reinterpret, replace or extend documented requirements.

## Scope and requirements

- Work only on the requested task. Keep changes small, reviewable and
  independently testable.
- Do not add unrelated refactoring, opportunistic improvements or functionality
  that merely seems useful.
- Do not invent business rules, configuration, validation behaviour, API
  contracts, defaults or architectural decisions. Infer existing behaviour only
  where code, tests or authoritative documentation clearly establish it.
- If implementation depends on an undefined requirement, stop that portion and
  report the blocker clearly.

## Python, architecture and security

- This project targets Python 3.14.x. Use the project virtual environment and
  existing tooling; do not rely on globally installed command-line tools.
- Follow the documented package structure, naming conventions, component
  responsibilities and existing patterns. Avoid unnecessary complexity and
  premature abstractions.
- Do not add dependencies unless the task requires them and their justification
  is explicit.
- Never expose or commit secrets, tokens, credentials or sensitive configuration
  in code, logs, tests, examples or diagnostics.

## Testing and quality checks

- Add or update appropriate automated tests for changed behaviour. Preserve and
  do not weaken, delete or bypass existing tests.
- Follow `docs/06-Testing.md`; prefer tests of meaningful external behaviour
  where practical.
- Run checks with module invocation:

  ```powershell
  python -m ruff check .
  python -m pytest
  ```

  These commands use the Ruff lint and pytest configuration in `pyproject.toml`.
  If a required check cannot run, state why.

## Change safety and Git

- Before handoff, inspect the diff and confirm no unrelated files changed.
  Preserve existing line endings and formatting where practical.
- Do not commit generated artefacts, temporary files, coverage data, virtual
  environments, caches, IDE artefacts or other unintended files.
- Do not independently merge branches, push, create or merge pull requests,
  rewrite history, force-push or commit. Make a commit only when the user
  explicitly requests it.
- Follow the Development Standards Git workflow: feature branch, Pull Request,
  then `main`; use Conventional Commits when a commit is requested.

## Standard task handoff

For every implementation task, provide a concise handoff with:

1. Summary of what was implemented.
2. Files changed.
3. Tests added or changed.
4. Ruff command(s) executed and result.
5. Pytest command executed and result.
6. Documentation or specification conflicts discovered.
7. Unresolved questions or blockers.
8. Output of `git status --short`.

Do not dump complete source files unless requested.
