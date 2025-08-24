# prefiq/cli/apps.py
from __future__ import annotations
import typer

from prefiq.apps.app_builder import new_app, drop_app, reinstall_app
from prefiq.apps.app_cfg import get_registered_apps, get_version

app = typer.Typer(help="Manage Prefiq apps (create, drop, reinstall, list)")


@app.command("new")
def cmd_new(
    name: str = typer.Argument(..., help="Name of the app to create"),
) -> None:
    """
    Create a new app skeleton under apps/<name> and register it in config/apps.cfg.
    """
    try:
        new_app(name)
        typer.echo(f"✅ App '{name}' created.")
    except Exception as e:
        typer.echo(f"❌ Failed to create '{name}': {e}")
        raise typer.Exit(code=1)


@app.command("drop")
def cmd_drop(
    name: str = typer.Argument(..., help="Name of the app to drop"),
    force: bool = typer.Option(False, "--force", "-f", help="Delete the folder if it exists"),
) -> None:
    """
    Remove apps/<name> (with --force) and unregister from config/apps.cfg.
    """
    try:
        drop_app(name, force=force)
        typer.echo(f"🗑️  App '{name}' dropped.")
    except Exception as e:
        typer.echo(f"❌ Failed to drop '{name}': {e}")
        raise typer.Exit(code=1)


@app.command("reinstall")
def cmd_reinstall(
    name: str = typer.Argument(..., help="Name of the app to reinstall"),
    force: bool = typer.Option(False, "--force", "-f", help="Force drop before reinstall"),
) -> None:
    """
    Drop (if present) and recreate apps/<name>, updating config/apps.cfg.
    """
    try:
        reinstall_app(name, force=force)
        typer.echo(f"♻️  App '{name}' reinstalled.")
    except Exception as e:
        typer.echo(f"❌ Failed to reinstall '{name}': {e}")
        raise typer.Exit(code=1)


@app.command("list")
def cmd_list() -> None:
    """
    Show apps in the same order as declared in config/apps.cfg (no sorting).
    """
    names = get_registered_apps()
    if not names:
        typer.echo("No apps registered yet.")
        return
    typer.echo("Registered apps:")
    from prefiq.apps.app_cfg import load_cfg
    cp = load_cfg()
    for n in names:
        v = get_version(cp, n) or "-"
        typer.echo(f" • {n}  (v{v})")


# expose Typer instance for main.py to mount
cli = app
