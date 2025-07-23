# prefiq/cli/docker/compose_action.py

import typer
from prefiq.docker.prepare.composefile import create_compose, remove_compose, list_compose_files

compose_cmd = typer.Typer(help="Docker Compose-related commands")


@compose_cmd.command("create")
def create(
        domain: str = typer.Argument(None, help="Domain name (e.g. sundar.com)"),
        port: int = typer.Argument(None, help="Port number (e.g. 8000)")
):
    """Create a Docker Compose file for the given domain and port."""
    if not domain:
        domain = typer.prompt("Compose file name (domain)")
    if not port:
        port = typer.prompt("Port", type=int)

    create_compose(domain, port)
    typer.echo(f"Docker Compose file for '{domain}' created successfully.")


@compose_cmd.command("remove")
def remove(
        domain: str = typer.Argument(None, help="Domain name of Compose file to remove")
):
    """Remove the Docker Compose file for the given domain."""
    if not domain:
        domain = typer.prompt("Compose file name (domain)")

    remove_compose(domain)
    typer.echo(f"Docker Compose file for '{domain}' removed successfully.")


@compose_cmd.command("list")
def list_all():
    """List all Docker Compose files"""
    files = list_compose_files()
    if not files:
        typer.echo("No Compose files found.")
    else:
        typer.echo("Docker Compose files:")
        for file in files:
            typer.echo(f"- {file}")
