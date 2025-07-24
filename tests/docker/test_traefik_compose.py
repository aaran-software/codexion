import re
from pathlib import Path
from prefiq.docker.prepare.traefik_compose import create_traefik_compose


def test_create_traefik_compose_basic(tmp_path: Path):
    test_email = "test@example.com"
    expected_file = tmp_path / "docker-compose-traefik.yml"

    create_traefik_compose(email=test_email, output_dir=tmp_path)

    assert expected_file.exists(), "Compose file not created"
    content = expected_file.read_text()

    # Basic ACME email config
    assert test_email in content
    assert f"--certificatesresolvers.myresolver.acme.email={test_email}" in content
    assert "--entrypoints.web.address=:80" in content
    assert "--entrypoints.websecure.address=:443" in content


def test_create_traefik_with_dashboard_and_auth(tmp_path: Path):
    test_email = "admin@example.com"
    dashboard_domain = "traefik.local"
    admin_user = "admin"
    admin_password = "s3cr3t"

    expected_file = tmp_path / "docker-compose-traefik.yml"

    create_traefik_compose(
        email=test_email,
        dashboard_domain=dashboard_domain,
        admin_user=admin_user,
        admin_password=admin_password,
        output_dir=tmp_path
    )

    assert expected_file.exists(), "Compose file not created with dashboard"
    content = expected_file.read_text()

    # Verify values in generated content
    assert test_email in content
    assert dashboard_domain in content
    assert f"traefik.http.routers.api.rule=Host(`{dashboard_domain}`)" in content
    assert "traefik.http.middlewares.auth.basicauth.users=" in content
    assert "traefik.http.routers.api.middlewares=auth" in content

    # Assert bcrypt hash is present with proper format
    bcrypt_match = re.search(
        r"traefik\.http\.middlewares\.auth\.basicauth\.users=.*:\$2[aby]\$",
        content
    )
    assert bcrypt_match, "Bcrypt hash not found or invalid format"


from prefiq.docker.prepare.traefik_compose import delete_traefik_compose

def test_delete_traefik_compose(tmp_path: Path):
    # Setup dummy files
    compose = tmp_path / "docker-compose-traefik.yml"
    dynamic = tmp_path / "dynamic"
    letsencrypt = tmp_path / "letsencrypt"

    compose.write_text("dummy compose")
    dynamic.mkdir()
    letsencrypt.mkdir()

    # Confirm files exist
    assert compose.exists()
    assert dynamic.exists()
    assert letsencrypt.exists()

    # Run deletion
    deleted = delete_traefik_compose(tmp_path)

    # Check all are deleted
    assert "docker-compose-traefik.yml" in deleted
    assert "dynamic/" in deleted
    assert "letsencrypt/" in deleted
    assert not compose.exists()
    assert not dynamic.exists()
    assert not letsencrypt.exists()