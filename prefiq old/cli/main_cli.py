# prefiq/cli.py
import typer

from prefiq.cli.git.update import git_sync_cmd
from prefiq.cli.cortex.server import server_cmd

commands = typer.Typer()
commands.add_typer(git_sync_cmd, name="git")
commands.add_typer(server_cmd, name="server")

def main():
    commands()
