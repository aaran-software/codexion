import typer
from typing import Optional
from prefiq.docker.prepare.create import dockerfile

docker_actions = typer.Typer(help="Prefiq Docker commands")


# ------------------ Create Dockerfile ------------------
@docker_actions.command("create", help="Generate a Dockerfile for your app.")
def create_dockerfile(name: Optional[str] = typer.Argument(None, help="Dockerfile name (e.g., app)")):
    """
    Generate a Dockerfile for your app.

    Usage: `prefiq docker create` or `prefiq docker create sundar`
    """
    if not name:
        name = typer.prompt("Dockerfile name (e.g., app)")
    dockerfile(name=name)