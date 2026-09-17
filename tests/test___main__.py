"""Package execution adapter tests, including isolated child adapter harnesses."""

import importlib
import json
import os
import runpy
import subprocess
import sys
import textwrap
from collections.abc import Iterator
from pathlib import Path
from unittest.mock import Mock

import pytest

import azure_devops_backlog_generator as package
import azure_devops_backlog_generator.main as main_module

_PACKAGE_NAME = "azure_devops_backlog_generator"
_ADAPTER_NAME = f"{_PACKAGE_NAME}.__main__"


@pytest.fixture
def isolated_adapter_cache() -> Iterator[pytest.MonkeyPatch]:
    """Restore both module cache entries and the parent's adapter attribute."""
    with pytest.MonkeyPatch.context() as patch:
        patch.delitem(sys.modules, _ADAPTER_NAME, raising=False)
        patch.delattr(package, "__main__", raising=False)
        # Record absent states too: imports can populate these during the test.
        patch.setitem(sys.modules, _ADAPTER_NAME, None)
        patch.delitem(sys.modules, _ADAPTER_NAME)
        patch.setattr(package, "__main__", None, raising=False)
        patch.delattr(package, "__main__")
        yield patch


@pytest.fixture
def forbidden_direct_calls(monkeypatch: pytest.MonkeyPatch) -> tuple[Mock, Mock]:
    main = Mock(side_effect=AssertionError("Adapter must not call main directly"))
    bootstrap = Mock(side_effect=AssertionError("Adapter must not call bootstrap directly"))
    monkeypatch.setattr(main_module, "main", main)
    monkeypatch.setattr(main_module, "coordinate_application_bootstrap", bootstrap)
    return main, bootstrap


@pytest.mark.parametrize("module_name", [_PACKAGE_NAME, _ADAPTER_NAME])
def test_ordinary_import_does_not_execute_application(
    module_name: str,
    isolated_adapter_cache: pytest.MonkeyPatch,
    forbidden_direct_calls: tuple[Mock, Mock],
    capsys: pytest.CaptureFixture[str],
    caplog: pytest.LogCaptureFixture,
) -> None:
    run_process = Mock(side_effect=AssertionError("Import must not call run_process"))
    isolated_adapter_cache.setattr(main_module, "run_process", run_process)
    if module_name == _PACKAGE_NAME:
        isolated_adapter_cache.delitem(sys.modules, _PACKAGE_NAME)

    imported = importlib.import_module(module_name)

    assert imported.__name__ == module_name
    run_process.assert_not_called()
    for call in forbidden_direct_calls:
        call.assert_not_called()
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""
    assert caplog.records == []


@pytest.mark.parametrize("result", [0, 1])
def test_executable_guard_terminates_with_exact_controlled_result(
    result: int,
    isolated_adapter_cache: pytest.MonkeyPatch,
    forbidden_direct_calls: tuple[Mock, Mock],
    capsys: pytest.CaptureFixture[str],
    caplog: pytest.LogCaptureFixture,
) -> None:
    run_process = Mock(return_value=result)
    isolated_adapter_cache.setattr(main_module, "run_process", run_process)

    with pytest.raises(SystemExit) as raised:
        runpy.run_module(_PACKAGE_NAME, run_name="__main__")

    assert raised.value.code == result
    assert type(raised.value.code) is int
    run_process.assert_called_once_with()
    for call in forbidden_direct_calls:
        call.assert_not_called()
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""
    assert caplog.records == []


def test_executable_guard_propagates_same_unexpected_exception(
    isolated_adapter_cache: pytest.MonkeyPatch,
    forbidden_direct_calls: tuple[Mock, Mock],
    capsys: pytest.CaptureFixture[str],
    caplog: pytest.LogCaptureFixture,
) -> None:
    error = RuntimeError("adapter sentinel")
    run_process = Mock(side_effect=error)
    isolated_adapter_cache.setattr(main_module, "run_process", run_process)

    with pytest.raises(RuntimeError) as raised:
        runpy.run_module(_PACKAGE_NAME, run_name="__main__")

    assert raised.value is error
    run_process.assert_called_once_with()
    for call in forbidden_direct_calls:
        call.assert_not_called()
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""
    assert caplog.records == []


@pytest.fixture
def child_environment(tmp_path: Path) -> dict[str, str]:
    environment = {key: os.environ[key] for key in ("SystemRoot", "WINDIR") if key in os.environ}
    environment.update(
        PYTHONPATH=str(Path(__file__).resolve().parents[1] / "src"),
        PYTHONNOUSERSITE="1",
        PYTHONDONTWRITEBYTECODE="1",
        PYTHONIOENCODING="utf-8",
        TEMP=str(tmp_path),
        TMP=str(tmp_path),
        TMPDIR=str(tmp_path),
    )
    return environment


def _run_child(
    arguments: list[str], tmp_path: Path, environment: dict[str, str]
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(Path(sys.executable).absolute()), "-B", *arguments],
        cwd=tmp_path,
        env=environment,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
        timeout=30,
    )


def test_real_package_subprocess_reports_missing_configuration(
    tmp_path: Path, child_environment: dict[str, str]
) -> None:
    missing_config = tmp_path / "missing-config.toml"
    assert not missing_config.exists()

    result = _run_child(
        ["-m", _PACKAGE_NAME, "--config-file", str(missing_config)],
        tmp_path,
        child_environment,
    )

    assert result.returncode == 1
    assert result.stdout == ""
    assert result.stderr == "Configuration error.\n"
    assert not missing_config.exists()
    assert not list(tmp_path.rglob("azure-devops-backlog-generator.log"))


def test_adapter_boundary_success_subprocess(
    tmp_path: Path, child_environment: dict[str, str]
) -> None:
    """Validate adapter termination, not a successful application E2E run."""
    script = (
        "import runpy\n"
        "import azure_devops_backlog_generator.main as main_module\n"
        "def successful_run_process():\n"
        "    return 0\n"
        "main_module.run_process = successful_run_process\n"
        'runpy.run_module("azure_devops_backlog_generator", run_name="__main__")\n'
    )

    result = _run_child(["-c", script], tmp_path, child_environment)

    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr == ""


def test_adapter_boundary_unexpected_exception_subprocess(
    tmp_path: Path, child_environment: dict[str, str]
) -> None:
    """Characterise native termination without fixing traceback details."""
    script = (
        "import runpy\n"
        "import azure_devops_backlog_generator.main as main_module\n"
        'error = RuntimeError("adapter sentinel")\n'
        "def unexpected_run_process():\n"
        "    raise error\n"
        "main_module.run_process = unexpected_run_process\n"
        'runpy.run_module("azure_devops_backlog_generator", run_name="__main__")\n'
    )

    result = _run_child(["-c", script], tmp_path, child_environment)

    assert result.returncode != 0
    assert result.stdout == ""
    assert result.stderr != ""


def test_package_maps_real_unexpected_fallback_to_system_exit_one(
    isolated_adapter_cache: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    loader = Mock(side_effect=RuntimeError("SYNTHETIC_PRIVATE_EXCEPTION"))
    isolated_adapter_cache.setattr(main_module, "load_configuration_from_cli", loader)

    with pytest.raises(SystemExit) as raised:
        runpy.run_module(_PACKAGE_NAME, run_name="__main__")

    assert type(raised.value.code) is int
    assert raised.value.code == 1
    loader.assert_called_once()
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "Unexpected application error.\n"


@pytest.mark.parametrize("logging_active", [False, True], ids=["pre-init", "post-init"])
def test_package_subprocess_real_fallback_suppresses_unexpected_details_and_traceback(
    tmp_path: Path,
    child_environment: dict[str, str],
    logging_active: bool,
) -> None:
    """Run the real package adapter and fallback with isolated lower collaborators."""
    sentinels = (
        "SYNTHETIC_PAT", "Authorization: SYNTHETIC_AUTH",
        "C:\\SYNTHETIC_PRIVATE\\config.toml", "SYNTHETIC_ORG/SYNTHETIC_PROJECT",
        "https://example.invalid/SYNTHETIC_URL", "SYNTHETIC_SOURCE_USER_CONTENT",
        "SYNTHETIC_EXCEPTION_MESSAGE", "SYNTHETIC_CAUSE", "SYNTHETIC_CONTEXT",
    )
    script = (
        "import runpy\n"
        "from pathlib import Path\n"
        "from azure_devops_backlog_generator.config.models import (\n"
        "    Configuration, AzureDevOpsConfig, DocumentationConfig, LoggingConfig\n"
        ")\n"
        "import azure_devops_backlog_generator.main as main_module\n"
        f"error = RuntimeError({sentinels!r})\n"
        "error.__cause__ = ValueError('SYNTHETIC_CAUSE')\n"
        "error.__context__ = ValueError('SYNTHETIC_CONTEXT')\n"
        "def fail(_):\n"
        "    raise error\n"
        "def configuration(_):\n"
        "    return Configuration(\n"
        "        azure_devops=AzureDevOpsConfig(organization='SYNTHETIC_ORG',\n"
        "                                     project='SYNTHETIC_PROJECT'),\n"
        "        documentation=DocumentationConfig(source_directory=Path('.')),\n"
        "        logging=LoggingConfig(level='INFO', log_directory=Path('.')),\n"
        "        personal_access_token='SYNTHETIC_PAT',\n"
        "    )\n"
        "main_module.load_configuration_from_cli = "
        f"{'configuration' if logging_active else 'fail'}\n"
        "main_module.coordinate_application_run = fail\n"
        'runpy.run_module("azure_devops_backlog_generator", run_name="__main__")\n'
    )

    result = _run_child(["-c", script], tmp_path, child_environment)

    assert result.returncode == 1
    assert result.stdout == ""
    assert result.stderr == "Unexpected application error.\n"
    log_file = tmp_path / "azure-devops-backlog-generator.log"
    if logging_active:
        contents = log_file.read_text(encoding="utf-8")
        assert [line.split(" ", 1)[1] for line in contents.splitlines()] == [
            "INFO azure_devops_backlog_generator Application run started.",
            "CRITICAL azure_devops_backlog_generator Unexpected application error.",
        ]
        assert list(tmp_path.iterdir()) == [log_file]
    else:
        contents = ""
        assert list(tmp_path.iterdir()) == []
    for sentinel in (*sentinels, "RuntimeError", "ValueError", "Traceback"):
        assert sentinel not in result.stderr + contents


@pytest.mark.parametrize(
    ("scenario", "http_message"),
    [(scenario, None) for scenario in ("success", "empty", "partial-rerun", "conflict-rerun")]
    + [(f"http-{status}-{stage}", message)
       for status, message in (
           (401, "Azure DevOps authentication failed."),
           (403, "Azure DevOps authorisation failed."),
           (429, "Azure DevOps rate limit reached."),
       ) for stage in ("preflight", "patch")],
)
def test_package_summary_with_real_parsing_generator_and_controlled_transport(
    tmp_path: Path, child_environment: dict[str, str], scenario: str,
    http_message: str | None,
) -> None:
    """Exercise the supported application, substituting only JSON transport."""
    source = tmp_path / "SYNTHETIC_SOURCE"
    source.mkdir()
    markdown = (
        "# SYNTHETIC_EPIC\nSYNTHETIC_BODY\n"
        "## SYNTHETIC_FEATURE\nSYNTHETIC_REQUEST_CONTENT\n"
        "### SYNTHETIC_PBI\nSYNTHETIC_HIERARCHY\n"
        "#### SYNTHETIC_TASK\nhttps://example.invalid/SYNTHETIC_URL\n"
    )
    for index in range(3 if scenario == "success" or http_message else 1):
        (source / f"input-{index}.md").write_text(
            "Ordinary prose.\n" if scenario == "empty" else markdown, encoding="utf-8",
        )
    config = tmp_path / "SYNTHETIC_CONFIG.toml"
    config.write_text(
        '[azure_devops]\norganization = "SYNTHETIC_ORG"\nproject = "SYNTHETIC_PROJECT"\n'
        '[documentation]\nsource_directory = "SYNTHETIC_SOURCE"\n'
        '[logging]\nlevel = "INFO"\nlog_directory = "logs"\n', encoding="utf-8",
    )
    child_environment["AZDO_PAT"] = "SYNTHETIC_PAT"
    script = textwrap.dedent('''\
        import json
        import runpy
        import sys
        import time
        from pathlib import Path
        from azure_devops_backlog_generator.azure_devops.rest_client import AzureDevOpsRestClient
        from azure_devops_backlog_generator.azure_devops.exceptions import (
            AzureDevOpsHttpError, AzureDevOpsTransportError,
        )

        scenario = sys.argv[1]
        config = sys.argv[2]
        identity_field = "Custom.BacklogGeneratorSourceIdentity"
        items = {}
        parents = {}
        requests = []
        snapshots = []
        outcomes = []
        failures = []
        sleeps = []
        phase = 0

        def forbidden_sleep(seconds):
            sleeps.append(seconds)
            raise AssertionError("Application must not sleep")

        time.sleep = forbidden_sleep

        def transport(self, *, method, path_segments, personal_access_token,
                      query=None, json_body=None, **kwargs):
            assert personal_access_token == "SYNTHETIC_PAT"
            path = tuple(path_segments)
            requests.append([phase, method, list(path), query])
            if failures:
                raise AssertionError("No operation may follow an HTTP failure")
            if scenario.startswith("http-") and (
                (scenario.endswith("preflight") and path[:2] == ("_apis", "projects"))
                or (scenario.endswith("patch") and method == "PATCH")
            ):
                failures.append(len(requests))
                error = AzureDevOpsHttpError(int(scenario.split("-")[1]))
                error.args = ("Authorization: SYNTHETIC_AUTH", "SYNTHETIC_RESPONSE_CONTENT")
                raise error
            if path[:2] == ("_apis", "projects"):
                return {"id": "SYNTHETIC_PROJECT_ID", "name": "SYNTHETIC_PROJECT"}
            if "fields" in path:
                field = path[-1]
                result = {"referenceName": field}
                if field == identity_field:
                    result.update(name="Backlog Generator Source Identity", type="String",
                                  readOnly=False, defaultValue=None, alwaysRequired=False)
                return result
            if "workitemtypes" in path:
                return {"name": path[-1]}
            if path[-1] == "wiql":
                return {"workItems": [
                    {"id": item["id"]} for item in items.values()
                    if item["fields"][identity_field] in json_body["query"]
                ]}
            if path[:3] == ("_apis", "wit", "workitems"):
                if query == {"validateOnly": "true"}:
                    return {}
                if method == "POST":
                    fields = {op["path"].removeprefix("/fields/"): op["value"]
                              for op in json_body}
                    fields.update({"System.TeamProject": "SYNTHETIC_PROJECT",
                                   "System.WorkItemType": path[-1]})
                    item_id = 987650 + len(items)
                    item = {"id": item_id, "rev": 1, "fields": fields,
                            "synthetic_response": "SYNTHETIC_RESPONSE_CONTENT"}
                    items[item_id] = item
                    return item
                item_id = int(path[-1])
                if method == "PATCH":
                    if scenario.endswith("rerun") and phase == 0:
                        raise AzureDevOpsTransportError("Authorization: SYNTHETIC_AUTH")
                    parents[item_id] = int(json_body[1]["value"]["url"].rsplit("/", 1)[1])
                    return {}
                if query == {"$expand": "relations"}:
                    parent = parents.get(item_id)
                    if scenario == "conflict-rerun" and phase == 1:
                        parent = 123456789
                    return {"id": item_id, "rev": 1, "relations": [] if parent is None else [
                        {"rel": "System.LinkTypes.Hierarchy-Reverse",
                         "url": f"https://dev.azure.com/SYNTHETIC_ORG/_apis/wit/workItems/{parent}"}
                    ]}
                return items[item_id]
            raise AssertionError("Unexpected transport operation")

        AzureDevOpsRestClient.send_json_request = transport
        runs = 3 if scenario == "conflict-rerun" else 2 if scenario == "partial-rerun" else 1
        for phase in range(runs):
            sys.argv = ["azure_devops_backlog_generator", "--config-file", config]
            try:
                runpy.run_module("azure_devops_backlog_generator", run_name="__main__")
            except SystemExit as result:
                outcomes.append(result.code)
            snapshots.append({
                "log": Path("logs/azure-devops-backlog-generator.log").read_text(encoding="utf-8"),
                "items": len(items),
            })
        Path("evidence.json").write_text(json.dumps({
            "outcomes": outcomes, "snapshots": snapshots, "requests": requests,
            "failures": failures, "sleeps": sleeps,
            "identities": [item["fields"][identity_field] for item in items.values()],
        }), encoding="utf-8")
        sys.exit(outcomes[-1])
    ''')
    result = _run_child(["-c", script, scenario, str(config)], tmp_path, child_environment)

    evidence = json.loads((tmp_path / "evidence.json").read_text(encoding="utf-8"))
    final_log = evidence["snapshots"][-1]["log"]
    assert evidence["sleeps"] == []
    for sentinel in (
        "SYNTHETIC", "987650", "987651", "123456789", "Authorization", "Traceback",
        str(tmp_path), "https://", "adbg:source-id", *evidence["identities"],
    ):
        assert sentinel not in final_log + result.stdout + result.stderr
    if http_message is not None:
        assert result.returncode == 1
        assert result.stdout == ""
        assert result.stderr == f"{http_message}\n"
        assert evidence["outcomes"] == [1]
        assert type(evidence["outcomes"][0]) is int
        assert evidence["failures"] == [len(evidence["requests"])]
        assert [line.split(" ", 1)[1] for line in final_log.splitlines()] == [
            "INFO azure_devops_backlog_generator Application run started.",
            f"CRITICAL azure_devops_backlog_generator {http_message}",
        ]
        if scenario.endswith("preflight"):
            assert len(evidence["requests"]) == 1
            assert evidence["snapshots"][-1]["items"] == 0
        else:
            assert evidence["requests"][-1][1] == "PATCH"
            assert evidence["snapshots"][-1]["items"] == 2
            assert sum(request[1] == "PATCH" for request in evidence["requests"]) == 1
        assert all(request[1] != "DELETE" for request in evidence["requests"])
        return

    assert result.returncode == 0, result.stderr
    assert result.stdout == ""
    expected_errors = "Azure DevOps error.\n" if scenario.endswith("rerun") else ""
    if scenario == "conflict-rerun":
        expected_errors += "Conflicting reused child relationship error.\n"
    assert result.stderr == expected_errors
    assert evidence["outcomes"] == (
        [1, 1, 0] if scenario == "conflict-rerun" else
        [1, 0] if scenario == "partial-rerun" else [0]
    )
    count = 0 if scenario == "empty" else 12 if scenario == "success" else 4
    summary = f"Execution summary: outcome=success; source_items_processed={count}."
    assert final_log.count("Execution summary:") == 1
    assert [line.split(" ", 1)[1] for line in final_log.splitlines()[-3:]] == [
        "INFO azure_devops_backlog_generator Application run started.",
        f"INFO azure_devops_backlog_generator {summary}",
        "INFO azure_devops_backlog_generator Application run completed successfully.",
    ]
    assert evidence["snapshots"][-1]["items"] == count
    for snapshot in evidence["snapshots"][:-1]:
        assert snapshot["items"] == 2
        assert "Execution summary:" not in snapshot["log"]
        assert "Application run completed successfully." not in snapshot["log"]
    creates = [request for request in evidence["requests"]
               if request[1] == "POST" and request[2][:3] == ["_apis", "wit", "workitems"]
               and request[3] is None]
    assert len(creates) == count
    assert len(evidence["requests"]) > count
