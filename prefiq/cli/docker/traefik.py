import typer
from prefiq.docker.prepare.traefik_compose import create_traefik_compose, delete_traefik_compose
from prefiq import CPATH
from pathlib import Path

traefik_cmd = typer.Typer(help="Manage Traefik Docker Compose files.")

@traefik_cmd.command("create")
def create(
    email: str = typer.Option(..., prompt=True, help="Email for Let's Encrypt notifications"),
    dashboard: bool = typer.Option(False, "--dashboard", help="Enable the Traefik dashboard"),
    dashboard_domain: str = typer.Option(None, help="Dashboard domain"),
    admin_user: str = typer.Option(None, help="Admin username"),
    admin_password: str = typer.Option(None, help="Admin password"),
    output: Path = typer.Option(CPATH.DOCKER_DIR, help="Output directory"),
):
    """
    Generate a docker-compose-traefik.yml file.
    """
    if dashboard:
        if not dashboard_domain:
            dashboard_domain = typer.prompt("Dashboard domain", default="")
        if not admin_user:
            admin_user = typer.prompt("Admin username", default="")
        if not admin_password:
            admin_password = typer.prompt("Admin password", hide_input=True)

    create_traefik_compose(
        email=email,
        dashboard_domain=dashboard_domain,
        admin_user=admin_user,
        admin_password=admin_password,
        output_dir=output,
    )

@traefik_cmd.command("delete")
def delete_traefik(
    output: Path = typer.Option(..., "--output", exists=True, file_okay=False, dir_okay=True),
    force: bool = typer.Option(False, "--force")
):
    """
    Delete the docker-compose-traefik.yml and related folders.
    """
    deleted = delete_traefik_compose(output)
    if deleted:
        typer.echo(f"Deleted: {', '.join(deleted)}")
    else:
        typer.echo("No files found to delete.")
