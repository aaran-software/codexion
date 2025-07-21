import os
from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'templates')
OUTPUT_DIR = os.path.join(os.getcwd(), 'docker')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_dockerfile(
    name: str,
    base_image: str,
    workdir: str,
    copy_instructions: list,
    run_commands: list,
    cmd: str
):
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template('dockerfile.j2')

    rendered = template.render(
        base_image=base_image,
        workdir=workdir,
        copy_instructions=copy_instructions,
        run_commands=run_commands,
        cmd=cmd
    )

    output_path = os.path.join(OUTPUT_DIR, name)
    with open(output_path, 'w') as f:
        f.write(rendered)

    print(f"[✓] Dockerfile written to: {output_path}")
