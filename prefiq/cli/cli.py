# prefiq/cli.py
import typer

from prefiq.cli.apps import app_cli
from prefiq.cli.config.commands import config_cli
from prefiq.cli.docker.dockerfile_action import docker_cmd
from prefiq.cli.docker.compose_action import compose_cmd
from prefiq.cli.docker.traefik import traefik_cmd
from prefiq.cli.docker.build_cli import build_cmd

commands = typer.Typer()
commands.add_typer(app_cli.app_cmd, name="app")
commands.add_typer(config_cli, name="config")
commands.add_typer(docker_cmd, name="docker")
commands.add_typer(compose_cmd, name="compose")
docker_cmd.add_typer(traefik_cmd, name="traefik")
docker_cmd.add_typer(build_cmd, name="build")


def main():
    commands()
