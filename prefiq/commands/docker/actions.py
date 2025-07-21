import typer

from prefiq.commands.docker.composefile import gen_compose
from prefiq.commands.docker.dockerfile import gen_dockerfile
from prefiq.commands.docker.gen_mariadb import gen_mariadb_compose
from prefiq.commands.docker.gen_pgdb import gen_pgdb_compose
from prefiq.commands.docker.nginx import gen_nginx_compose
from prefiq.commands.docker.traefik import gen_traefik_compose

docker_build = typer.Typer(help="Docker utility commands")


@docker_build.command("build")
def create_dockerfile(name: str = typer.Option(None, "--name", "-n", help="Dockerfile name (e.g., app)")):
    if not name:
        name = typer.prompt("Dockerfile name (e.g., app)")
    gen_dockerfile(name=name)


@docker_build.command("compose")
def compose_docker():
    domain = typer.prompt("Domain (e.g., sundar.com)")
    port = typer.prompt("Port (e.g., 8000)", type=int)
    gen_compose(domain=domain, port=port)


@docker_build.command("mariadb")
def compose_mariadb():
    name = typer.prompt("MariaDB database name", default="mariadb")
    password = typer.prompt("MariaDB root password", default="DbPass1@@", hide_input=True)
    gen_mariadb_compose(name=name, password=password)


@docker_build.command("pgdb")
def compose_pgdb():
    name = typer.prompt("Postgres database name", default="postgres")
    password = typer.prompt("Postgres root password", default="PgPass1@@", hide_input=True)
    gen_pgdb_compose(name=name, password=password)


@docker_build.command("nginx")
def compose_nginx_proxy():
    service_name = typer.prompt("App service name (e.g., cloud)")
    service_port = typer.prompt("Internal port (e.g., 8000)", type=int)
    gen_nginx_compose(service_name=service_name, service_port=service_port)


@docker_build.command("traefik")
def compose_traefik_proxy():
    email = typer.prompt("Email for SSL cert (Let's Encrypt)")
    gen_traefik_compose(email=email)
