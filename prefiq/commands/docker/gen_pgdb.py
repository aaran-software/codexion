import os

from prefiq.commands.docker.templates.generate_from_template import generate_from_template
from prefiq.utils.ui import print_success

# Define paths
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
OUTPUT_DIR = os.path.join(os.getcwd(), 'docker')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def gen_pgdb_compose(name: str, password: str = "PgPass1@@"):
    """
    Generates docker-compose file for PostgreSQL
    """
    context = {
        "db_name": name,
        "db_password": password,
    }

    output_filename = "docker-compose-postgres.yml"

    generate_from_template(
        template_name="postgres.j2",
        output_filename=output_filename,
        context=context,
        output_dir=OUTPUT_DIR
    )

    print_success(f"Compose written to: {os.path.join(OUTPUT_DIR, output_filename)}")
