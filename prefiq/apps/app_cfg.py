# prefiq/apps/app_cfg.py

from __future__ import annotations
import os
from pathlib import Path
from configparser import ConfigParser
from typing import List, Optional, Tuple
from collections import OrderedDict

from prefiq.settings.get_settings import load_settings

CFG_BASENAME = "apps.cfg"
CFG_DIRNAME  = "config"


# ──────────────────────────────────────────────────────────────────────────────
# Project root resolution
# Order of precedence (most explicit → least):
#  1) PREFIQ_PROJECT_ROOT env var (absolute path)
#  2) Current working directory IF ./config/apps.cfg exists
#  3) Settings.project_root IF it exists and has ./config/apps.cfg
#  4) Settings.project_root (fallback even if cfg missing)
#  5) Current working directory
# This prevents “reading a different cfg than the one I edited” problems.
# ──────────────────────────────────────────────────────────────────────────────

def _project_root() -> Path:
    # 1) explicit env override
    env_root = os.getenv("PREFIQ_PROJECT_ROOT")
    if env_root:
        p = Path(env_root).resolve()
        if p.exists():
            return p

    # 2) prefer cwd if the cfg we're looking for is right here
    cwd = Path.cwd()
    if (cwd / CFG_DIRNAME / CFG_BASENAME).exists():
        return cwd

    # 3) settings.project_root if it *contains* the cfg
    try:
        s = load_settings()
        sr = Path(getattr(s, "project_root", "") or "").resolve()
        if sr and (sr / CFG_DIRNAME / CFG_BASENAME).exists():
            return sr
        # 4) otherwise still prefer settings.project_root if present
        if sr:
            return sr
    except Exception:
        pass

    # 5) last resort
    return cwd


def cfg_path(project_root: Path | None = None) -> Path:
    return (project_root or _project_root()) / CFG_DIRNAME / CFG_BASENAME


def ensure_cfg(project_root: Path | None = None) -> Path:
    p = cfg_path(project_root)
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        # Initialize empty file, preserving order semantics via OrderedDict
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


# ---- optional helpers for nicer list output (non-breaking) ----

def registered_apps_with_versions(project_root: Path | None = None) -> List[Tuple[str, Optional[str]]]:
    """
    Convenience: [(name, version), ...] in cfg order.
    """
    cp = load_cfg(project_root)
    return [(name, get_version(cp, name)) for name in cp.sections()]


def apps_dir(project_root: Path | None = None) -> Path:
    """
    Path to the apps/ folder under the resolved project root.
    """
    return (project_root or _project_root()) / "apps"
