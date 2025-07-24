import pytest
from typer.testing import CliRunner
from prefiq.cli.cli import commands
import prefiq

runner = CliRunner()

def test_mariadb_compose(tmp_path, monkeypatch):
    # ✅ PATCH where the compose file is saved
    monkeypatch.setattr(prefiq.CPATH, "DOCKER_DIR", tmp_path)

    cmd = ["compose-site", "mariadb", "--database", "test_db", "--port", "3307"]
    expected_file = tmp_path / "docker-compose-mariadb.yml"

    result = runner.invoke(commands, cmd)
    print(result.output)
    print("Files in tmp_path:", list(tmp_path.iterdir()))

    assert result.exit_code == 0
    assert expected_file.exists()
    assert "test_db" in expected_file.read_text()


def test_postgres_compose(tmp_path, monkeypatch):
    # ✅ PATCH where the compose file is saved
    monkeypatch.setattr(prefiq.CPATH, "DOCKER_DIR", tmp_path)

    cmd = ["compose-site", "postgres", "--database", "test_pg", "--port", "5433"]
    expected_file = tmp_path / "docker-compose-postgres.yml"

    result = runner.invoke(commands, cmd)
    print(result.output)
    print("Files in tmp_path:", list(tmp_path.iterdir()))

    assert result.exit_code == 0
    assert expected_file.exists()
    assert "test_pg" in expected_file.read_text()
