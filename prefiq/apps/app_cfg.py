# prefiq/apps/app_cfg.py

from __future__ import annotations
import os
from pathlib import Path
from configparser import ConfigParser
from typing import List, Optional
from collections import OrderedDict

from prefiq.settings.get_settings import load_settings

CFG_BASENAME = "apps.cfg"
CFG_DIRNAME  = "config"
ENV_CFG_PATH = "PREFIQ_APPS_CFG"       # absolute/relative file path wins
ENV_ROOT     = "PREFIQ_PROJECT_ROOT"   # explicit project root (folder) wins


def _project_root() -> Path:
    """
    Resolve the project root in this priority:
      1) PREFIQ_PROJECT_ROOT (env)
      2) Settings.project_root (derived from .env)
      3) CWD
    """
    # 1) explicit override
    env_root = os.getenv(ENV_ROOT)
    if env_root:
        p = Path(env_root).expanduser().resolve()
        if p.exists():
            return p

    # 2) settings-derived
    try:
        s = load_settings()
        root = getattr(s, "project_root", None)
        if root:
            return Path(root)
    except (ValueError, TypeError):
        pass

    # 3) fallback
    return Path.cwd()


def cfg_path(project_root: Path | None = None) -> Path:
    """
    Determine the path of apps.cfg in this priority:
      1) PREFIQ_APPS_CFG (env) -> treated as a file path (absolute or relative)
      2) <project_root>/config/apps.cfg
    """
    env_cfg = os.getenv(ENV_CFG_PATH)
    if env_cfg:
        p = Path(env_cfg).expanduser()
        # if relative, resolve under provided project_root (or CWD)
        if not p.is_absolute():
            base = project_root or _project_root()
            p = (base / p).resolve()
        return p
    base = project_root or _project_root()
    return (base / CFG_DIRNAME / CFG_BASENAME)


def ensure_cfg(project_root: Path | None = None) -> Path:
    p = cfg_path(project_root)
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        cp = ConfigParser(dict_type=OrderedDict)
        with p.open("w", encoding="utf-8") as f:
            cp.write(f)
    return p


def load_cfg(project_root: Path | None = None) -> ConfigParser:
    """
    Load apps.cfg preserving the section order as declared in the file.
    """
    p = ensure_cfg(project_root)
    cp = ConfigParser(dict_type=OrderedDict)
    cp.read(p, encoding="utf-8")
    return cp


def save_cfg(cp: ConfigParser, project_root: Path | None = None) -> None:
    p = cfg_path(project_root)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        cp.write(f)


# ---- minimal API (version-only sections) ----

def has_app(cp: ConfigParser, name: str) -> bool:
    return cp.has_section(name)


def add_app(cp: ConfigParser, name: str, version: str) -> None:
    if not cp.has_section(name):
        cp.add_section(name)           # appended at the end, preserving order
    cp.set(name, "version", version)


def remove_app(cp: ConfigParser, name: str) -> None:
    if cp.has_section(name):
        cp.remove_section(name)


def get_version(cp: ConfigParser, name: str) -> Optional[str]:
    try:
        return cp.get(name, "version", fallback=None)
    except (ValueError, TypeError):
        return None


def get_registered_apps(project_root: Path | None = None) -> List[str]:
    """
    Return app names in the **same order as declared** in apps.cfg.
    No sorting.
    """
    cp = load_cfg(project_root)
    return list(cp.sections())


# Small helper so the CLI can print which file is being used.
def get_cfg_abspath() -> str:
    return str(cfg_path().resolve())
