import typer
import subprocess
from pathlib import Path
from typing import Optional

from prefiq.commands.docker.actions.build import run_build

docker_action = typer.Typer(help="Docker-related operations")

DOCKERFILE_DIR = Path("./docker")
DEFAULT_REGISTRY = "docker.io"

# ------------------ Build ------------------

@docker_action.command("build", help="Build Docker image(s)")
def build(
    name: Optional[str] = typer.Argument(None, help="App name to build (if omitted, builds all from docker.json)"),
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

@docker_action.command("tag", help="Tag a Docker image")
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

@docker_action.command("push", help="Push a Docker image to registry")
def push(
    tag: str = typer.Argument(..., help="Image tag to push (e.g., sundar:latest)")
):
    """
    Push a Docker image to a registry.
    """
    typer.echo(f"📤 Pushing image {tag}")
    subprocess.run(["docker", "push", tag], check=True)


# ------------------ Delete ------------------

@docker_action.command("delete", help="Delete a local Docker image")
def delete(
    name: str = typer.Argument(..., help="Image name to delete")
):
    """
    Remove local Docker image.
    """
    typer.echo(f"🗑️ Removing image: {name}")
    subprocess.run(["docker", "rmi", name], check=True)


# ------------------ Up ------------------

@docker_action.command("up", help="Start containers using docker-compose")
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

@docker_action.command("down", help="Stop and remove containers")
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

@docker_action.command("purge", help="Stop and delete image & container")
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

@docker_action.command("registry", help="Show full image path in registry")
def registry(
    name: str = typer.Argument(..., help="App/domain name"),
    tag: str = typer.Option("latest", "--tag", help="Image tag")
):
    """
    Print full image path in the registry.
    """
    full_path = f"{DEFAULT_REGISTRY}/{name}:{tag}"
    typer.echo(f"📦 Registry path: {full_path}")
