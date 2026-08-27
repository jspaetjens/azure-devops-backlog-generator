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

## Configuration bootstrap

Copy the tracked configuration template to the default local runtime path:

```powershell
Copy-Item -LiteralPath "config\config.example.toml" -Destination "config\config.toml"
```

Edit `config/config.toml` with the required non-secret Azure DevOps and documentation
values. The application uses `config/config.toml` as its default configuration path.

Set `AZDO_PAT` separately as an environment variable. Do not store Personal Access Tokens
in TOML configuration files.

Run the required quality checks:

```powershell
python -m ruff check .
python -m pytest
```
