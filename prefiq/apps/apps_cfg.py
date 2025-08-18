# prefiq/apps/apps_cfg.py
from __future__ import annotations

from pathlib import Path
from typing import Iterable, List
import os

# ✅ import the function, not the module
from prefiq.settings.get_settings import load_settings

def _project_root() -> Path:
    """
    Resolve project root lazily to avoid import-time side effects.
    Prefer Settings.project_root, fallback to env or cwd.
    """
    try:
        s = load_settings()
        root = getattr(s, "project_root", None)
        if root:
            return Path(root)
    except Exception:
        pass
    return Path(os.getenv("PROJECT_ROOT", ".")).resolve()

def cfg_path() -> Path:
    return _project_root() / "config" / "apps.cfg"

def get_registered_apps() -> List[str]:
    """
    Read config/apps.cfg and return a list of enabled app names.
    Format (one per line, comments allowed with '#'):
        accounts
        billing
        # reports
    """
    p = cfg_path()
    if not p.exists():
        return []
    apps: List[str] = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        apps.append(line)
    return apps
