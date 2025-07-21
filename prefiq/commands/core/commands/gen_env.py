import os
from prefiq.commands.docker.commands.prepare.generate_from_template import generate_from_template
from prefiq.commands.utils.ui import print_success

# Paths
OUTPUT_DIR = os.path.join(os.getcwd(), "docker")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def gen_env_file(context: dict):
    """
    Generate .env.sample file from Jinja2 template using dynamic context.
    """
    generate_from_template(
        template_name="env.j2",
        output_filename=".env.sample",
        context=context,
        output_dir=OUTPUT_DIR
    )
    print_success(f".env.sample written to: {os.path.join(OUTPUT_DIR, '.env.sample')}")
