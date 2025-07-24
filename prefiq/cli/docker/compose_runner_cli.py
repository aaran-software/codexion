import typer
import json
from typing import Optional
from pathlib import Path
from prefiq.docker.utils.docker_manage_services import find_compose_files

docker_run_cmd = typer.Typer()


@docker_run_cmd.command("up", help="Start Docker containers from compose files")
def up(
        dry_run: bool = typer.Option(False, "--dryrun", help="Preview actions without executing"),
        recreate: bool = typer.Option(False, "--recreate", help="Recreate compose files before running"),
        yes: bool = typer.Option(False, "--yes", "--no-input", help="Skip prompts and auto-confirm actions"),
        compose_dir: Optional[Path] = typer.Option(None, "--compose-dir", help="Directory to look for compose files"),
        output: Optional[str] = typer.Option(None, "--output", help="Output format (e.g., json)")
):
    typer.echo("👋 Hai from docker up")
    typer.echo(f"dry_run: {dry_run}")
    typer.echo(f"recreate: {recreate}")
    typer.echo(f"json_output: {output == 'json'}")

    # Ask for compose_dir if recreate is True or not provided
    if recreate and not compose_dir:
        prompt_msg = typer.style("Enter directory to recreate and scan for docker-compose files",
                                 fg=typer.colors.YELLOW)
        user_input = typer.prompt(prompt_msg, default="docker")
        compose_dir = Path(user_input).expanduser().resolve()

    # Default if still not set
    compose_dir = compose_dir or Path("docker")

    typer.echo(f"Searching compose files in: {compose_dir}")

    try:
        compose_files = find_compose_files(compose_dir)
    except Exception as e:
        typer.echo(typer.style(f"❌ {str(e)}", fg=typer.colors.RED))
        raise typer.Exit(1)

    # Output in JSON mode
    if output == "json":
        typer.echo(json.dumps({
            "compose_dir": str(compose_dir),
            "compose_files": [str(f) for f in compose_files],
            "dry_run": dry_run,
            "recreate": recreate
        }, indent=2))
    else:
        typer.echo(typer.style("[list]", fg=typer.colors.BRIGHT_CYAN) + " Compose files found:")

        for idx, file in enumerate(compose_files, start=1):
            file_str = str(file).lower()

            if "Dockerfile" in file_str:
                color = typer.colors.MAGENTA
                label = "DOCKERFILE"
            elif "compose" in file_str or "site" in file_str:
                color = typer.colors.GREEN
                label = "SITE"
            elif "mariadb" in file_str or "postgres" in file_str:
                color = typer.colors.YELLOW
                label = "DATABASE"
            elif "nginx" in file_str or "traefik" in file_str:
                color = typer.colors.CYAN
                label = "PROXY"
            else:
                color = typer.colors.MAGENTA
                label = "OTHER"

            line = f" -[{idx}] [{label}] {file}"
            typer.echo(typer.style(line, fg=color))


