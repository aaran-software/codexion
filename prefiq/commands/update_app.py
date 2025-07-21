from pathlib import Path
import json
from prefiq.utils.path import get_apps_dir, get_config_path

def is_app_installed(app_name: str) -> bool:
    config_path = Path(get_config_path())
    if not config_path.exists():
        return False

    with config_path.open("r") as f:
        data = json.load(f)
        return app_name in data.get("apps", [])

def run(args):
    app_name = args.name
    app_path = Path(get_apps_dir()) / app_name

    if not app_path.exists():
        print(f"[ERROR] App '{app_name}' does not exist in apps/")
        return

    if not is_app_installed(app_name):
        print(f"[WARN] App '{app_name}' is not registered as installed.")
        return

    print(f"[UPDATE] Updating app '{app_name}'...")

    update_file = app_path / "last_updated.txt"
    update_file.write_text("App updated!")

    print(f"[ok] App '{app_name}' updated successfully!", flush=True)
