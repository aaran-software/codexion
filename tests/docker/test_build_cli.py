from typer.testing import CliRunner
from pathlib import Path
from prefiq.cli.cli import commands

runner = CliRunner()

def test_docker_build_all(tmp_path: Path):
    input_data = "\n".join([
        "sundar.com",        # Site name
        "mariadb",           # DB
        "root",              # DB user
        "DbPass1@@",         # DB pass
        "traefik",           # Proxy
        "admin@example.com"  # Email
    ]) + "\n"

    result = runner.invoke(commands, ["docker", "build", "all", "--output", str(tmp_path)], input=input_data)

    assert result.exit_code == 0, result.stdout
    assert "Full Docker stack generated" in result.stdout
    assert (tmp_path / "docker-compose-mariadb.yml").exists()
    assert (tmp_path / "docker-compose-traefik.yml").exists()
