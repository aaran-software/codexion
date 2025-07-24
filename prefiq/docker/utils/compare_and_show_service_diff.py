import subprocess
from pathlib import Path
from typing import List, Set

import typer


def list_running_containers() -> Set[str]:
    result = subprocess.run(
        ["docker", "ps", "--format", "{{.Names}}"],
        capture_output=True,
        text=True,
    )
    return set(result.stdout.strip().splitlines())


def get_services_from_compose(compose_file: Path) -> List[str]:
    result = subprocess.run(
        ["docker-compose", "-f", str(compose_file), "config", "--services"],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip().splitlines()


def compare_and_show_service_diff(compose_files: List[Path]):
    running_services = list_running_containers()

    for compose_file in compose_files:
        typer.echo(f"From {compose_file.name}:")
        planned_services = get_services_from_compose(compose_file)

        for service in planned_services:
            if service in running_services:
                typer.echo(f"  [=] {service} (already running)")
            else:
                typer.echo(f"  [+] {service} (will be started)")

        # Optional: detect stopped/orphaned containers
        # related to this compose project (not in planned list)
        # You can expand this logic later if needed
