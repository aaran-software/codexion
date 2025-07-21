import os
from jinja2 import Environment, FileSystemLoader

from prefiq.utils.ui import print_success

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
OUTPUT_DIR = os.path.join(os.getcwd(), 'docker')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_dockerfile(
    name: str
):
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template('dockerfile.j2')

    rendered = template.render(
        base_image=name,
    )

    output_path = os.path.join(OUTPUT_DIR, "Dockerfile_"+name)
    with open(output_path, 'w') as f:
        f.write(rendered)

    print_success(f"Dockerfile written to: {output_path}")
