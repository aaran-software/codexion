import typer
import subprocess
from pathlib import Path
from typing import Optional

from prefiq.commands.docker.commands.prepare.dockerfile import gen_dockerfile
from prefiq.commands.docker.commands.prepare.composefile import gen_compose
from prefiq.commands.docker.commands.prepare.gen_mariadb import gen_mariadb_compose
from prefiq.commands.docker.commands.prepare.gen_pgdb import gen_pgdb_compose
from prefiq.commands.docker.commands.prepare.nginx import gen_nginx_compose
from prefiq.commands.docker.commands.prepare.traefik import gen_traefik_compose
from prefiq.commands.docker.commands.prepare.gen_docker_json import remove_docker_domain_entry



docker_actions = typer.Typer(help="Prefiq Docker commands")
DOCKERFILE_DIR = Path("./docker")
DEFAULT_REGISTRY = "docker.io"


# ------------------ Create Dockerfile ------------------
@docker_actions.command("create", help="Generate a Dockerfile for your app.")
def create_dockerfile(name: str = typer.Option(None, "--name", "-n", help="Dockerfile name (e.g., app)")):
    """
    Generate a Dockerfile for your app.

    Usage: `prefiq docker create --name app`
    """
    if not name:
        name = typer.prompt("Dockerfile name (e.g., app)")
    gen_dockerfile(name=name)


# ------------------ Compose ------------------
@docker_actions.command("compose", help="Generate docker-compose.yml for your app with domain and port.")
def compose_docker():
    """
    Generate docker-compose.yml for your app with domain and port.

    Usage: `prefiq docker compose`
            :domain: Domain name for the app (e.g., sundar.com)
            :port: Port number for the app (e.g., 8000)

    """
    domain = typer.prompt("Domain (e.g., sundar.com)")
    port = typer.prompt("Port (e.g., 8000)", type=int)
    gen_compose(domain=domain, port=port)


# ------------------ MariaDB ------------------
@docker_actions.command("mariadb", help="Generate docker-compose file for MariaDB.")
def compose_mariadb():
    """
    Generate docker-compose file for MariaDB.
        :param name: Name of the MariaDB database (default: mariadb)
        :param password: Root password for MariaDB (default: DbPass1@@)
    """
    name = typer.prompt("MariaDB database name", default="mariadb")
    password = typer.prompt("MariaDB root password", default="DbPass1@@", hide_input=True)
    gen_mariadb_compose(name=name, password=password)


# ------------------ Postgres SQL ------------------
@docker_actions.command("pgdb", help="Generate docker-compose file for Postgres SQL.")
def compose_pgdb():
    """
    Generate docker-compose file for Postgres SQL.
    """
    name = typer.prompt("Postgres database name", default="postgres")
    password = typer.prompt("Postgres root password", default="PgPass1@@", hide_input=True)
    gen_pgdb_compose(name=name, password=password)


# ------------------ Nginx ------------------
@docker_actions.command("nginx", help="Generate docker-compose and nginx.conf for reverse proxy.")
def compose_nginx_proxy():
    """
    Generate docker-compose and nginx.conf for reverse proxy.
    """
    service_name = typer.prompt("App service name (e.g., cloud)")
    service_port = typer.prompt("Internal port (e.g., 8000)", type=int)
    gen_nginx_compose(service_name=service_name, service_port=service_port)


# ------------------ Traefik ------------------
@docker_actions.command("traefik", help="Generate docker-compose for Traefik with SSL setup.")
def compose_traefik_proxy():
    """
    Generate docker-compose for Traefik with Let's Encrypt SSL setup.
    """
    email = typer.prompt("Email for SSL cert (Let's Encrypt)")
    gen_traefik_compose(email=email)


# ------------------ Build ------------------
@docker_actions.command("remove-compose", help="Remove a site's docker-compose entry")
def remove_compose_entry(domain: str = typer.Argument(None, help="Domain to remove (e.g., sundar.com)")):
    """
      Remove a site's docker-compose entry from docker.json.
    """
    if not domain:
        domain = typer.prompt("Domain to remove (e.g., sundar.com)")

    remove_docker_domain_entry(domain)


# ------------------ Build ------------------

@docker_actions.command("build", help="Build Docker image(s)")
def build(
        name: Optional[str] = typer.Argument(None,
                                             help="App name to build (if omitted, builds all from docker.json)"),
        push: bool = typer.Option(False, "--push", help="Push image after building"),
        tag: Optional[str] = typer.Option(None, "--tag", help="Override tag (e.g., myapp:latest)")
):
    """
    Build Docker image(s) from docker.json or single app.
    """
    run_build(name=name, push=push, tag=tag)

    typer.echo(f"🔨 Building image for: {name or 'ALL'} (push={push}, tag={tag})")
    # Call docker build commands here


# ------------------ Tag ------------------

@docker_actions.command("tag", help="Tag a Docker image")
def tag(
        source: str = typer.Argument(..., help="Source image name (e.g., sundar:latest)"),
        target: str = typer.Argument(..., help="Target image tag (e.g., registry.com/sundar:latest)")
):
    """
    Tag a Docker image with a new name.
    """
    typer.echo(f"🏷️ Tagging image {source} as {target}")
    subprocess.run(["docker", "tag", source, target], check=True)


# ------------------ Push ------------------

@docker_actions.command("push", help="Push a Docker image to registry")
def push(
        tag: str = typer.Argument(..., help="Image tag to push (e.g., sundar:latest)")
):
    """
    Push a Docker image to a registry.
    """
    typer.echo(f"📤 Pushing image {tag}")
    subprocess.run(["docker", "push", tag], check=True)


# ------------------ Delete ------------------

@docker_actions.command("delete", help="Delete a local Docker image")
def delete(
        name: str = typer.Argument(..., help="Image name to delete")
):
    """
    Remove local Docker image.
    """
    typer.echo(f"🗑️ Removing image: {name}")
    subprocess.run(["docker", "rmi", name], check=True)


# ------------------ Up ------------------

@docker_actions.command("up", help="Start containers using docker-compose")
def up(
        name: str = typer.Argument(..., help="App/domain name to start (e.g., sundar)")
):
    """
    Start container using docker-compose.
    """
    compose_file = f"docker/docker-compose-{name}.yml"
    typer.echo(f"⬆️ Starting container for {name}")
    subprocess.run(["docker-compose", "-f", compose_file, "up", "-d"], check=True)


# ------------------ Down ------------------

@docker_actions.command("down", help="Stop and remove containers")
def down(
        name: str = typer.Argument(..., help="App/domain name to stop (e.g., sundar)")
):
    """
    Stop container using docker-compose.
    """
    compose_file = f"docker/docker-compose-{name}.yml"
    typer.echo(f"⬇️ Stopping container for {name}")
    subprocess.run(["docker-compose", "-f", compose_file, "down"], check=True)


# ------------------ Purge ------------------

@docker_actions.command("purge", help="Stop and delete image & container")
def purge(
        name: str = typer.Argument(..., help="App/domain name to fully remove")
):
    """
    Fully remove container and image.
    """
    typer.echo(f"🔥 Purging {name}")
    down(name)
    delete(name)


# ------------------ Registry ------------------

@docker_actions.command("registry", help="Show full image path in registry")
def registry(
        name: str = typer.Argument(..., help="App/domain name"),
        tag: str = typer.Option("latest", "--tag", help="Image tag")
):
    """
    Print full image path in the registry.
    """
    full_path = f"{DEFAULT_REGISTRY}/{name}:{tag}"
    typer.echo(f"📦 Registry path: {full_path}")
