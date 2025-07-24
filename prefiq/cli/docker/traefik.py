import typer
from pathlib import Path
from typing import Optional

from prefiq.docker.prepare.traefik_compose import create_traefik_compose, delete_traefik_compose

traefik_cmd = typer.Typer(help="Manage Traefik Docker Compose")


@traefik_cmd.command("create", help="Generate Traefik Docker Compose")
def create(
    email: Optional[str] = typer.Option ("info@admin.com",  "--email", "-e", help="Email for Let's Encrypt"),
    dashboard_domain: Optional[str] = typer.Option(None, "--dashboard-domain", "-d", help="Domain for Traefik dashboard (optional)"),
    admin_user: Optional[str] = typer.Option(None, "--admin-user", "-u", help="Dashboard admin username (optional)"),
    admin_password: Optional[str] = typer.Option(None, "--admin-password", "-p", hide_input=True, confirmation_prompt=True, help="Dashboard admin password (optional)"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Directory to write the file (default: docker/)"),
):
    """
    Generate a docker-compose-traefik.yml with optional dashboard and basic auth.
    """
    if dashboard_domain and not admin_user:
        admin_user = typer.prompt("Dashboard admin username")
    if dashboard_domain and not admin_password:
        admin_password = typer.prompt("Dashboard admin password", hide_input=True, confirmation_prompt=True)
    if not output:
        output = typer.prompt("Output directory", default="docker", type=Path)

    create_traefik_compose(
        email=email,
        dashboard_domain=dashboard_domain,
        admin_user=admin_user,
        admin_password=admin_password,
        output_dir=output,
    )


@traefik_cmd.command("delete", help="Delete generated Traefik files")
def delete(
    output: Path = typer.Option(..., "--output", "-o", help="Directory where Traefik files are located"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation prompt"),
):
    """
    Delete docker-compose-traefik.yml and optional folders like 'letsencrypt' and 'dynamic'.
    """
    if not force:
        typer.confirm(f"Are you sure you want to delete files in {output}?", abort=True)

    deleted = delete_traefik_compose(output)
    if deleted:
        typer.echo(f"[OK] Deleted: {', '.join(deleted)}")
    else:
        typer.echo("[INFO] No files found to delete.")

