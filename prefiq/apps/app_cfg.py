# prefiq/apps/app_cfg.py

from __future__ import annotations
from pathlib import Path
from configparser import ConfigParser
from typing import List, Optional
from collections import OrderedDict

from prefiq.settings.get_settings import load_settings

CFG_BASENAME = "apps.cfg"
CFG_DIRNAME  = "config"


def _project_root() -> Path:
    try:
        s = load_settings()
        root = getattr(s, "project_root", None)
        if root:
            return Path(root)
    except Exception:
        pass
    return Path.cwd()


def cfg_path(project_root: Path | None = None) -> Path:
    return (project_root or _project_root()) / CFG_DIRNAME / CFG_BASENAME


def ensure_cfg(project_root: Path | None = None) -> Path:
    p = cfg_path(project_root)
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        # Initialize empty, preserving order semantics
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
    except Exception:
        return None


def get_registered_apps(project_root: Path | None = None) -> List[str]:
    """
    Return app names in the **same order as declared** in apps.cfg.
    No sorting.
    """
    cp = load_cfg(project_root)
    return list(cp.sections())
