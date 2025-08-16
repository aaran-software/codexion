# prefiq/__init__.py
import os

from pathlib import Path


class CPATH:
    ROOT_DIR = Path(__file__).resolve().parent.parent
    BASE_DIR = ROOT_DIR

    APPS_DIR = ROOT_DIR / "apps"
    CONFIG_DIR = ROOT_DIR / "config"
    DB_PATH = ROOT_DIR / "database"
    DOCKER_DIR = ROOT_DIR / "docker"

    CORTEX_DIR = ROOT_DIR / "context"
    STORAGE_DIR = ROOT_DIR / "storage"
    LOG_DIR = STORAGE_DIR / "logs"

    PREFIQ_DIR = ROOT_DIR / "prefiq"
    PREFIQ_APP = ROOT_DIR / "prefiq/app"
    PREFIQ_TEMPLATE = ROOT_DIR / "prefiq/templates"
    PREFIQ_DOCKER = ROOT_DIR / "prefiq/docker"

def get_root_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def get_apps_dir():
    return os.path.join(get_root_dir(), "apps")

def get_config_json() -> Path:
    return CPATH.ROOT_DIR / "config" / "app.json"

def get_app_config_path():
    return CPATH.CONFIG_DIR / "app.cfg"
