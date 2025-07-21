# prefiq/cli.py
import typer

from prefiq.commands.app import actions
from prefiq.commands.docker.actions import docker_build

docker = typer.Typer()
docker.add_typer(docker_build, name="docker", help="Docker commands")

def main():
    # actions.run_cli()
    docker()