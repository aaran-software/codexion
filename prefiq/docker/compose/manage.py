from pathlib import Path

import typer
import yaml
import subprocess

def docker_run_cmd(dry_run: bool = False, recreate: bool = False, json_output: bool = False):
    typer.secho("👋 Hai from docker up", fg=typer.colors.GREEN)
    typer.echo(f"dry_run: {dry_run}")
    typer.echo(f"recreate: {recreate}")
    typer.echo(f"json_output: {json_output}")

def parse_services_from_compose(file_path: Path) -> list[str]:
    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        return list(data.get('services', {}).keys())
    except Exception as e:
        typer.echo(typer.style(f"[ERROR] Failed to parse {file_path.name}: {e}", fg=typer.colors.RED))
        return []

def show_services_preview(compose_files: list[Path]) -> list[str]:
    all_services = []
    typer.echo("\n🔍 Planned containers to run:")
    for file in compose_files:
        services = parse_services_from_compose(file)
        if services:
            typer.echo(typer.style(f"\n📦 {file.name}", fg=typer.colors.BRIGHT_BLUE))
            for svc in services:
                typer.echo(typer.style(f"   - {svc}", fg=typer.colors.GREEN))
                all_services.append(svc)
    return all_services

def run_docker_up(compose_files: list[Path]):
    cmd = ["docker", "compose"]
    for file in compose_files:
        cmd.extend(["-f", str(file)])
    cmd.append("up")
    cmd.append("-d")

    typer.echo("\n🚀 Running: " + " ".join(cmd))
    subprocess.run(cmd)
