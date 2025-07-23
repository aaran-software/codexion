# prefiq/commands/app/uninstall.py

import os
import shutil
import json
from prefiq import get_apps_dir,get_config_path
from prefiq.utils.cprint import cprint_success, cprint_error


def run(name: str):
    app_path = os.path.join(get_apps_dir(), name)
    if not os.path.exists(app_path):
        cprint_error(f"App '{name}' not found.")
        return

    shutil.rmtree(app_path)

    config_path = get_config_path()
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
        if name in config.get("apps", []):
            config["apps"].remove(name)
            with open(config_path, "w") as f:
                json.dump(config, f, indent=2)

    cprint_success(f"App '{name}' uninstalled.")
