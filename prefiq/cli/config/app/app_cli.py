import typer
from prefiq.config.generate import (
    list_apps,
    update_app_version,
    delete_app,
    add_app_to_config,
    generate_all_configs,

)

app_cmd = typer.Typer(name="app", help="Manage applications")


@app_cmd.command("init", help="Generate default config files if missing")
def init_configs():
    generate_all_configs()


@app_cmd.command("list")
def list_all_apps():
    """List all registered apps and their versions."""
    apps = list_apps()
    for name, info in apps.items():
        typer.echo(f"{name}: v{info.get('version')}")


@app_cmd.command("add")
def add_app(
    name: str = typer.Argument(None, help="App name"),
    version: str = typer.Option(None, "--version", "-v", help="App version")
):
    """
    Add a new app with version. If no arguments are provided, you'll be prompted.
    """

    if not name:
        name = typer.prompt("Enter the app name")

    if not version:
        version = typer.prompt(f"Enter the version for '{name}'")

    add_app_to_config(name, version)
    typer.echo(f"✅ App '{name}' added with version {version}.")


@app_cmd.command("delete")
def delete_app_command(name: str):
    """Delete an app from the config."""
    try:
        delete_app(name)
        typer.echo(f"App '{name}' deleted.")
    except KeyError as e:
        typer.echo(str(e))


@app_cmd.command("version")
def update_version(name: str, version: str):
    """Update version of an existing app (alias of update)."""
    try:
        update_app_version(name, version)
        typer.echo(f"Updated '{name}' to version {version}.")
    except KeyError as e:
        typer.echo(str(e))


@app_cmd.command("update")
def update_app(
        name: str,
        version: str = typer.Argument(None, help="New version for the app."),
        latest: bool = typer.Option(False, "--latest", help="Update app to latest version"),
):
    """
    Update version of an existing app.

    You can either:
    - Provide a version: `prefiq app update crm 2.0.1`
    - Or use --latest:    `prefiq app update crm --latest`
    """
    if not version and not latest:
        typer.echo("Error: Provide a version or use --latest.")
        raise typer.Exit(code=1)

    new_version = version or "latest"
    try:
        update_app_version(name, new_version)
        typer.echo(f"App '{name}' updated to version {new_version}.")
    except KeyError as e:
        typer.echo(str(e))
