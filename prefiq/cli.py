# prefiq/cli.py
import typer

# from prefiq.commands.app import actions
from prefiq.commands.docker.dockgen import docker_build
from prefiq.commands.docker.action import docker_action

docker = typer.Typer()
docker.add_typer(docker_build, name="docker", help="Docker commands")
docker.add_typer(docker_action, name="docker", help="Docker actions")


def main():
    # actions.run_cli()
    docker()
