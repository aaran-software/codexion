# prefiq/cli.py
import typer

from prefiq.commands.app import actions
from prefiq.commands.docker.docker_actions import dockit_app

docker = typer.Typer()
docker.add_typer(dockit_app, name="dockit")

def main():
    # actions.run_cli()
    docker()