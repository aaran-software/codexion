import typer
from typing import Optional
from prefiq.docker.prepare.mariadb_compose import create_mariadb_compose
from prefiq.docker.prepare.postgres_compose import create_postgres_compose
from prefiq.docker.prepare.traefik_compose import create_traefik_compose
from prefiq.docker.prepare.nginx_compose import create_nginx_compose
from prefiq.docker.prepare.site_compose import create_site_compose
from prefiq.docker.prepare.dockerfile import build_docker

build_cmd = typer.Typer(help="Create all Docker Compose stack")

@build_cmd.command("create-all", help="Build Docker stack")
def create_all(
    component: Optional[str] = typer.Argument(
        None,
        help="Create all: Dockerfile, site name, mariadb, postgres, traefik, nginx"
    ),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output directory")
):

    if component in ["all", None]:
        site = typer.prompt("Site name")
        db_choice = typer.prompt("Database (mariadb/postgres)", default="m")
        proxy_choice = typer.prompt("Reverse Proxy (traefik/nginx)", default="t")

        create_site_compose(site, output_dir=output)
        build_dockerfile(site)

        if db_choice.lower() in ["m", "mariadb"]:
            create_mariadb_compose(output_dir=output)
        elif db_choice.lower() in ["p", "postgres"]:
            create_postgres_compose(output_dir=output)

        if proxy_choice.lower() in ["t", "traefik"]:
            email = typer.prompt("Email for Let's Encrypt")
            create_traefik_compose(email=email, output_dir=output)
        elif proxy_choice.lower() in ["n", "nginx"]:
            create_nginx_compose(output_dir=output)

    elif component.lower().endswith(".com"):
        create_site_compose(component, output_dir=output)
        build_dockerfile(component)

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
        build_dockerfile(component)
