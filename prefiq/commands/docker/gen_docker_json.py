import os
import json

from prefiq.utils.ui import print_success

DOCKER_JSON_PATH = os.path.join(os.path.dirname(__file__), "docker.json")
MULTI_SITES_PATH = os.path.join(os.path.dirname(__file__), "../../config/multi_sites.json")


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

    multi_sites = load_multi_sites()

    # Ensure dir exists
    os.makedirs(os.path.dirname(DOCKER_JSON_PATH), exist_ok=True)

    # Load docker.json if exists
    if os.path.exists(DOCKER_JSON_PATH):
        with open(DOCKER_JSON_PATH, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    # Special case: COMPOSE_FILE key for multi-site domains
    if key == "COMPOSE_FILE" and domain:
        entry = {
            domain: safe_json_value(file_path),
            "port": str(port)
        }

        if key not in data or not isinstance(data[key], list):
            data[key] = []

        # Avoid duplicates
        if entry not in data[key]:
            data[key].append(entry)
            print_success(f"docker.json updated: {key} += {entry}")
        else:
            print_success(f"docker.json already contains: {entry}")
    else:
        # Generic key update
        data[key] = safe_json_value(file_path)
        print_success(f"docker.json updated: {key} = {file_path}")

    # Write back
    with open(DOCKER_JSON_PATH, "w") as f:
        json.dump(data, f, indent=4)


def remove_docker_domain_entry(domain_to_remove: str):
    """
    Removes the COMPOSE_FILE entry for a specific domain.
    """
    if not os.path.exists(DOCKER_JSON_PATH):
        print(f"docker.json does not exist.")
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
    updated_list = [
        entry for entry in data["COMPOSE_FILE"]
        if not (isinstance(entry, dict) and domain_to_remove in entry)
    ]

    if len(updated_list) == original_length:
        print(f"No entry found for domain: {domain_to_remove}")
        return

    data["COMPOSE_FILE"] = updated_list

    with open(DOCKER_JSON_PATH, "w") as f:
        json.dump(data, f, indent=4)

    print_success(f"Removed COMPOSE_FILE entry for domain: {domain_to_remove}")
