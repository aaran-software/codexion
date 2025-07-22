import pytest
from typer.testing import CliRunner
from prefiq.cli.cli import commands
from prefiq import CPATH

from pathlib import Path


runner = CliRunner()


@pytest.fixture(autouse=True)
def clean_dockerfiles():
    # Cleanup Dockerfiles before and after test
    for f in Path(CPATH.DOCKER_DIR).glob("Dockerfile_testcli_*"):
        f.unlink()
    yield
    for f in Path(CPATH.DOCKER_DIR).glob("Dockerfile_testcli_*"):
        f.unlink()


def test_create_docker_cli():
    result = runner.invoke(commands, ["docker", "create", "testcli_app"])
    assert result.exit_code == 0
    assert "created successfully" in result.output.lower()
    dockerfile = CPATH.DOCKER_DIR / "Dockerfile_testcli_app"
    assert dockerfile.exists()


def test_update_docker_cli():
    dockerfile = CPATH.DOCKER_DIR / "Dockerfile_testcli_update"
    dockerfile.write_text("Dummy content")

    result = runner.invoke(commands, ["docker", "update", "testcli_update"])
    assert result.exit_code == 0
    assert "updated successfully" in result.output.lower()
    assert "ubuntu:24.04" in dockerfile.read_text()


def test_remove_docker_cli():
    dockerfile = CPATH.DOCKER_DIR / "Dockerfile_testcli_remove"
    dockerfile.write_text("Dummy content")

    result = runner.invoke(commands, ["docker", "remove", "testcli_remove"])
    assert result.exit_code == 0
    assert "removed successfully" in result.output.lower()
    assert not dockerfile.exists()


def test_list_docker_cli():
    (CPATH.DOCKER_DIR / "Dockerfile_testcli_list").write_text("# Dummy Dockerfile")
    result = runner.invoke(commands, ["docker", "list"])
    assert result.exit_code == 0
    assert "Dockerfile_testcli_list" in result.output


def test_build_docker_cli(monkeypatch):
    dockerfile = CPATH.DOCKER_DIR / "Dockerfile_testcli_build"
    dockerfile.write_text("FROM alpine")

    called = {}

    def mock_run(cmd, check):
        called["cmd"] = cmd

    monkeypatch.setattr("subprocess.run", mock_run)

    result = runner.invoke(commands, ["docker", "build", "testcli_build"])
    assert result.exit_code == 0
    assert "built successfully" in result.output.lower()
    assert "cmd" in called
