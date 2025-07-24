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

import yaml

def show_services_preview(compose_files):
    all_services = []

    for file_path in compose_files:
        try:
            if "dockerfile" in str(file_path).lower():
                # Dockerfile is not YAML – skip parsing
                print(f"[INFO] Skipping Dockerfile preview: {file_path}")
                continue

            with open(file_path, "r") as f:
                content = f.read()
                data = yaml.safe_load(content)

            if not isinstance(data, dict):
                print(f"[WARN] Ignored non-dict YAML in {file_path}")
                continue

            services = data.get("services", {})
            if isinstance(services, dict):
                all_services.append((file_path.name, list(services.keys())))
            else:
                print(f"[WARN] 'services' is not a dict in {file_path}")

        except Exception as e:
            print(f"[ERROR] Failed to parse {file_path}: {e}")

    # Pretty-print service summary
    if all_services:
        print("\n🔍 Planned containers to run:\n")
        for file_name, services in all_services:
            print(f"📦 {file_name}")
            for svc in services:
                print(f"   - {svc}")
            print("")

    return all_services


def run_docker_up(compose_files: list[Path]):
    cmd = ["docker", "compose"]
    for file in compose_files:
        cmd.extend(["-f", str(file)])
    cmd.append("up")
    cmd.append("-d")

    typer.echo("\n🚀 Running: " + " ".join(cmd))
    subprocess.run(cmd)
