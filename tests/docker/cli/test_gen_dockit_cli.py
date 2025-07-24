from typer.testing import CliRunner
from pathlib import Path

from prefiq.cli.cli import commands  # ✅ use top-level CLI

runner = CliRunner()

def test_create_all_full_stack(tmp_path: Path):
    site_name = "sundar.com"
    sanitized = site_name.replace('.', '_').lower()

    input_data = "\n".join([
        site_name,         # Site name
        "8080",            # Site port
        "mariadb",         # DB choice
        "traefik",         # Reverse proxy
        "sundar_db",       # DB name
        "DbPass1@@",       # DB pass
        "admin@example.com"  # Email for Traefik
    ]) + "\n"

    result = runner.invoke(commands, ["generate", "all", "--output", str(tmp_path)], input=input_data)

    assert result.exit_code == 0, f"Exited with {result.exit_code}: {result.stdout}"
    print(result.stdout)

    assert (tmp_path / f"Dockerfile_{sanitized}").exists(), "Missing Dockerfile"
    assert (tmp_path / f"docker-compose-{sanitized}.yml").exists(), "Missing site compose"
    assert (tmp_path / "docker-compose-mariadb.yml").exists(), "Missing MariaDB compose"
    assert (tmp_path / "docker-compose-traefik.yml").exists(), "Missing Traefik compose"

