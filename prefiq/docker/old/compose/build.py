import json
import subprocess
from pathlib import Path
from typing import Optional
from prefiq.commands.utils.ui import print_success, print_error

DOCKER_JSON_PATH = Path("docker/docker.json")


def run_build(name: Optional[str], push: bool = False, tag: Optional[str] = None):
    """
    Build Docker image(s) based on docker.json or a specific name.
    """
    if not DOCKER_JSON_PATH.exists():
        print_error("❌ docker.json not found.")
        return

    with open(DOCKER_JSON_PATH) as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            print_error("❌ Invalid docker.json format.")
            return

    images = []
    if name:
        image_tag = tag or f"{name}:latest"
        images.append((name, image_tag))
    else:
        # Get all top-level keys that look like image names
        for key in config.get("IMAGES", {}):
            image_tag = config["IMAGES"][key].get("tag", f"{key}:latest")
            images.append((key, tag or image_tag))

    for img_name, img_tag in images:
        dockerfile = Path(f"docker/{img_name}/Dockerfile")
        if not dockerfile.exists():
            print_error(f"❌ Dockerfile not found for {img_name}")
            continue

        build_cmd = ["docker", "build", "-t", img_tag, str(dockerfile.parent)]
        print_success(f"🔨 Running: {' '.join(build_cmd)}")
        subprocess.run(build_cmd, check=True)

        if push:
            push_cmd = ["docker", "push", img_tag]
            print_success(f"📤 Pushing: {img_tag}")
            subprocess.run(push_cmd, check=True)
