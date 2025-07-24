import subprocess
import typer
from pathlib import Path

docker_run_cmd = typer.Typer()

@docker_run_cmd.command("up", help="Start all Docker services from compose files in the given folder")
def compose_up_from_folder(
    folder: Path = typer.Option(
        Path("docker"), "--folder", "-f",
        file_okay=False,
        readable=True,
        help="Folder containing Docker Compose YAML files (default: ./docker)"
    )
):
    """
    Runs `docker compose -f <file> up -d` for each .yml/.yaml file in the folder.
    """
    if not folder.exists():
        typer.secho(f"❌ Folder '{folder}' does not exist.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    compose_files = sorted([f for f in folder.iterdir() if f.is_file() and f.suffix in [".yml", ".yaml"]])

    if not compose_files:
        typer.secho("❌ No Docker Compose YAML files found in the folder.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    for compose_file in compose_files:
        typer.secho(f"🔧 Running: docker compose -f {compose_file.name} up -d", fg=typer.colors.CYAN)
        try:
            result = subprocess.run(
                ["docker", "compose", "-f", str(compose_file), "up", "-d"],
                check=True,
                capture_output=True,
                text=True,
            )
            typer.secho(result.stdout.strip(), fg=typer.colors.GREEN)
        except subprocess.CalledProcessError as e:
            typer.secho(f"❌ Failed to start: {compose_file.name}", fg=typer.colors.RED)
            typer.secho(e.stderr.strip(), fg=typer.colors.RED)
            raise typer.Exit(code=2)

    typer.secho("✅ All Docker Compose services started successfully!", fg=typer.colors.GREEN)
