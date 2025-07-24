import os
import re
import time
import json
import yaml
import subprocess
import typer

from pathlib import Path
from typing import List


# ─────────────────────────────────────────────────────────────
# 🔍 Utility: Parse and preview services from Compose files
# ─────────────────────────────────────────────────────────────

def get_services_from_compose(compose_file: Path) -> List[str]:
    try:
        with open(compose_file) as f:
            data = yaml.safe_load(f)
        return list(data.get("services", {}).keys())
    except Exception as e:
        typer.secho(f"⚠️ Failed to parse {compose_file.name}: {e}", fg=typer.colors.RED)
        return []


def show_services_preview(compose_files):
    all_services = []

    for file_path in compose_files:
        try:
            if "dockerfile" in str(file_path).lower():
                print(f"[INFO] Skipping Dockerfile preview: {file_path}")
                continue

            with open(file_path, "r") as f:
                data = yaml.safe_load(f)

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

    if all_services:
        print("\n🔍 Planned containers to run:\n")
        for file_name, services in all_services:
            print(f"📦 {file_name}")
            for svc in services:
                print(f"   - {svc}")
            print("")

    return all_services


def preview_services(compose_files: list[Path]):
    running = get_running_containers()
    to_start = set()

    typer.secho("\n[INFO] Planned services:", fg=typer.colors.CYAN, bold=True)

    for file in compose_files:
        typer.secho(f"  - File: {file.name}", fg=typer.colors.BLUE, bold=True)
        services = get_services_from_compose(file)

        for service in services:
            is_running = service in running
            status = "[✓ RUNNING]" if is_running else "[x STOPPED]"
            color = typer.colors.GREEN if is_running else typer.colors.RED
            typer.secho(f"      {status:<10} {service}", fg=color)
            if not is_running:
                to_start.add(service)

    return to_start


def get_running_containers() -> set:
    result = subprocess.run(
        ["docker", "ps", "--format", "{{.Names}}"],
        capture_output=True,
        text=True
    )
    return set(result.stdout.strip().splitlines())


# ─────────────────────────────────────────────────────────────
# 🧪 Health Checking
# ─────────────────────────────────────────────────────────────

def wait_for_healthy(containers: list[str], timeout: int = 60):
    start_time = time.time()
    remaining = containers.copy()

    while remaining and (time.time() - start_time < timeout):
        for name in remaining[:]:
            try:
                result = subprocess.run(
                    ["docker", "inspect", "--format", "{{.State.Health.Status}}", name],
                    capture_output=True,
                    text=True,
                    check=True
                )
                status = result.stdout.strip()
                if status == "healthy":
                    typer.secho(f"✅ {name} is healthy.", fg=typer.colors.GREEN)
                    remaining.remove(name)
                elif status == "unhealthy":
                    typer.secho(f"❌ {name} is unhealthy!", fg=typer.colors.RED)
                else:
                    typer.echo(f"⏳ Waiting for {name}... ({status})")
            except subprocess.CalledProcessError:
                typer.echo(f"⚠️ {name} has no healthcheck defined.")
                remaining.remove(name)
        time.sleep(2)

    if remaining:
        typer.secho("⚠️ Timeout waiting for containers to become healthy:", fg=typer.colors.YELLOW)
        for name in remaining:
            typer.echo(f"  - {name}")


def get_containers_from_compose(file: Path) -> list[str]:
    try:
        result = subprocess.run(
            ["docker", "compose", "-f", str(file), "ps", "--format", "json"],
            capture_output=True,
            text=True,
            check=True
        )
        containers = json.loads(result.stdout)
        return [container["Name"] for container in containers]
    except Exception as e:
        typer.secho(f"❌ Failed to get containers: {e}", fg=typer.colors.RED)
        return []


# ─────────────────────────────────────────────────────────────
# 🚀 Compose Execution Logic
# ─────────────────────────────────────────────────────────────

def run_compose_file(compose_file: Path):
    typer.secho(f"\n⚙️  Compose File: {compose_file.name}", fg=typer.colors.BLUE)
    confirm = typer.confirm(f"👉 Do you want to start: {compose_file.name}?", default=True)
    if not confirm:
        typer.echo("⏭️ Skipped.")
        return

    typer.echo(f"🔧 Running: docker compose -f {compose_file} up -d")
    result = subprocess.run(["docker", "compose", "-f", str(compose_file), "up", "-d"])
    if result.returncode != 0:
        typer.secho(f"❌ Error running: {compose_file.name}", fg=typer.colors.RED)
        return

    containers = get_containers_from_compose(compose_file)
    if containers:
        typer.echo("🔍 Checking container health...")
        wait_for_healthy(containers)
    else:
        typer.echo("⚠️ No containers found to monitor.")

    typer.secho(f"✓ Finished: {compose_file.name}", fg=typer.colors.GREEN)
    input("⏸️ Press Enter to continue...")


def run_docker_up(valid_files: list[Path]):
    if not valid_files:
        typer.secho("❌ No valid Docker Compose files found.", fg=typer.colors.RED)
        raise typer.Exit(1)

    typer.secho("\n📦 Planned compose files:", fg=typer.colors.CYAN)
    for file in valid_files:
        typer.echo(f"  - {file.name}")

    mode = typer.prompt(
        "\n❓ Do you want to run all at once or one by one? [all/one]",
        default="one"
    ).strip().lower()

    if mode == "all":
        cmd = ["docker", "compose"]
        for file in valid_files:
            cmd.extend(["-f", str(file)])
        cmd += ["up", "-d"]

        typer.echo("\n🚀 Running: " + " ".join(cmd))
