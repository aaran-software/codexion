# prefiq/cli.py
import typer

from prefiq.commands.app import actions


docker = typer.Typer()
docker.add_typer(dockit_app, name="dockit")

def main():
    actions.run_cli()
    docker()