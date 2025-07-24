# tests/test_generate_full_stack.py
from typer.testing import CliRunner
from pathlib import Path

from prefiq.cli.cli import commands  # ✅ use top-level CLI

runner = CliRunner()

def test_create_all_full_stack(tmp_path: Path):
    input_data = "\n".join([
        "sundar.com",        # Site name
        "8080",              # Site port
        "mariadb",           # DB choice
        "sundar_db",         # DB name
        "DbPass1@@",         # DB pass
        "traefik",           # Proxy choice
        "admin@example.com"  # Email for Traefik
    ]) + "\n"

    result = runner.invoke(commands, ["generate", "all", "--output", str(tmp_path)], input=input_data)

    assert result.exit_code == 0, f"Exited with {result.exit_code}: {result.stdout}"

    assert (tmp_path / "Dockerfile_sundar_com").exists(), "Missing Dockerfile"
    assert (tmp_path / "docker-compose.yml").exists(), "Missing site compose"
    assert (tmp_path / "docker-compose-mariadb.yml").exists(), "Missing MariaDB compose"
    assert (tmp_path / "docker-compose-traefik.yml").exists(), "Missing Traefik compose"
