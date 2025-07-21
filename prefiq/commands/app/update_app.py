from pathlib import Path
import json
from prefiq.utils.path import get_apps_dir, get_config_path
from prefiq.utils.ui import print_warning, print_success


def is_app_installed(app_name: str) -> bool:
    config_path = Path(get_config_path())
    if not config_path.exists():
        return False

    with config_path.open("r") as f:
        data = json.load(f)
        return app_name in data.get("apps", [])


def run(name: str):
    app_path = Path(get_apps_dir()) / name

    if not app_path.exists():
        print_warning(f"App '{name}' does not exist in apps/")
        return

    if not is_app_installed(name):
        print_warning(f"App '{name}' is not registered as installed.")
        return

    print_success(f"Updating app '{name}'...")

    update_file = app_path / "last_updated.txt"
    update_file.write_text("App updated!")

    print(f"[ok] App '{name}' updated successfully!", flush=True)
