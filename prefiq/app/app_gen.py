# prefiq/cli.py

import typer
from prefiq.commands.app.commands import reinstall, uninstall, install, list_app

app_actions = typer.Typer(help="Prefiq App Manager")

@app_actions.command("install")
def install_app(
    name: str = typer.Argument(None, help="App name to install"),
    force: bool = typer.Option(False, "--force", help="Overwrite if app exists")
):
    if not name:
        name = typer.prompt("Enter app name to install")
    install.run(name=name, force=force)


@app_actions.command("uninstall")
def uninstall_app(name: str = typer.Argument(None, help="App name to uninstall")):
    if not name:
        name = typer.prompt("Enter app name to uninstall")
    uninstall.run(name=name)


@app_actions.command("reinstall")
def reinstall_app(name: str = typer.Argument(None, help="App name to reinstall")):
    if not name:
        name = typer.prompt("Enter app name to reinstall")
    reinstall.run(name=name)


@app_actions.command("list")
def list_apps():
    list_app.run()


def run_cli():
    app_actions()


if __name__ == "__main__":
    run_cli()
