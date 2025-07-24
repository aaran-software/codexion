import os
from pathlib import Path

from prefiq.docker.prepare.generate_from_template import generate_from_template
from prefiq.utils.cprint import cprint_success, cprint_error
from prefiq import CPATH

TEMPLATE_NAME = "cloud.j2"
OUTPUT_PATH = CPATH.DOCKER_DIR


def create_site_compose(domain: str, port: int):
    # Sanitize name for docker usage
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
        "traefik_service_name": name
    }

    output_filename = f"docker-compose-{name}.yml"

    generate_from_template(
        template_name=TEMPLATE_NAME,
        output_filename=output_filename,
        context=context,
        output_dir=OUTPUT_PATH
    )

    cprint_success(f"Compose written to: {os.path.join(OUTPUT_PATH, output_filename)}")


def remove_site_compose(domain: str):
    """
    Remove the generated docker-compose YAML file based on the domain.
    """
    name = domain.replace('.', '_').lower()
    filename = os.path.join(OUTPUT_PATH, f"docker-compose-{name}.yml")

    if os.path.exists(filename):
        os.remove(filename)
        cprint_success(f"Compose removed: {filename}")
    else:
        cprint_error(f"Compose file not found: {filename}")


def list_compose_files():
    files = list(Path(CPATH.DOCKER_DIR).glob("docker-compose-*.yml"))
    return sorted(f.name for f in files)
