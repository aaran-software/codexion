from __future__ import annotations
from typing import Optional
import typer

# These should be your real implementations
# prefiq/apps/app_builder.py must expose: new_app(name), drop_app(name, force), reinstall_app(name, force)
from prefiq.apps.app_builder import new_app, drop_app, reinstall_app

app_builder_cmd = typer.Typer(help="Application lifecycle commands (new, drop, reinstall)")

@app_builder_cmd.command("new")
def cmd_new(
    name: str = typer.Argument(..., help="Name of the app to create"),
) -> None:
    """
    Create a new app skeleton.
    Usage: prefiq app new <name>
    """
    try:
        new_app(name)
        typer.echo(f"✅ App '{name}' created successfully.")
    except Exception as e:
        typer.echo(f"❌ Failed to create app '{name}': {e}")
        raise typer.Exit(code=1)


@app_builder_cmd.command("drop")
def cmd_drop(
    name: str = typer.Argument(..., help="Name of the app to drop"),
    force: bool = typer.Option(False, "--force", "-f", help="Force removal without prompts"),
) -> None:
    """
    Remove an existing app (files/db/etc. as implemented by drop_app).
    Usage: prefiq app drop <name> [--force]
    """
    try:
        drop_app(name, force=force)
        typer.echo(f"🗑️  App '{name}' dropped.")
    except Exception as e:
        typer.echo(f"❌ Failed to drop app '{name}': {e}")
        raise typer.Exit(code=1)


@app_builder_cmd.command("reinstall")
def cmd_reinstall(
    name: str = typer.Argument(..., help="Name of the app to reinstall"),
    force: bool = typer.Option(False, "--force", "-f", help="Force drop before reinstall"),
) -> None:
    """
    Drop and recreate an app in one step.
    Usage: prefiq app reinstall <name> [--force]
    """
    try:
        reinstall_app(name, force=force)
        typer.echo(f"♻️  App '{name}' reinstalled.")
    except Exception as e:
        typer.echo(f"❌ Failed to reinstall app '{name}': {e}")
        raise typer.Exit(code=1)
