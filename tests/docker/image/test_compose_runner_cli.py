import pytest
from typer.testing import CliRunner
from prefiq.cli.cli import commands

runner = CliRunner()

def test_docker_up_dryrun_recreate_yes(monkeypatch):
    monkeypatch.setenv("DOCKER_INSECURE_NO_IPTABLES_RAW", "1")

    result = runner.invoke(
        commands,
        [
            "docker", "up",
            "--dryrun",
            "--recreate",
            "--yes",
            "--compose-dir", "./tests/sample_composes",
            "--json-output",
        ],
    )

    assert result.exit_code == 0
    assert "Hai from docker up" in result.output
    assert "previewing compose files" in result.output or "No compose files found." in result.output
