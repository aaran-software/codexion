import time
import json
import subprocess
import yaml
import typer
from pathlib import Path
from typing import List

# ─────────────────────────────────────────────────────────────
# 🔍 Compose Utilities
# ─────────────────────────────────────────────────────────────

def get_services_from_compose(compose_file: Path) -> List[str]:
    try:
        with open(compose_file) as f:
            data = yaml.safe_load(f)
        return list(data.get("services", {}).keys())
    except Exception as e:
        typer.secho(f"⚠️ Failed to parse {compose_file.name}: {e}", fg=typer.colors.RED)
        return []

def extract_images_from_compose(file_path: Path) -> List[str]:
    try:
        with open(file_path, 'r') as f:
            content = yaml.safe_load(f)
            services = content.get("services", {})
            return [svc.get("image") for svc in services.values() if "image" in svc]
    except Exception as e:
        typer.secho(f"⚠️ Failed to parse {file_path}: {e}", fg=typer.colors.RED)
        return []

# ─────────────────────────────────────────────────────────────
# 📦 Preview Services
# ─────────────────────────────────────────────────────────────

def show_services_preview(compose_files: List[Path]) -> List[tuple[str, List[str]]]:
    all_services = []
    for file_path in compose_files:
        if "dockerfile" in str(file_path).lower():
            typer.echo(f"[INFO] Skipping Dockerfile preview: {file_path}")
            continue

        try:
            with open(file_path, "r") as f:
                data = yaml.safe_load(f)
            services = data.get("services", {})
            if isinstance(services, dict):
                all_services.append((file_path.name, list(services.keys())))
            else:
                typer.echo(f"[WARN] 'services' is not a dict in {file_path}")
        except Exception as e:
            typer.echo(f"[ERROR] Failed to parse {file_path}: {e}")

    if all_services:
        typer.echo("\n🔍 Planned containers to run:\n")
        for file_name, services in all_services:
            typer.echo(f"📦 {file_name}")
            for svc in services:
                typer.echo(f"   - {svc}")
            typer.echo("")
    return all_services

# ─────────────────────────────────────────────────────────────
# 🔧 Image Handling
# ─────────────────────────────────────────────────────────────

def image_exists(image: str) -> bool:
    try:
        subprocess.run(["docker", "image", "inspect", image], capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def prompt_build_or_pull(image: str):
    typer.secho(f"🔍 Image not found: {image}", fg=typer.colors.YELLOW)
    choice = typer.prompt(f"⚙️  Do you want to [b]uild, [p]ull, or [s]kip '{image}'?", default="p")

    if choice.lower() == "b":
        default_path = Path("docker") / "Dockerfile"
        dockerfile = typer.prompt("📄 Path to Dockerfile", default=str(default_path))
        if not Path(dockerfile).exists():
            typer.secho(f"❌ Dockerfile not found at {dockerfile}", fg=typer.colors.RED)
            return
        tag = typer.prompt("🏷️ Tag for built image", default=image)
        subprocess.run(["docker", "build", "-t", tag, "-f", dockerfile, "."])

    elif choice.lower() == "p":
        subprocess.run(["docker", "pull", image])

    else:
        typer.secho(f"⏭️ Skipped image: {image}", fg=typer.colors.YELLOW)

def process_compose_file(file_path: Path):
    for image in extract_images_from_compose(file_path):
        if image and not image_exists(image):
            prompt_build_or_pull(image)

# ─────────────────────────────────────────────────────────────
# 🧪 Health Check
# ─────────────────────────────────────────────────────────────

def get_containers_from_compose(file: Path) -> List[str]:
    try:
        result = subprocess.run([
            "docker", "compose", "-f", str(file), "ps", "--format", "{{json .}}"
        ], capture_output=True, text=True, check=True)

        lines = result.stdout.strip().splitlines()
        containers = [json.loads(line) for line in lines if line.strip()]  # 👈 safer
        return [c["Name"] for c in containers]
    except Exception as e:
        typer.secho(f"❌ Failed to get containers: {e}", fg=typer.colors.RED)
        return []


import subprocess
import time
import typer
from typing import List

def wait_for_healthy(containers: List[str], timeout: int = 60):
    """
    Wait until all listed containers become healthy, or timeout.
    If no healthcheck is defined for a container, it will be skipped.
    """
    start = time.time()
    remaining = containers[:]

    while remaining and (time.time() - start < timeout):
        for name in remaining[:]:
            try:
                res = subprocess.run(
                    ["docker", "inspect", "--format", "{{.State.Health.Status}}", name],
                    capture_output=True, text=True, check=True
                )
                status = res.stdout.strip()
                if status == "healthy":
                    typer.secho(f"✅ {name} is healthy.", fg=typer.colors.GREEN)
                    remaining.remove(name)
                elif status == "unhealthy":
                    typer.secho(f"❌ {name} is unhealthy!", fg=typer.colors.RED)
                else:
                    typer.echo(f"⏳ Waiting for {name}... ({status})")
            except subprocess.CalledProcessError:
                typer.secho(f"⚠️  {name} has no healthcheck defined.", fg=typer.colors.YELLOW)
                remaining.remove(name)
        time.sleep(2)

    if remaining:
        typer.secho("⚠️ Timeout waiting for containers to become healthy:", fg=typer.colors.YELLOW)
        for name in remaining:
            typer.echo(f"  - {name}")
    else:
        typer.secho("🏁 All containers are healthy.", fg=typer.colors.CYAN)


# ─────────────────────────────────────────────────────────────
# 🚀 Main Compose Runner
# ─────────────────────────────────────────────────────────────

def run_docker_up(valid_files: List[Path], choice: str):
    if choice.lower() == "all":
        for file in valid_files:
            process_compose_file(file)

        cmd = ["docker", "compose"]
        for file in valid_files:
            cmd.extend(["-f", str(file)])
        cmd.extend(["up", "-d"])

        typer.echo(f"\n🔧 Running: {' '.join(cmd)}")
        subprocess.run(cmd)
        typer.secho("✓ Docker containers started.", fg=typer.colors.GREEN)

    else:
        for file in valid_files:
            if typer.confirm(f"\n❓ Do you want to start: {file.name}?"):
                process_compose_file(file)
                typer.echo(f"🔧 Running: docker compose -f {file} up -d")
                subprocess.run(["docker", "compose", "-f", str(file), "up", "-d"])

                containers = get_containers_from_compose(file)
                if containers:
                    typer.echo("🔍 Checking container health...")
                    wait_for_healthy(containers)
                else:
                    typer.echo("⚠️ No containers found to monitor.")

                typer.secho(f"✓ Finished: {file.name}", fg=typer.colors.GREEN)
                input("⏸️ Press Enter to continue...")
