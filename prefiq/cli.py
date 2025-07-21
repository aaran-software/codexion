# prefiq/cli.py
import typer

# from prefiq.commands.app import actions
from prefiq.commands.docker.docgen import docker_actions

docker = typer.Typer()
docker.add_typer(docker_actions, name="docker", help="Docker commands")


def main():
    # actions.run_cli()
    docker()
