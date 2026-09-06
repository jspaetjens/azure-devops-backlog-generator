"""Execute the application with controlled process termination."""

from azure_devops_backlog_generator.main import run_process

if __name__ == "__main__":
    raise SystemExit(run_process())
