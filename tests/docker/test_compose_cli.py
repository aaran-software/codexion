import pytest
from typer.testing import CliRunner
from pathlib import Path

from prefiq import CPATH
from prefiq.cli.cli import commands

runner = CliRunner()


@pytest.fixture(autouse=True)
def clean_compose_files():
    for f in Path(CPATH.DOCKER_DIR).glob("docker-compose-testcli_*.yml"):
        f.unlink()
    yield
    for f in Path(CPATH.DOCKER_DIR).glob("docker-compose-testcli_*.yml"):
        f.unlink()


def test_create_compose_cli():
    result = runner.invoke(commands, ["compose", "create", "testcli.com", "8080"])
    assert result.exit_code == 0
    assert "created successfully" in result.output.lower()
    assert (CPATH.DOCKER_DIR / "docker-compose-testcli_com.yml").exists()


def test_remove_compose_cli():
    compose_file = CPATH.DOCKER_DIR / "docker-compose-testcli_remove.yml"
    compose_file.write_text("# Dummy file")
    assert compose_file.exists()

    result = runner.invoke(commands, ["compose", "remove", "testcli.remove"])
    assert result.exit_code == 0
    assert "removed successfully" in result.output.lower()
    assert not compose_file.exists()


def test_list_compose_cli():
    compose_file = CPATH.DOCKER_DIR / "docker-compose-testcli_list.yml"
    compose_file.write_text("# Dummy Compose file")

    result = runner.invoke(commands, ["compose", "list"])

    assert result.exit_code == 0
    assert "docker-compose-testcli_list.yml" in result.output
