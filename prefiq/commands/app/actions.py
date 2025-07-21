# prefiq/cli.py

import typer
from prefiq.commands.app import install, uninstall, update_app, list_app, reinstall

app = typer.Typer(help="Prefiq App Manager")

@app.command("install-app")
def install_app(
    name: str = typer.Argument(None, help="App name to install"),
    force: bool = typer.Option(False, "--force", help="Overwrite if app exists")
):
    if not name:
        name = typer.prompt("Enter app name to install")
    install.run(name=name, force=force)


@app.command("uninstall-app")
def uninstall_app(name: str = typer.Argument(None, help="App name to uninstall")):
    if not name:
        name = typer.prompt("Enter app name to uninstall")
    uninstall.run(name=name)


@app.command("reinstall-app")
def reinstall_app(name: str = typer.Argument(None, help="App name to reinstall")):
    if not name:
        name = typer.prompt("Enter app name to reinstall")
    reinstall.run(name=name)


@app.command("update-app")
def update_app_cmd(name: str = typer.Argument(None, help="App name to update")):
    if not name:
        name = typer.prompt("Enter app name to update")
    update_app.run(name=name)


@app.command("list-apps")
def list_apps():
    list_app.run()


def run_cli():
    app()


if __name__ == "__main__":
    run_cli()
