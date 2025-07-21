import typer

from prefiq.commands.docker.dockerfile import generate_dockerfile

dockit_app = typer.Typer(help="Docker-related utilities")

@dockit_app.command("dockfile")
def create_dockfile(
    name: str = typer.Argument(..., help="Custom Dockerfile name (e.g., cx_dockerfile)"),
):
    generate_dockerfile(
        name=name,
    )
