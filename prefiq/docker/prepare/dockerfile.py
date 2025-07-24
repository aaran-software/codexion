import subprocess
from pathlib import Path

from prefiq import CPATH
from prefiq.docker.prepare.generate_from_template import generate_from_template
from prefiq.utils.cprint import cprint_success, cprint_error, cprint_info

TEMPLATE_NAME = "dockerfile.j2"
OUTPUT_PATH = CPATH.DOCKER_DIR


def get_default_context() -> dict:
    return {
        "base_image": "ubuntu:24.04",
        "packages": ["python3", "python3-pip", "curl", "nano"],
        "cmd": "bash"
    }


def create_docker(name: str, output_dir: Path = OUTPUT_PATH)-> None:
    """Create a Dockerfile for the given app name."""
    context = get_default_context()
    output_filename = f"Dockerfile_{name}"

    generate_from_template(
        template_name=TEMPLATE_NAME,
        output_filename=output_filename,
        context=context,
        output_dir=str(output_dir),
    )

    cprint_success(f"Dockerfile written: {output_dir / output_filename}")


def update_docker(name: str, output_dir: Path = OUTPUT_PATH)-> None:
    """Remove existing Dockerfile and create a new one for the given app name."""
    output_filename = f"Dockerfile_{name}"
    output_file = OUTPUT_PATH / output_filename

    if output_file.exists():
        output_file.unlink()
        cprint_success(f"Removed: {output_file}")

    context = get_default_context()

    generate_from_template(
        template_name=TEMPLATE_NAME,
        output_filename=output_filename,
        context=context,
        output_dir=OUTPUT_PATH,
    )

    cprint_success(f"Recreated: {output_file}")


def remove_docker(name: str, output_dir: Path = OUTPUT_PATH)-> None:
    """Delete Dockerfile for the given app name."""
    output_filename = f"Dockerfile_{name}"
    output_file = OUTPUT_PATH / output_filename

    if output_file.exists():
        output_file.unlink()
        cprint_success(f"Removed: {output_file}")
    else:
        cprint_error(f"Dockerfile not found: {output_file}")


def list_dockers() -> None:
    """List all Dockerfiles in the Docker output directory."""
    dockerfiles = sorted(Path(OUTPUT_PATH).glob("Dockerfile_*"))

    if not dockerfiles:
        cprint_info("No Dockerfiles found.")
    else:
        cprint_info("Available Dockerfiles:")
        for file in dockerfiles:
            cprint_info(f" - {file.name}")


# def build_docker(name: str) -> None:
#     """Build Docker image from the generated Dockerfile."""
#     dockerfile_path = OUTPUT_PATH / f"Dockerfile_{name}"
#     image_name = f"{name.lower()}:latest"
#
#     if not dockerfile_path.exists():
#         cprint_error(f"Dockerfile does not exist: {dockerfile_path}")
#         return
#
#     try:
#         subprocess.run(
#             ["docker", "build", "-f", str(dockerfile_path), "-t", image_name, str(OUTPUT_PATH)],
#             check=True,
#         )
#         cprint_success(f"Docker image '{image_name}' built successfully.")
#     except FileNotFoundError:
#         cprint_error("Docker is not installed or not found in PATH.")
#     except subprocess.CalledProcessError:
#         cprint_error("Docker build failed.")
