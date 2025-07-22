import os

from prefiq.docker.prepare.generate_from_template import generate_from_template
from prefiq import CPATH
from prefiq.utils.cprint import cprint_success

TEMPLATE_NAME = "postgres.j2"
OUTPUT_PATH = CPATH.DOCKER_DIR


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
        output_dir=OUTPUT_PATH
    )

    cprint_success(f"Compose written to: {os.path.join(OUTPUT_PATH, output_filename)}")
