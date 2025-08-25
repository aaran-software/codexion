# prefiq/cli/apps.py

from __future__ import annotations
import typer
from pathlib import Path

from prefiq.apps.app_builder import new_app, drop_app, reinstall_app  # unchanged
from prefiq.apps.app_cfg import load_cfg, get_registered_apps, get_version  # cfg is the SoT
from prefiq.apps.app_scaffold import APP_ROOT  # to check folders on disk

apps_app = typer.Typer(help="Manage Prefiq apps (create, drop, reinstall, list)")


@apps_app.command("new")
def cmd_new(
    name: str = typer.Argument(..., help="Name of the app to create"),
) -> None:
    """Create a new app skeleton under apps/<name> and register it in config/apps.cfg."""
    try:
        new_app(name)
        typer.echo(f"✅ App '{name}' created.")
    except Exception as e:
        typer.echo(f"❌ Failed to create '{name}': {e}")
        raise typer.Exit(code=1)


@apps_app.command("drop")
def cmd_drop(
    name: str = typer.Argument(..., help="Name of the app to drop"),
    force: bool = typer.Option(False, "--force", "-f", help="Delete the folder if it exists"),
) -> None:
    """Remove apps/<name> (with --force) and unregister from config/apps.cfg."""
    try:
        drop_app(name, force=force)
        typer.echo(f"🗑️  App '{name}' dropped.")
    except Exception as e:
        typer.echo(f"❌ Failed to drop '{name}': {e}")
        raise typer.Exit(code=1)


@apps_app.command("reinstall")
def cmd_reinstall(
    name: str = typer.Argument(..., help="Name of the app to reinstall"),
    force: bool = typer.Option(False, "--force", "-f", help="Force drop before reinstall"),
) -> None:
    """Drop (if present) and recreate apps/<name>, updating config/apps.cfg."""
    try:
        reinstall_app(name, force=force)
        typer.echo(f"♻️  App '{name}' reinstalled.")
    except Exception as e:
        typer.echo(f"❌ Failed to reinstall '{name}': {e}")
        raise typer.Exit(code=1)


@apps_app.command("list")
def cmd_list() -> None:
    """
    Show apps exactly in the order declared in config/apps.cfg.
    - Version is read from apps.cfg
    - Warn if an app in cfg has no corresponding folder
    - Show any on-disk app folders that are NOT registered in cfg
    """
    names = get_registered_apps()  # preserves cfg order
    cp = load_cfg()

    if not names:
        typer.echo("No apps registered yet.")
        # Still show any stray folders to help users clean up
        stray = _find_unregistered_folders(names)
        if stray:
            typer.echo("\nUnregistered app folders:")
            for n in stray:
                typer.echo(f" • {n}  (UNREGISTERED)")
        return

    typer.echo("Registered apps:")
    for n in names:
        v = get_version(cp, n) or "-"  # read version from cfg
        folder_missing = "" if (APP_ROOT / n).exists() else "  (MISSING FOLDER)"
        typer.echo(f" • {n}  (v{v}){folder_missing}")

    stray = _find_unregistered_folders(names)
    if stray:
        typer.echo("\nUnregistered app folders:")
        for n in stray:
            typer.echo(f" • {n}  (UNREGISTERED)")


def _find_unregistered_folders(registered_names: list[str]) -> list[str]:
    try:
        return sorted(
            p.name
            for p in APP_ROOT.glob("*")
            if p.is_dir() and p.name not in registered_names
        )
    except FileNotFoundError:
        return []


# expose Typer instance for main.py to mount
cli = apps_app
