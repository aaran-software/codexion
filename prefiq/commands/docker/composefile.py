import os
from jinja2 import Environment, FileSystemLoader
from mypy.types import names

from prefiq.commands.docker.generate_from_template import generate_from_template
from prefiq.utils.ui import print_success

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
OUTPUT_DIR = os.path.join(os.getcwd(), 'docker')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def docker_compose(
        name: str
):
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template('dockerfile.j2')

    context = {
        "base_image": "ubuntu:24.04",
        "packages": ["python3", "python3-pip", "curl", "nano"],
        "cmd": "bash"
    }

    dockerfile = "Dockerfile_" + name

    generate_from_template('dockerfile.j2', dockerfile, context, OUTPUT_DIR)

    print_success(f"Dockerfile written to: {OUTPUT_DIR}\\{dockerfile}")
