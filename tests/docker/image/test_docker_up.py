# tests/docker/build/test_docker_up.py

from typer.testing import CliRunner
from pathlib import Path
import shutil
import os

from prefiq.cli.cli import commands  # top-level CLI

runner = CliRunner()

def test_docker_up(tmp_path: Path):
    # Copy test docker-compose file to tmp_path
    compose_path = tmp_path / "docker-compose.yml"
    sample_compose = """
version: "3.8"
services:
  hello:
    image: hello-world
    """
    compose_path.write_text(sample_compose)

    # Run the command
    result = runner.invoke(commands, [
        "docker", "up",
        "--path", str(tmp_path)
    ])


    # 👇 Debug info
    print("STDOUT:\n", result.stdout)
    print("STDERR:\n", result.stderr)
    print("Exit Code:", result.exit_code)

    # We don't expect real Docker to run, but we expect it to hit the function
    assert result.exit_code == 0 or result.exit_code == 1  # allow mocked or dry-run fails
    assert "docker-compose up" in result.stdout.lower() or "docker compose up" in result.stdout.lower()
