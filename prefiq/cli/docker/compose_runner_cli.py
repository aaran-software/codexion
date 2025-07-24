import typer
from typing import Optional, List
from pathlib import Path
from prefiq.docker.image.compose_runner import DockerComposeManager

docker_run_cmd = typer.Typer()

@docker_run_cmd.command("up")
def up(
    sites: Optional[List[str]] = typer.Argument(None, help="Site names like site1.com"),
    recreate: bool = typer.Option(False, "--recreate", help="Recreate compose files"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview actions without running"),
    json_output: bool = typer.Option(False, "--json", help="Output in JSON format"),
):
    from prefiq.docker.image.compose_runner import DockerComposeManager

    manager = DockerComposeManager(
        sites=sites,
        recreate=recreate,
        dry_run=dry_run,
        json_output=json_output
    )
    manager.run()

