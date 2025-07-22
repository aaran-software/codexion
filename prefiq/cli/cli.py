# prefiq/cli.py
import typer

from prefiq.cli.apps import app_cli
from prefiq.cli.config.commands import config_cli
from prefiq.cli.docker.dockerfile_action import docker_cmd

commands = typer.Typer()
commands.add_typer(app_cli.app_cmd, name="app")
commands.add_typer(config_cli, name="config")
commands.add_typer(docker_cmd, name="docker")


def main():
    commands()
