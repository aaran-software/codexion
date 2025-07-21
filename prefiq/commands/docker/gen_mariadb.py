import os

from prefiq.commands.docker.templates.generate_from_template import generate_from_template
from prefiq.utils.ui import print_success

# Define paths
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
OUTPUT_DIR = os.path.join(os.getcwd(), 'docker')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def gen_mariadb_compose(name: str, password: str = "DbPass1@@"):
    """
    Generates docker-compose files for MariaDB and PostgreSQL
    """

    # Shared context
    context = {
        "db_name": name,
        "db_password": password,
    }

    # File outputs
    output_files = {
        "mariadb.j2": "docker-compose-mariadb.yml",
        "postgres.j2": "docker-compose-postgres.yml"
    }

    # Loop over templates
    for template_name, output_filename in output_files.items():
        generate_from_template(
            template_name=template_name,
            output_filename=output_filename,
            context=context,
            output_dir=OUTPUT_DIR
        )
        print_success(f"Compose written to: {os.path.join(OUTPUT_DIR, output_filename)}")
