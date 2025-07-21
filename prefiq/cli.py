# prefiq/cli.py
import typer

from prefiq.commands.app.app_gen import app_actions
from prefiq.commands.git.git_gen import git_actions
from prefiq.commands.docker.docker_gen import docker_actions

docker = typer.Typer()
docker.add_typer(app_actions, name="app", help="Docker commands")
docker.add_typer(docker_actions, name="docker", help="Docker commands")
docker.add_typer(git_actions, name="git", help="Git commands")


def main():
    docker()
