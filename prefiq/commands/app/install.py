import os
import json
import shutil
from prefiq.utils.path import get_apps_dir, get_config_path
from prefiq.utils.ui import *


def load_config():
    config_path = get_config_path()
    if not os.path.exists(config_path):
        return {"apps": []}
    with open(config_path, "r") as f:
        return json.load(f)


def save_config(data):
    config_path = get_config_path()
    with open(config_path, "w") as f:
        json.dump(data, f, indent=2)


def run(args):
    app_name = args.name
    force = getattr(args, "force", False)

    apps_dir = get_apps_dir()
    os.makedirs(apps_dir, exist_ok=True)

    app_path = os.path.join(apps_dir, app_name)

    if os.path.exists(app_path):
        if force:
            shutil.rmtree(app_path)
            print_warning(f"Overwriting existing app '{app_name}'")
        else:
            print_error(f"App '{app_name}' already exists. Use --force to overwrite.")
            return

    os.makedirs(app_path)

    config = load_config()
    if app_name not in config.get("apps", []):
        config["apps"].append(app_name)
        save_config(config)

    print_success(f"[ok] App '{app_name}' installed at apps/{app_name}")
