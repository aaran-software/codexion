import os

from prefiq.commands.docker.commands.prepare.gen_docker_json import gen_docker_json
from prefiq.commands.docker.commands.prepare.generate_from_template import generate_from_template
from prefiq.commands.utils.ui import print_success

# Define paths
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
OUTPUT_DIR = os.path.join(os.getcwd(), 'docker')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def gen_dockerfile(name: str):
    context = {
        "base_image": "ubuntu:24.04",
        "packages": ["python3", "python3-pip", "curl", "nano"],
        "cmd": "bash"
    }

    output_filename = f"Dockerfile_{name}"

    generate_from_template(
        template_name='dockerfile.j2',
        output_filename=output_filename,
        context=context,
        output_dir=OUTPUT_DIR
    )

    gen_docker_json("DOCKERFILE_NAME", output_filename)
    gen_docker_json("DOCKERFILE_PATH", {os.path.join(OUTPUT_DIR, output_filename)})

    print_success(f"Dockerfile written to: {os.path.join(OUTPUT_DIR, output_filename)}")
