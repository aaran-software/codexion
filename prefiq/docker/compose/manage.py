from pathlib import Path

import yaml
import subprocess
import typer
from pathlib import Path


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




def get_running_containers() -> set:
    result = subprocess.run(
        ["docker", "ps", "--format", "{{.Names}}"],
        capture_output=True, text=True
    )
    return set(result.stdout.strip().splitlines())


def get_services_from_compose(compose_file: Path) -> list[str]:
    result = subprocess.run(
        ["docker", "compose", "-f", str(compose_file), "config", "--services"],
        capture_output=True, text=True
    )
    return result.stdout.strip().splitlines()



def preview_services(compose_files: list[Path]):
    running = get_running_containers()
    to_start = set()

    typer.secho("\n[INFO] Planned services:", fg=typer.colors.CYAN, bold=True)

    for file in compose_files:
        typer.secho(f"  - File: {file.name}", fg=typer.colors.BLUE, bold=True)
        services = get_services_from_compose(file)

        for service in services:
            is_running = service in running
            status = "[RUNNING]" if is_running else "[STOPPED]"
            color = typer.colors.GREEN if is_running else typer.colors.RED
            typer.secho(f"      {status:<10} {service}", fg=color)
            if not is_running:
                to_start.add(service)

    return to_start





def run_docker_up(compose_files: list[Path]):
    # Filter YAML files
    valid_files = [f for f in compose_files if f.suffix in [".yml", ".yaml"]]
    if not valid_files:
        typer.secho("❌ No valid docker-compose YAML files found.", fg=typer.colors.RED)
        raise typer.Exit(1)

    # Preview what will run
    services_to_start = preview_services(valid_files)

    if not services_to_start:
        typer.secho("✅ All services already running. Nothing to do.", fg=typer.colors.GREEN)
        raise typer.Exit()

    confirm = typer.prompt(
        "\n❓ Do you want to start these containers?", default="y"
    ).strip().lower()

    if confirm not in ("y", "yes", ""):
        typer.secho("Cancelled by user.", fg=typer.colors.YELLOW)
        raise typer.Exit()

    # Build and run
    cmd = ["docker", "compose"]
    for file in valid_files:
        cmd.extend(["-f", str(file)])
    cmd += ["up", "-d"]

    typer.echo("\n Running: " + " ".join(cmd))
    subprocess.run(cmd)
    typer.secho("✅ Docker containers started.", fg=typer.colors.GREEN)

