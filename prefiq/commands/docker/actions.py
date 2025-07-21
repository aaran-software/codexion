import typer

from prefiq.commands.docker.composefile import docker_compose
from prefiq.commands.docker.dockerfile import generate_dockerfile

docker_build = typer.Typer(help="Prepare Dockerfile")


@docker_build.command("build")
def create_dockfile(
        name: str = typer.Argument(..., help="Dockerfile name (e.g., dockerfile)"),
):
    generate_dockerfile(name=name)


@docker_build.command("compose")
def compose_docker(
        name: str = typer.Argument(..., help="Dockerfile name (e.g., dockerfile)"),
):
    docker_compose( name=name )
