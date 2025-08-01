# prefiq/cli.py
import typer
from prefiq.cli.context import get_codexion_root

CODEXION_HOME = get_codexion_root()

from prefiq.cli.apps import app_cli
from prefiq.cli.config.commands import config_cli
from prefiq.cli.docker.prepare.dockerfile_action import docker_cmd
from prefiq.cli.docker.prepare.compose_action import compose_cmd
from prefiq.cli.docker.prepare.traefik import traefik_cmd
from prefiq.cli.docker.prepare.gen_dockit_cli import generate_cmd
from prefiq.cli.docker.compose.compose_runner_cli import docker_run_cmd
from prefiq.cli.git.update import git_sync_cmd
from prefiq.cli.cortex.server import server_cmd

commands = typer.Typer()
commands.add_typer(app_cli.app_cmd, name="app")
commands.add_typer(config_cli, name="config")
commands.add_typer(docker_cmd, name="dockfile")
commands.add_typer(compose_cmd, name="compose-site")
commands.add_typer(traefik_cmd, name="traefik")
commands.add_typer(generate_cmd, name="generate")
commands.add_typer(docker_run_cmd, name="docker")
commands.add_typer(git_sync_cmd, name="git")
commands.add_typer(server_cmd, name="server")


def main():
    commands()
