from typer.testing import CliRunner
from pathlib import Path
import re
from prefiq.cli.cli import commands

runner = CliRunner()

def test_traefik_create_basic(tmp_path: Path):
    test_email = "admin@example.com"
    result = runner.invoke(commands, [
        "docker", "traefik", "create",
        "--email", test_email,
        "--output", str(tmp_path)
    ])

    if result.exit_code != 0:
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        print("EXCEPTION:", result.exception)

    assert result.exit_code == 0, f"Exited with {result.exit_code}\nStdout:\n{result.stdout}\nStderr:\n{result.stderr}"



def test_traefik_create_with_dashboard_auth(tmp_path: Path):
    email = "admin@example.com"
    domain = "traefik.local"
    username = "admin"
    password = "s3cr3t"

    result = runner.invoke(commands, [
        "docker", "traefik", "create",
        "--email", email,
        "--dashboard-domain", domain,
        "--admin-user", username,
        "--admin-password", password,
        "--output", str(tmp_path)
    ])

    assert result.exit_code == 0, result.stdout
    assert "[OK] Traefik compose generated." in result.stdout

    compose_file = tmp_path / "docker-compose-traefik.yml"
    assert compose_file.exists()

    content = compose_file.read_text()
    assert email in content
    assert domain in content
    assert "traefik.http.routers.api.middlewares=auth" in content
    assert "traefik.http.middlewares.auth.basicauth.users=" in content
    assert re.search(rf"{username}:\$2[aby]\$", content), "Missing bcrypt hash"


def test_traefik_delete(tmp_path: Path):
    from prefiq.docker.prepare.traefik_compose import create_traefik_compose

    # First create
    create_traefik_compose(email="admin@example.com", output_dir=tmp_path)
    assert (tmp_path / "docker-compose-traefik.yml").exists()

    # Then delete with --force
    result = runner.invoke(commands, [
        "docker", "traefik", "delete",
        "--output", str(tmp_path),
        "--force"
    ])

    assert result.exit_code == 0
    assert "Deleted" in result.stdout
    assert not (tmp_path / "docker-compose-traefik.yml").exists()
