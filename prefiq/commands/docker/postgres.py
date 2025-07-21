import os

from prefiq.commands.docker.templates.generate_from_template import generate_from_template
from prefiq.utils.ui import print_success

# Define paths
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
OUTPUT_DIR = os.path.join(os.getcwd(), 'docker')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def gen_compose(name: str):
    context = {
        "base_image": "ubuntu:24.04",
        "packages": ["python3", "python3-pip", "curl", "nano"],
        "cmd": "bash"
    }

    output_filename = f"docker-compose-postgres.yml"

    generate_from_template(
        template_name='cloud.j2',
        output_filename=output_filename,
        context=context,
        output_dir=OUTPUT_DIR
    )

    print_success(f"Compose written to: {os.path.join(OUTPUT_DIR, output_filename)}")
