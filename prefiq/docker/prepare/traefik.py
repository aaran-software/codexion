import os

from prefiq.docker.prepare.generate_from_template import generate_from_template
from prefiq.utils.cprint import cprint_success
from prefiq import CPATH

TEMPLATE_NAME = "traefik.j2"
OUTPUT_PATH = CPATH.DOCKER_DIR


def gen_traefik_compose(email: str):
    context = {
        "email": email,
    }
    generate_from_template(
        template_name='traefik.j2',
        output_filename='docker-compose-traefik.yml',
        context=context,
        output_dir=OUTPUT_DIR
    )

    cprint_success("Traefik compose generated.")
