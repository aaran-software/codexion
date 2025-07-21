from pathlib import Path
import json
import shutil
from prefiq.utils.path import get_apps_dir, get_config_path
from prefiq.utils.ui import print_success, print_warning, print_info


def load_config() -> dict:
    config_path = Path(get_config_path())
    if not config_path.exists():
        return {"apps": []}
    with config_path.open("r") as f:
        return json.load(f)


def save_config(data: dict):
    config_path = Path(get_config_path())
    with config_path.open("w") as f:
        json.dump(data, f, indent=2)


def run(args):
    app_name = args.name
    app_path = Path(get_apps_dir()) / app_name

    if not app_path.exists():
        print_warning(f"App '{app_name}' does not exist in apps/")
        return

    shutil.rmtree(app_path)

    config = load_config()
    if app_name in config.get("apps", []):
        config["apps"].remove(app_name)
        save_config(config)

    print_info(f"App '{app_name}' uninstalled successfully.")
