# apps/devmeta/provider.py
from __future__ import annotations

import os
import glob
from typing import Optional

from prefiq.log.logger import get_logger

LOG = get_logger("prefiq.devmeta.provider")

# ---------------------- Constants & Locations ----------------------

PROFILE_KEY = "devmeta"  # settings.profiles.database.devmeta
ENV_SQLITE_PATH = "PREFIQ_DEV_SQLITE"

# Default DB: apps/devmeta/data/devmeta.sqlite (self-contained)
DEFAULT_SQLITE_PATH = os.path.join(os.path.dirname(__file__), "data", "devmeta.sqlite")

# Migrations: apps/devmeta/migrations/*.sql
MIGRATIONS_DIR = os.path.join(os.path.dirname(__file__), "migrations")

# DevMeta's own migration bookkeeping table (inside SQLite)
DEV_MIGR_TABLE = "dev_migrations"


# ----------------------- Externalized Hooks ------------------------

# helpers: resolve path, ensure dir, connect sqlite, hashing, etc.
try:
    from apps.devmeta.core.helper import (
        resolve_sqlite_path,
        ensure_dir_for,
        connect_sqlite,
        sha256_file,
    )
except Exception as e:  # graceful fallback stubs
    LOG.warning("helpers_import_failed", extra={"reason": repr(e)})

    def resolve_sqlite_path(settings: Optional[object]) -> str:
        env_path = os.getenv(ENV_SQLITE_PATH)
        if env_path:
            return env_path
        # Try to read settings.profiles.database.devmeta.path (duck-typed)
        try:
            db_profiles = getattr(getattr(settings, "profiles", {}), "database", None) or settings["profiles"]["database"]
            devmeta = db_profiles.get(PROFILE_KEY) or db_profiles[PROFILE_KEY]
            return devmeta.get("path") or DEFAULT_SQLITE_PATH
        except Exception:
            return DEFAULT_SQLITE_PATH

    def ensure_dir_for(path: str) -> None:
        d = os.path.dirname(path)
        if d and not os.path.exists(d):
            os.makedirs(d, exist_ok=True)

    import sqlite3, hashlib
    def connect_sqlite(db_path: str) -> sqlite3.Connection:
        ensure_dir_for(db_path)
        conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        conn.executescript("""
            PRAGMA journal_mode=WAL;
            PRAGMA foreign_keys=ON;
            PRAGMA synchronous=NORMAL;
            PRAGMA temp_store=MEMORY;
        """)
        return conn

    def sha256_file(path: str) -> str:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

# migration bootstrap: create dev_migrations table
try:
    from apps.devmeta.database.migrations.m000_migrations_tbl import (
        ensure_devmeta_migrations_table,
    )
except Exception as e:
    LOG.warning("migration_bootstrap_import_failed", extra={"reason": repr(e)})

    def ensure_devmeta_migrations_table(conn, table_name: str = DEV_MIGR_TABLE) -> None:
        conn.executescript(f"""
            CREATE TABLE IF NOT EXISTS {table_name}(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL UNIQUE,
              order_index INTEGER NOT NULL,
              hash TEXT NOT NULL,
              applied_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)

# CLI mount hook
try:
    from apps.devmeta.cli.devmeta import mount_devmeta_cli
except Exception as e:
    LOG.warning("cli_hooks_import_failed", extra={"reason": repr(e)})

    def mount_devmeta_cli(app) -> None:
        # no-op fallback; real hook will mount Typer subapp when implemented
        LOG.info("cli_mount_skipped", extra={"reason": "devmeta cli hooks not available"})

# service bind hooks (e.g., TodoService)
try:
    from apps.devmeta.services.todo import bind_todo_service
except Exception as e:
    LOG.warning("service_hooks_import_failed", extra={"reason": repr(e)})

    def bind_todo_service(app, db_path: str) -> None:
        LOG.info("todo_service_bind_skipped", extra={"reason": "service hooks not available"})


# --------------------------- Migrator ------------------------------

class DevMetaMigrator:
    """
    File-based migrator for DevMeta (SQLite).
    - Tracks applied files in DEV_MIGR_TABLE
    - Applies *.sql from MIGRATIONS_DIR in sorted order
    """

    def __init__(self, db_path: str):
        self.db_path = db_path

    def migrate(self) -> int:
        files = sorted(glob.glob(os.path.join(MIGRATIONS_DIR, "*.sql")))
        applied = 0
        with connect_sqlite(self.db_path) as conn:
            # ensure bookkeeping table exists
            ensure_devmeta_migrations_table(conn, DEV_MIGR_TABLE)

            # get already-applied names
            done = {
                row["name"]
                for row in conn.execute(
                    f"SELECT name FROM {DEV_MIGR_TABLE} ORDER BY order_index"
                ).fetchall()
            }

            for idx, path in enumerate(files, start=1):
                name = os.path.basename(path)
                if name in done:
                    continue
                sql = open(path, "r", encoding="utf-8").read()
                LOG.info("apply_migration", extra={"file": name, "index": idx})
                conn.executescript(sql)
                conn.execute(
                    f"INSERT INTO {DEV_MIGR_TABLE}(name, order_index, hash) VALUES (?,?,?)",
                    (name, idx, sha256_file(path)),
                )
                applied += 1

            conn.commit()
        return applied


# ---------------------------- Provider -----------------------------

class DevMetaProvider:
    """
    Prefiq-style provider for the DevMeta app.
    Responsibilities:
      - Resolve SQLite path from env/settings (scoped under apps/devmeta/data by default)
      - Bind DevMeta migrator
      - Bind TodoService (via hooks)
      - Mount CLI subapp (via hooks)
    """

    def __init__(self) -> None:
        self.sqlite_path: Optional[str] = None

    def register(self, app) -> None:
        LOG.info("register_start")

        # Resolve settings (duck-typed)
        try:
            settings = app.resolve("settings")
        except Exception:
            settings = None

        # Pick SQLite path and ensure its directory exists
        path = resolve_sqlite_path(settings)
        if not path or path.strip() == "":
            path = DEFAULT_SQLITE_PATH
        ensure_dir_for(path)
        self.sqlite_path = path

        LOG.info("sqlite_path_resolved", extra={"path": self.sqlite_path})

        # Bind path for others to discover
        try:
            app.bind("devmeta.sqlite_path", self.sqlite_path)
        except Exception:
            pass

        # Bind migrator
        migrator = DevMetaMigrator(db_path=self.sqlite_path)
        try:
            app.bind("devmeta.migrator", migrator)
            LOG.info("migrator_bound")
        except Exception as e:
            LOG.error("migrator_bind_failed", extra={"error": repr(e)})

        # Bind services (Todo) via hook
        try:
            bind_todo_service(app, db_path=self.sqlite_path)
        except Exception as e:
            LOG.error("todo_service_bind_failed", extra={"error": repr(e)})

        LOG.info("register_done")

    def boot(self, app) -> None:
        LOG.info("boot_start")
        # Mount CLI (Typer) via hook if host CLI is available
        try:
            mount_devmeta_cli(app)
        except Exception as e:
            LOG.error("cli_mount_failed", extra={"error": repr(e)})
        LOG.info("boot_done")
