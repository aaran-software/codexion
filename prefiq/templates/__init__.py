# prefiq/__init__.py

from pathlib import Path


class CPATH:
    ROOT_DIR = Path(__file__).resolve().parent.parent
    BASE_DIR = ROOT_DIR

    APPS_DIR = ROOT_DIR / "apps"
    CORTEX_DIR = ROOT_DIR / "context"
    DB_PATH = ROOT_DIR / "database"
    DOCKER_DIR = ROOT_DIR / "docker"
    STORAGE_DIR = ROOT_DIR / "storage"
    LOG_DIR = STORAGE_DIR / "logs"


    PREFIQ_DIR = ROOT_DIR / "prefiq"
    PREFIQ_APP = ROOT_DIR / "prefiq/app"
    PREFIQ_TEMPLATE = ROOT_DIR / "prefiq/templates"
    PREFIQ_DOCKER = ROOT_DIR / "prefiq/docker"
