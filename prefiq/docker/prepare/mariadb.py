import os

from prefiq.docker.prepare.generate_from_template import generate_from_template
from prefiq.utils.cprint import cprint_success
from prefiq import CPATH

TEMPLATE_NAME = "mariadb.j2"
OUTPUT_PATH = CPATH.DOCKER_DIR

def gen_mariadb_compose(name: str, password: str = "DbPass1@@"):
    """
    Generates docker-compose file for MariaDB
    """

    context = {
        "db_name": name,
        "db_password": password,
    }

    output_filename = "docker-compose-mariadb.yml"

    generate_from_template(
        template_name=TEMPLATE_NAME,
        output_filename=output_filename,
        context=context,
        output_dir=OUTPUT_PATH
    )

    cprint_success(f"Compose written to: {os.path.join(OUTPUT_PATH, output_filename)}")
