import subprocess
from pathlib import Path
from typing import List, Set

import typer


def find_compose_files(compose_dir: Path) -> List[Path]:
    """
    Scan a given directory for Docker Compose YAML files matching docker-compose-*.yml pattern.
    """
    # print(f"Searching for compose files in : {compose_dir}")

    if not compose_dir.exists() or not compose_dir.is_dir():
        raise FileNotFoundError(f"❌ Directory not found: {compose_dir}")

    compose_files = sorted(compose_dir.glob("docker-compose-*.yml"))

    if not compose_files:
        raise FileNotFoundError(f"⚠️ No compose files found in {compose_dir}")

    return compose_files
