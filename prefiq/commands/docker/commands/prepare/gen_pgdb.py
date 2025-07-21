import os

from prefiq.commands.core.commands.update_env import gen_env
from prefiq.commands.docker.commands.prepare.gen_docker_json import gen_docker_json
from prefiq.commands.docker.commands.prepare.generate_from_template import generate_from_template
from prefiq.commands.utils.ui import print_success

# Define paths
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
OUTPUT_DIR = os.path.join(os.getcwd(), 'docker')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def gen_pgdb_compose(name: str, password: str = "PgPass1@@"):
    """
    Generates docker-compose file for Postgres SQL
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

    gen_env("PG_DB", name)
    gen_env("PG_PASSWORD", password)

    gen_docker_json("PG_COMPOSE", {os.path.join(OUTPUT_DIR, output_filename)})

    print_success(f"Compose written to: {os.path.join(OUTPUT_DIR, output_filename)}")
