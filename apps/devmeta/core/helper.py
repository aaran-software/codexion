# apps/devmeta/core/helper.py
from __future__ import annotations

import hashlib
import os
import sqlite3
from typing import Optional

# Default DB lives inside the app (self-contained)
DEFAULT_SQLITE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),  # apps/devmeta
    "data",
    "devmeta.sqlite",
)
ENV_SQLITE_PATH = "PREFIQ_DEV_SQLITE"
PROFILE_KEY = "devmeta"  # settings.profiles.database.devmeta


def ensure_dir_for(path: str) -> None:
    """
    Ensure the directory for a file path exists (mkdir -p).
    """
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


def resolve_sqlite_path(settings: Optional[object]) -> str:
    """
    Decide where DevMeta's SQLite DB should live.

    Precedence:
      1) Environment variable PREFIQ_DEV_SQLITE
      2) settings.profiles.database.devmeta.path (duck-typed)
      3) apps/devmeta/data/devmeta.sqlite
    """
    # 1) ENV wins
    env_path = os.getenv(ENV_SQLITE_PATH)
    if env_path:
        return env_path

    # 2) settings (works with object-like or dict-like structures)
    if settings is not None:
        # Try attribute-style first (settings.profiles.database.devmeta.path)
        try:
            profiles = getattr(settings, "profiles", None)
            database = getattr(profiles, "database", None) if profiles else None
            devmeta = getattr(database, PROFILE_KEY, None) if database else None
            path = getattr(devmeta, "path", None) if devmeta else None
            if isinstance(path, str) and path.strip():
                return path
        except Exception:
            pass

        # Try dict-style fallback (settings["profiles"]["database"]["devmeta"]["path"])
        try:
            profiles = settings["profiles"]  # type: ignore[index]
            database = profiles["database"]  # type: ignore[index]
            devmeta = database[PROFILE_KEY]  # type: ignore[index]
            path = devmeta.get("path") or ""
            if isinstance(path, str) and path.strip():
                return path
        except Exception:
            pass

    # 3) default in-repo path
    return DEFAULT_SQLITE_PATH


def connect_sqlite(db_path: str) -> sqlite3.Connection:
    """
    Open a SQLite connection with sensible PRAGMAs for a local dev tool.
    """
    ensure_dir_for(db_path)
    conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    conn.executescript(
        """
        PRAGMA journal_mode=WAL;
        PRAGMA foreign_keys=ON;
        PRAGMA synchronous=NORMAL;
        PRAGMA temp_store=MEMORY;
        """
    )
    return conn


def sha256_file(path: str) -> str:
    """
    SHA-256 hash of a file, hex-encoded.
    """
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


__all__ = [
    "DEFAULT_SQLITE_PATH",
    "ENV_SQLITE_PATH",
    "PROFILE_KEY",
    "ensure_dir_for",
    "resolve_sqlite_path",
    "connect_sqlite",
    "sha256_file",
]
