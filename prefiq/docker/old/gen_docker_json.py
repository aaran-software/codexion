import os
import json

from prefiq.utils.cprint import cprint_success

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
DOCKER_JSON_PATH = os.path.join(PROJECT_ROOT, "docker", "docker.json")
MULTI_SITES_PATH = os.path.join(PROJECT_ROOT, "prefiq", "config", "multi_sites.json")


def load_multi_sites():
    """Load the list of allowed multi-site domains from JSON."""
    if os.path.exists(MULTI_SITES_PATH):
        with open(MULTI_SITES_PATH, "r") as f:
            try:
                data = json.load(f)
                return data.get("multi_sites", {})
            except json.JSONDecodeError:
                return {}
    return {}


def safe_json_value(value):
    """Ensure value is serializable."""
    if isinstance(value, set):
        return list(value)
    elif isinstance(value, (os.PathLike,)):
        return str(value)
    return value


def gen_docker_json(key: str, file_path, domain: str = None, port: str = None):
    """
    Update docker.json with given key and value.
    If key == COMPOSE_FILE, append structured dict with domain and port.
    All others overwrite.
    """

    # multi_sites = load_multi_sites()

    # Ensure the docker directory exists
    os.makedirs(os.path.dirname(DOCKER_JSON_PATH), exist_ok=True)

    # Load docker.json if it exists
    if os.path.exists(DOCKER_JSON_PATH):
        with open(DOCKER_JSON_PATH, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    # Special case for COMPOSE_FILE
    if key == "COMPOSE_FILE" and domain:
        entry = {
            domain: safe_json_value(file_path),
            "port": str(port)
        }

        if key not in data or not isinstance(data[key], list):
            data[key] = []

        if entry not in data[key]:
            data[key].append(entry)
            cprint_success(f"docker.json updated: {key} += {entry}")
        else:
            cprint_success(f"docker.json already contains: {entry}")
    else:
        data[key] = safe_json_value(file_path)
        cprint_success(f"docker.json updated: {key} = {file_path}")

    with open(DOCKER_JSON_PATH, "w") as f:
        json.dump(data, f, indent=4)


def remove_docker_domain_entry(domain_to_remove: str):
    """Remove domain entry from docker.json COMPOSE_FILE."""
    if not os.path.exists(DOCKER_JSON_PATH):
        print("docker.json does not exist.")
        return

    with open(DOCKER_JSON_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("Invalid JSON format in docker.json")
            return

    if "COMPOSE_FILE" not in data or not isinstance(data["COMPOSE_FILE"], list):
        print("No COMPOSE_FILE section found or not a list.")
        return

    original_length = len(data["COMPOSE_FILE"])
    updated = [
        entry for entry in data["COMPOSE_FILE"]
        if not (isinstance(entry, dict) and domain_to_remove in entry)
    ]

    if len(updated) == original_length:
        print(f"No entry found for domain: {domain_to_remove}")
        return

    data["COMPOSE_FILE"] = updated

    with open(DOCKER_JSON_PATH, "w") as f:
        json.dump(data, f, indent=4)

    cprint_success(f"Removed COMPOSE_FILE entry for domain: {domain_to_remove}")
