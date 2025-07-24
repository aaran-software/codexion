from pathlib import Path
from prefiq.docker.common.generate_from_template import generate_from_template
from prefiq.utils.cprint import cprint_success
from prefiq import CPATH

TEMPLATE_NAME = "mariadb.j2"

def create_mariadb_compose(name: str, password: str = "DbPass1@@", output_dir: Path = None) -> str:
    """
    Generates docker-compose file for MariaDB.
    """
    if output_dir is None:
        output_dir = CPATH.DOCKER_DIR

    output_filename = "docker-compose-mariadb.yml"

    context = {
        "db_name": name,
        "db_password": password,
    }

    generate_from_template(
        template_name=TEMPLATE_NAME,
        output_filename=output_filename,
        context=context,
        output_dir=str(output_dir)
    )

    full_path = output_dir / output_filename
    cprint_success(f"Compose written to:  {full_path}")
    return str(full_path)
