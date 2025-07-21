import os
from prefiq.commands.docker.templates.generate_from_template import generate_from_template
from prefiq.utils.ui import print_success

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
    print_success("Traefik compose generated.")
