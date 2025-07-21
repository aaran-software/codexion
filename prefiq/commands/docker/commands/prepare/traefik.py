import os

from prefiq.commands.docker.commands.prepare.gen_docker_json import gen_docker_json
from prefiq.commands.docker.commands.prepare.generate_from_template import generate_from_template
from prefiq.commands.utils.ui import print_success

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
OUTPUT_DIR = os.path.join(os.getcwd(), 'docker')
os.makedirs(OUTPUT_DIR, exist_ok=True)


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

    gen_docker_json("TRAEFIK_COMPOSE", {os.path.join(OUTPUT_DIR, "docker-compose-traefik.yml")})

    print_success("Traefik compose generated.")
