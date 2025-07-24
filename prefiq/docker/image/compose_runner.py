import subprocess
from pathlib import Path
import typer

def compose_up_from_folder(
    folder: Path = typer.Argument(..., exists=True, file_okay=False, help="Folder containing Docker Compose .yml files")
):
    """
    Bring up all docker-compose files in the given folder.
    """
    compose_files = sorted(folder.glob("*.yml")) + sorted(folder.glob("*.yaml"))

    if not compose_files:
        typer.echo(f"[ERROR] No compose files found in: {folder}")
        raise typer.Exit(code=1)

    for file in compose_files:
        typer.echo(f"[INFO] Running: docker compose -f {file} up -d")

        try:
            subprocess.run(["docker", "compose", "-f", str(file), "up", "-d"], check=True)
        except subprocess.CalledProcessError as e:
            typer.echo(f"[ERROR] Failed to run {file.name}: {e}")
            raise typer.Exit(code=2)

    typer.echo("[SUCCESS] All Docker Compose files started successfully.")
