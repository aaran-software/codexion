import shutil
from pathlib import Path

from prefiq import CPATH
from prefiq.config.manager import config_get_app, config_set_app
from prefiq.utils.cprint import cprint_success, cprint_warning, cprint_error


def run(name: str, force: bool = False):
    apps_dir: Path = CPATH.APPS_DIR
    apps_dir.mkdir(parents=True, exist_ok=True)

    app_path = apps_dir / name

    if app_path.exists():
        if force:
            shutil.rmtree(app_path)
            cprint_warning(f"[warn] Overwriting existing app '{name}'...")
        else:
            cprint_error(f"[err] App '{name}' already exists. Use --force to overwrite.")
            return

    app_path.mkdir()

    config = config_get_app()
    if name not in config.apps:
        config.apps.append(name)
        config_set_app(config)

    cprint_success(f"[ok] App '{name}' installed at apps/{name}")
