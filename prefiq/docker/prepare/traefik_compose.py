from passlib.context import CryptContext
from prefiq.docker.prepare.generate_from_template import generate_from_template
from prefiq.utils.cprint import cprint_success
from prefiq import CPATH
from pathlib import Path
import shutil

TEMPLATE_NAME = "traefik.j2"
OUTPUT_PATH = CPATH.DOCKER_DIR

# Ensure bcrypt hashing
bcrypt_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_traefik_compose(email: str,
                           dashboard_domain: str = None,
                           admin_user: str = None,
                           admin_password: str = None,
                           output_dir=None):
    context = {
        "email": email,
    }

    if dashboard_domain and admin_user and admin_password:
        # Generate bcrypt hash
        bcrypt_hash = bcrypt_ctx.hash(admin_password)
        context["dashboard_domain"] = dashboard_domain
        context["dashboard_auth_user"] = f"{admin_user}:{bcrypt_hash}"

    generate_from_template(
        template_name=TEMPLATE_NAME,
        output_filename="docker-compose-traefik.yml",
        context=context,
        output_dir=output_dir or OUTPUT_PATH
    )

    cprint_success("Traefik compose generated.")


def delete_traefik_compose(output: Path) -> list[str]:
    """
    Delete Traefik-related files in the output directory.

    Args:
        output (Path): Path to the directory where Traefik files are stored.

    Returns:
        List[str]: List of deleted file/folder names.
    """
    deleted = []
    compose_file = output / "docker-compose-traefik.yml"
    dynamic_dir = output / "dynamic"
    letsencrypt_dir = output / "letsencrypt"

    if compose_file.exists():
        compose_file.unlink()
        deleted.append("docker-compose-traefik.yml")

    if dynamic_dir.exists() and dynamic_dir.is_dir():
        shutil.rmtree(dynamic_dir)
        deleted.append("dynamic/")

    if letsencrypt_dir.exists() and letsencrypt_dir.is_dir():
        shutil.rmtree(letsencrypt_dir)
        deleted.append("letsencrypt/")

    return deleted
