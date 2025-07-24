# prefiq/cli.py
import typer

from prefiq.cli.apps import app_cli
from prefiq.cli.config.commands import config_cli
from prefiq.cli.docker.dockerfile_action import docker_cmd
from prefiq.cli.docker.compose_action import compose_cmd
from prefiq.cli.docker.traefik import traefik_cmd
from prefiq.cli.docker.gen_dockit_cli import generate_cmd
from prefiq.cli.docker.compose_runner_cli import docker_run_cmd
from prefiq.cli.docker.compose_list_cli import  list_docker_assets

commands = typer.Typer()
commands.add_typer(app_cli.app_cmd, name="app")
commands.add_typer(config_cli, name="config")
commands.add_typer(docker_cmd, name="dockfile")
commands.add_typer(compose_cmd, name="compose-site")
commands.add_typer(traefik_cmd, name="traefik")
commands.add_typer(generate_cmd, name="generate")
commands.add_typer(docker_run_cmd, name="docker")


def main():
    commands()
