import subprocess
from pathlib import Path

from prefiq import CPATH
from prefiq.docker.common.generate_from_template import generate_from_template
from prefiq.utils.cprint import cprint_success, cprint_error, cprint_info

TEMPLATE_NAME = "dockerfile.j2"
DEFAULT_OUTPUT_PATH = CPATH.DOCKER_DIR


def get_default_context() -> dict:
    return {
        "base_image": "ubuntu:24.04",
        "packages": ["python3", "python3-pip", "curl", "nano"],
        "cmd": "bash"
    }


def create_docker(output_dir: Path = DEFAULT_OUTPUT_PATH) -> None:
    """Create a Dockerfile for the given app name."""
    context = get_default_context()
    output_filename = f"Dockerfile"
    output_path = output_dir / output_filename

    generate_from_template(
        template_name=TEMPLATE_NAME,
        output_filename=output_filename,
        context=context,
        output_dir=str(output_dir),
    )

    cprint_success(f"Dockerfile written: {output_path}")

def remove_docker(name: str, output_dir: Path = DEFAULT_OUTPUT_PATH) -> None:
    """Delete Dockerfile for the given app name."""
    output_filename = f"Dockerfile"
    output_path = output_dir / output_filename

    if output_path.exists():
        output_path.unlink()
        cprint_success(f"Removed: {output_path}")
    else:
        cprint_error(f"Dockerfile not found: {output_path}")
