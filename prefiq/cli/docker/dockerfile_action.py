import typer

from prefiq.docker.prepare.dockerfile import create_docker,update_docker, list_dockers, remove_docker, build_docker

docker_cmd = typer.Typer(help="Docker-related commands")


def prompt_for_name(prompt_text: str = "Name of docker") -> str:
    return typer.prompt(prompt_text)


@docker_cmd.command("create")
def create(name: str = typer.Argument(None, help="Name of Dockerfile")):
    """Create a new Dockerfile configuration"""
    if not name:
        name = prompt_for_name()
    create_docker(name)
    typer.echo(f"Dockerfile '{name}' created successfully.")


@docker_cmd.command("update")
def update(name: str = typer.Argument(None, help="Name of Dockerfile to update")):
    """Update an existing Dockerfile configuration"""
    if not name:
        name = prompt_for_name()
    update_docker(name)
    typer.echo(f"Dockerfile '{name}' updated successfully.")


@docker_cmd.command("remove")
def remove(name: str = typer.Argument(None, help="Name of Dockerfile to remove")):
    """Remove a Dockerfile configuration"""
    if not name:
        name = prompt_for_name()
    remove_docker(name)
    typer.echo(f"Dockerfile '{name}' removed successfully.")


@docker_cmd.command("list")
def list_all():
    """List all Dockerfile configurations"""
    lists = list_dockers() or []
    if not lists:
        typer.echo("No Dockerfiles found.")
    else:
        typer.echo("Dockerfiles:")
        for app in lists:
            typer.echo(f"- {app}")


@docker_cmd.command("build-image")
def build_image(name: str = typer.Argument(None, help="Name of Dockerfile to build")):
    """Build a Dockerfile for the specified app"""
    if not name:
        name = prompt_for_name()
    build_docker(name)
    typer.echo(f"Dockerfile for '{name}' built successfully.")
