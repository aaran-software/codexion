# prefiq/cli/docker/compose_action.py

import typer
from prefiq.docker.prepare.site_compose import create_site_compose, remove_site_compose, list_compose_files
from prefiq.docker.prepare.mariadb_compose import create_mariadb_compose
from prefiq.docker.prepare.postgres_compose import create_postgres_compose

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

    create_site_compose(domain, port)
    typer.echo(f"Docker Compose file for '{domain}' created successfully.")


@compose_cmd.command("remove")
def remove(
        domain: str = typer.Argument(None, help="Domain name of Compose file to remove")
):
    """Remove the Docker Compose file for the given domain."""
    if not domain:
        domain = typer.prompt("Compose file name (domain)")

    remove_site_compose(domain)
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


@compose_cmd.command("mariadb")
def mariadb(
    database: str = typer.Option(None, "--database", "-d", help="Database name (e.g. codexion_db)"),
    port: int = typer.Option(None, "--port", "-p", help="Port number (e.g. 3606)")
):
    """Create a Docker Compose file for MariaDB with given database and port."""
    if database is None:
        database = typer.prompt("Enter database name", default="codexion_db")
    if port is None:
        port = typer.prompt("Enter port number", type=int, default=3606)

    create_mariadb_compose(database, port)
    typer.echo(f"Docker Compose file for MariaDB '{database}' created on port {port}.")


@compose_cmd.command("postgres")
def postgres(
    database: str = typer.Option(None, "--database", "-d", help="Database name (e.g. codexion_pg)"),
    port: int = typer.Option(None, "--port", "-p", help="Port number (e.g. 5432)")
):
    """Create a Docker Compose file for PostgresSQL with given database and port."""
    if database is None:
        database = typer.prompt("Enter database name", default="codexion_pg")
    if port is None:
        port = typer.prompt("Enter port number", type=int, default=5432)

    create_postgres_compose(database, port)
    typer.echo(f"Docker Compose file for PostgresSQL '{database}' created on port {port}.")
