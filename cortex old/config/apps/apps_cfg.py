import os
import configparser
from pathlib import Path

from cortex.core.settings import get_settings

CFG_PATH = Path(get_settings().project_root) / "config" / "apps.cfg"


def create_apps_cfg():
    os.makedirs(os.path.dirname(CFG_PATH), exist_ok=True)
    with open(CFG_PATH, "w") as f:
        f.write("")  # Empty file


def delete_apps_cfg():
    if os.path.exists(CFG_PATH):
        os.remove(CFG_PATH)


def get_registered_apps():
    config = configparser.ConfigParser()
    if not os.path.exists(CFG_PATH):
        return []
    config.read(CFG_PATH)
    return list(config.sections())


def add_app(app_name: str, version: str = "1.0.0"):
    config = configparser.ConfigParser()
    config.read(CFG_PATH)
    if app_name in config:
        print(f"⚠️ Docs '{app_name}' already exists. Use `update_app_version()` instead.")
    config[app_name] = {"version": version}
    with open(CFG_PATH, "w") as f:
        config.write(f)


def remove_app(app_name: str):
    config = configparser.ConfigParser()
    config.read(CFG_PATH)
    config.remove_section(app_name)
    with open(CFG_PATH, "w") as f:
        config.write(f)


def update_app_version(app_name: str, version: str):
    config = configparser.ConfigParser()
    config.read(CFG_PATH)
    if app_name not in config:
        raise ValueError(f"Docs '{app_name}' not found in apps.cfg")
    config[app_name]["version"] = version
    with open(CFG_PATH, "w") as f:
        config.write(f)
