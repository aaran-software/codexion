# prefiq/cli.py

import typer
from prefiq.commands.app.commands import install

git_actions = typer.Typer(help="App Git Manager")

@git_actions.command("install")
def install_git(
    name: str = typer.Argument(None, help="App name to install"),
    force: bool = typer.Option(False, "--force", help="Overwrite if app exists")
):
    if not name:
        name = typer.prompt("Enter app name to install")
    install.run(name=name, force=force)
