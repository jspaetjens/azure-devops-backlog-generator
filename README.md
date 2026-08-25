# azure-devops-backlog-generator

## Local development setup

Use Windows PowerShell and Python 3.14. `.venv` is the canonical local virtual
environment name; activate it before following the commands below. The project
does not rely on globally installed Ruff or pytest.

Create the virtual environment:

```powershell
py -3.14 -m venv .venv
```

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the project and development dependencies. Development dependencies are
defined in `pyproject.toml`; `.[dev]` installs the project in editable mode
together with those dependencies.

```powershell
python -m pip install -e ".[dev]"
```

Run the required quality checks:

```powershell
python -m ruff check .
python -m pytest
```
