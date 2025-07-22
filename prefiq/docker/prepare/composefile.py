import os

from prefiq.core.commands.update_env import gen_env
from prefiq.docker.gen_docker_json import gen_docker_json
from prefiq.docker.generate_from_template import generate_from_template
from prefiq.utils.cprint import cprint_success

# Define paths
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
OUTPUT_DIR = os.path.join(os.getcwd(), 'docker')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def gen_compose(domain: str, port: int):
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
        template_name='cloud.j2',
        output_filename=output_filename,
        context=context,
        output_dir=OUTPUT_DIR
    )

    gen_env("DOMAIN", name)
    gen_env("DOMAIN_PORT", str(port))

    gen_docker_json(
        key="COMPOSE_FILE",
        file_path=os.path.join(OUTPUT_DIR, output_filename),
        domain=name,
        port=str(port)
    )

    cprint_success(f"Compose written to: {os.path.join(OUTPUT_DIR, output_filename)}")
