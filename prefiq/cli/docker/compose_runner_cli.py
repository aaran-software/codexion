from pathlib import Path
from typing import Optional

import typer
from prefiq.docker.utils.docker_checks import is_docker_running
from prefiq.docker.utils.find_compose_files import find_compose_files
from prefiq.docker.utils.preview_compose_services import preview_compose_services
from prefiq.docker.utils.recreate_compose_files import recreate_compose_files
from prefiq.docker.utils.start_docker_services import start_docker_services
from prefiq.docker.utils.compare_and_show_service_diff import compare_and_show_service_diff

docker_run_cmd = typer.Typer()

@docker_run_cmd.command("up")
def up(
    dryrun: bool = typer.Option(False, "--dryrun", help="Show planned actions without executing"),
    recreate: bool = typer.Option(False, "--recreate", help="Recreate compose files"),
    yes: bool = typer.Option(False, "--yes", "--no-input", help="Auto-confirm all prompts"),
    json_output: bool = typer.Option(False, "--json-output", help="Output result in JSON format"),
    compose_dir: Optional[Path] = typer.Option(None, "--compose-dir", help="Directory to scan for docker-compose files"),
):
    print("Hai from docker up")
    print(f"dry_run: {dryrun}")
    print(f"recreate: {recreate}")
    print(f"json_output: {json_output}")

    # Ask for compose_dir if not provided
    if compose_dir is None:
        prompt_msg = typer.style("Enter directory to scan for docker-compose files", fg=typer.colors.YELLOW)
        user_input = typer.prompt(prompt_msg, default=".")
        compose_dir = Path(user_input).expanduser().resolve()

    # Check if Docker is running
    if not is_docker_running():
        typer.echo("Docker is not running. Please start Docker and try again.")
        raise typer.Exit(code=1)

    # --- Dry Run Mode ---
    if dryrun:
        if yes or typer.confirm(
            typer.style("Do you want to recreate the compose files before dry run?", fg=typer.colors.YELLOW),
            default=False
        ):
            typer.echo("Starting recreate compose files")
            recreate_compose_files()

        typer.echo("finding compose files")
        compose_files = find_compose_files(compose_dir)
        if not compose_files:
            typer.echo("No compose files found.")
            raise typer.Exit(code=1)

        typer.echo("previewing compose files")
        preview_compose_services(compose_files, json_output=json_output)

        if not yes and not typer.confirm(
            typer.style("Proceed with this dry run summary?", fg=typer.colors.YELLOW),
            default=True
        ):
            typer.echo("Aborted by user.")
            raise typer.Exit()
        return

    # --- Actual Execution ---
    if recreate:
        typer.echo("Recreating compose files...")
        recreate_compose_files()

    compose_files = find_compose_files(compose_dir)
    if not compose_files:
        typer.echo("No compose files found. Use --recreate to generate them.")
        raise typer.Exit(code=1)

    # Show diff between planned services and running containers
    compare_and_show_service_diff(compose_files)

    if not yes and not typer.confirm(
        typer.style("Proceed to start the containers?", fg=typer.colors.YELLOW),
        default=True
    ):
        typer.echo("Aborted by user.")
        raise typer.Exit()

    start_docker_services(compose_files)
