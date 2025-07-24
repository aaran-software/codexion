import typer
from typing import Optional
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
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output directory")
):
    """
    Build Docker components: full stack, or individual parts like site, DB, proxy.
    """
    # --- 1. All-in-One Interactive Prompt ---
    if component in ["all", None]:
        site = typer.prompt("Site name (e.g. sundar.com)")
        site_port = typer.prompt("Site port", default=8000)
        db_choice = typer.prompt("Database (mariadb/postgres)", default="mariadb")
        proxy_choice = typer.prompt("Reverse Proxy (traefik/nginx)", default="traefik")

        create_docker(site)
        create_site_compose(site, site_port, output_dir=output)

        if db_choice.lower() in ["m", "mariadb"]:
            create_mariadb_compose(output_dir=output)
        elif db_choice.lower() in ["p", "postgres"]:
            create_postgres_compose(output_dir=output)

        if proxy_choice.lower() in ["t", "traefik"]:
            email = typer.prompt("Email for Let's Encrypt")
            create_traefik_compose(email=email, output_dir=output)
        elif proxy_choice.lower() in ["n", "nginx"]:
            create_nginx_compose(output_dir=output)

    # --- 2. Individual Component ---
    elif component.lower() in ["site"]:
        site_name = typer.prompt("Site name (e.g. sundar.com)")
        site_port = typer.prompt("Site port", default=8000)
        create_docker(site_name)
        create_site_compose(site_name, site_port, output_dir=output)

    elif component.lower() in ["m", "mariadb"]:
        create_mariadb_compose(output_dir=output)

    elif component.lower() in ["p", "postgres"]:
        create_postgres_compose(output_dir=output)

    elif component.lower() in ["t", "traefik"]:
        email = typer.prompt("Email for Let's Encrypt")
        create_traefik_compose(email=email, output_dir=output)

    elif component.lower() in ["n", "nginx"]:
        create_nginx_compose(output_dir=output)

    else:
        typer.echo("[ERROR] Unknown component. Valid options: all, site, mariadb, postgres, traefik, nginx")
