import typer
from typing import Optional
from pathlib import Path

from prefiq.docker.prepare.dockerfile import create_docker
from prefiq.docker.prepare.site_compose import create_site_compose
from prefiq.docker.prepare.mariadb_compose import create_mariadb_compose
from prefiq.docker.prepare.postgres_compose import create_postgres_compose
from prefiq.docker.prepare.traefik_compose import create_traefik_compose
from prefiq.docker.prepare.nginx_compose import create_nginx_compose

generate_cmd = typer.Typer(help="Create all Docker Compose stack")


@generate_cmd.command("all", help="Build Docker stack")
def create_all(
    component: Optional[str] = typer.Argument(
        None,
        help="Create: all, site, mariadb, postgres, traefik, nginx"
    ),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Output directory (default: current folder)"
    )
):
    """
    Build Docker components: full stack, or individual parts like site, DB, proxy.
    """
    output_dir = output or Path.cwd()

    # --- 1. Full Stack Interactive ---
    if component in ["all", None]:
        site = typer.prompt("Site name (e.g. sundar.com)")
        site_port = int(typer.prompt("Site port", default=8000))
        db_choice = typer.prompt("Database (mariadb/postgres)", default="mariadb")
        proxy_choice = typer.prompt("Reverse Proxy (traefik/nginx)", default="traefik")

        create_docker(site, output_dir=output_dir)
        create_site_compose(site, site_port, output_dir=output_dir)

        if db_choice.lower() in ["m", "mariadb"]:
            db_name = typer.prompt("Db name (e.g. sundar_db)")
            db_pass = typer.prompt("Db pass", default="DbPass1@@")
            create_mariadb_compose(db_name, db_pass, output_dir=output_dir)

        elif db_choice.lower() in ["p", "postgres"]:
            db_pg_name = typer.prompt("Db name (e.g. sundar_db)")
            db_pg_pass = typer.prompt("Db pass", default="DbPass1@@")
            create_postgres_compose(db_pg_name, db_pg_pass, output_dir=output_dir)

        if proxy_choice.lower() in ["t", "traefik"]:
            email = typer.prompt("Email for Let's Encrypt")
            create_traefik_compose(email=email, site_name=site, output_dir=output_dir)

        elif proxy_choice.lower() in ["n", "nginx"]:
            create_nginx_compose(service_name="nginx", service_port=80, output_dir=output_dir)

    # --- 2. Individual Component ---
    elif component.lower() == "site":
        site_name = typer.prompt("Site name (e.g. sundar.com)")
        site_port = int(typer.prompt("Site port", default=8000))
        create_docker(site_name, output_dir=output_dir)
        create_site_compose(site_name, site_port, output_dir=output_dir)

    elif component.lower() in ["m", "mariadb"]:
        db_name = typer.prompt("Db name (e.g. sundar_db)")
        db_pass = typer.prompt("Db pass", default="DbPass1@@")
        create_mariadb_compose(db_name, db_pass, output_dir=output_dir)

    elif component.lower() in ["p", "postgres"]:
        db_pg_name = typer.prompt("Db name (e.g. sundar_db)")
        db_pg_pass = typer.prompt("Db pass", default="DbPass1@@")
        create_postgres_compose(db_pg_name, db_pg_pass, output_dir=output_dir)

    elif component.lower() in ["t", "traefik"]:
        email = typer.prompt("Email for Let's Encrypt")
        site_name = typer.prompt("Site name (e.g. sundar.com)")
        create_traefik_compose(email=email, output_dir=output_dir)
        create_traefik_compose(email=email, output_dir=output)

    elif component.lower() in ["n", "nginx"]:
        create_nginx_compose(service_name="nginx", service_port=80, output_dir=output_dir)

    else:
        typer.secho("[ERROR] Unknown component. Valid options: all, site, mariadb, postgres, traefik, nginx", fg=typer.colors.RED)
