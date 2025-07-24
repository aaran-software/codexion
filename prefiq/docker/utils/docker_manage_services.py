import subprocess
from pathlib import Path
from typing import List, Set

import typer

def find_compose_files(compose_dir: Path):
    if not compose_dir.exists() or not compose_dir.is_dir():
        raise FileNotFoundError(f"Compose directory not found: {compose_dir}")

    return sorted(compose_dir.glob("**/docker*.yml")) + sorted(compose_dir.glob("**/Dockerfile*"))
