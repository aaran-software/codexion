from pathlib import Path
from prefiq.docker.common.generate_from_template import generate_from_template
from prefiq.utils.cprint import cprint_success, cprint_error
from prefiq import CPATH

TEMPLATE_NAME = "cloud.j2"
DEFAULT_OUTPUT_PATH = CPATH.DOCKER_DIR


def create_site_compose(domain: str, port: int, output_dir: Path = DEFAULT_OUTPUT_PATH) -> None:
    # Sanitize domain for Docker-safe naming
    name = domain.replace('.', '_').lower()

    context = {
        "service_name": name,
        "image_name": name,
        "version": "1",
        "container_name": name,
        "host_port": port,
        "container_port": port,
        "domain": domain,
        "router_prefix": name,
        "traefik_service_name": name,
    }

    output_filename = f"docker-compose-{name}.yml"
    output_path = output_dir / output_filename

    generate_from_template(
        template_name=TEMPLATE_NAME,
        output_filename=output_filename,
        context=context,
        output_dir=str(output_dir)  # now a Path, not str
    )

    cprint_success(f"Compose written to: {output_path}")


def remove_site_compose(domain: str, output_dir: Path = DEFAULT_OUTPUT_PATH) -> None:
    name = domain.replace('.', '_').lower()
    filepath = output_dir / f"docker-compose-{name}.yml"

    if filepath.exists():
        filepath.unlink()
        cprint_success(f"Compose removed: {filepath}")
    else:
        cprint_error(f"Compose file not found: {filepath}")


def list_compose_files() -> list[str]:
    files = list(DEFAULT_OUTPUT_PATH.glob("docker-compose-*.yml"))
    return sorted(f.name for f in files)
