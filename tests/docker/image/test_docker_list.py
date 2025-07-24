import pytest
from pathlib import Path
from typer.testing import CliRunner
from prefiq.cli.docker.compose_list_cli import list_docker_assets

runner = CliRunner()

@pytest.fixture
def mock_docker_dir(tmp_path: Path) -> Path:
    # Simulated Docker-related files
    (tmp_path / "Dockerfile_sundar").write_text("# Sample Dockerfile")
    (tmp_path / "Dockerfile_sundar.com").write_text("# Another Dockerfile")

    (tmp_path / "docker-compose-sundar_com.yml").write_text("version: '3'")
    (tmp_path / "docker-compose-sundr_ocd.yml").write_text("version: '3'")

    (tmp_path / "docker-compose-mariadb.yml").write_text("version: '3'")
    (tmp_path / "docker-compose-postgres.yml").write_text("version: '3'")

    (tmp_path / "docker-compose-nginx.yml").write_text("version: '3'")
    (tmp_path / "docker-compose-traefik.yml").write_text("version: '3'")

    return tmp_path


def test_list_docker_assets_output(mock_docker_dir, capsys):
    list_docker_assets(folder=mock_docker_dir)

    captured = capsys.readouterr()
    output = captured.out

    assert "📂 Scanning folder" in output
    assert "🐳 Dockerfiles:" in output
    assert "✔ Dockerfile_sundar" in output
    assert "✔ Dockerfile_sundar.com" in output

    assert "📦 Docker Compose (Site files):" in output
    assert "✔  docker-compose-sundar_com.yml" in output
    assert "✔  docker-compose-sundr_ocd.yml" in output

    assert "🛢️ Database Compose Files:" in output
    assert "✔  docker-compose-mariadb.yml" in output
    assert "✔  docker-compose-postgres.yml" in output

    assert "🌐 Reverse Proxy Compose Files:" in output
    assert "✔ docker-compose-nginx.yml" in output
    assert "✔ docker-compose-traefik.yml" in output

    assert "✅ Scan complete." in output
