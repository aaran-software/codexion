from prefiq.docker.prepare.generate_from_template import generate_from_template
from prefiq.utils.cprint import cprint_success

TEMPLATE_NAME = "postgres.j2"

def create_postgres_compose(name: str, password: str = "PgPass1@@"):
    """
    Generates docker-compose file for Postgres SQL
    """
    from prefiq import CPATH
    output_path = CPATH.DOCKER_DIR
    output_filename = "docker-compose-postgres.yml"

    context = {
        "db_name": name,
        "db_password": password,
    }

    generate_from_template(
        template_name=TEMPLATE_NAME,
        output_filename=output_filename,
        context=context,
        output_dir=output_path
    )

    full_path = output_path / output_filename
    cprint_success(f"Compose written to:  {full_path}")
    return full_path
