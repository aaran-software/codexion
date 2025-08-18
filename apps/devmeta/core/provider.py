# apps/devmeta/provider.py
from __future__ import annotations

import os, sys, importlib, pkgutil, inspect, hashlib
from dataclasses import dataclass
from typing import Optional, List, Tuple

from prefiq.log.logger import get_logger
LOG = get_logger("prefiq.devmeta.provider")

# ---------------------- Constants & Locations ----------------------

PROFILE_KEY = "devmeta"                     # settings.profiles.database.devmeta
ENV_SQLITE_PATH = "PREFIQ_DEV_SQLITE"       # optional override for DB file
DEFAULT_SQLITE_PATH = os.path.join(os.path.dirname(__file__), "data", "devmeta.sqlite")

# Python migration package (not .sql files)
MIGRATIONS_PKG = "apps.devmeta.database.migrations"
DEV_MIGR_TABLE = "dev_migrations"           # bookkeeping table inside DevMeta sqlite

# ----------------------- Externalized Hooks ------------------------

try:
    from apps.devmeta.core.helper import (
        resolve_sqlite_path,
        ensure_dir_for,
        connect_sqlite,
    )
except Exception as e:
    LOG.warning("helpers_import_failed", extra={"reason": repr(e)})

    def resolve_sqlite_path(settings: Optional[object]) -> str:
        env_path = os.getenv(ENV_SQLITE_PATH)
        if env_path:
            return env_path
        try:  # settings.profiles.database.devmeta.path (duck-typed)
            db_profiles = getattr(getattr(settings, "profiles", {}), "database", None) or settings["profiles"]["database"]
            devmeta = db_profiles.get(PROFILE_KEY) or db_profiles[PROFILE_KEY]
            return devmeta.get("path") or DEFAULT_SQLITE_PATH
        except Exception:
            return DEFAULT_SQLITE_PATH

    def ensure_dir_for(path: str) -> None:
        d = os.path.dirname(path)
        if d and not os.path.exists(d):
            os.makedirs(d, exist_ok=True)

    import sqlite3
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

# CLI mount (optional)
try:
    from apps.devmeta.cli.devmeta import mount_devmeta_cli
except Exception as e:
    LOG.warning("cli_hooks_import_failed", extra={"reason": repr(e)})

    def mount_devmeta_cli(app) -> None:
        LOG.info("cli_mount_skipped", extra={"reason": "devmeta cli hooks not available"})

# Todo service (optional)
try:
    from apps.devmeta.services.todo import bind_todo_service
except Exception as e:
    LOG.warning("service_hooks_import_failed", extra={"reason": repr(e)})

    def bind_todo_service(app, db_path: str) -> None:
        LOG.info("todo_service_bind_skipped", extra={"reason": "service hooks not available"})

# --------------------------- Migration utils -----------------------

def _sha256_file(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def _ensure_migrations_table(conn, table: str = DEV_MIGR_TABLE) -> None:
    """
    Always ensure the bookkeeping table exists.
    SQLite DDL used here is accepted by SQLite; for DevMeta we only use SQLite locally.
    """
    conn.executescript(f"""
        CREATE TABLE IF NOT EXISTS {table}(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL UNIQUE,
          order_index INTEGER NOT NULL,
          hash TEXT NOT NULL,
          applied_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        CREATE UNIQUE INDEX IF NOT EXISTS ux_{table}_name ON {table}(name);
        CREATE INDEX IF NOT EXISTS ix_{table}_order ON {table}(order_index);
    """)

@dataclass(frozen=True)
class PyMigration:
    name: str
    order_index: int
    module: object
    file_path: Optional[str]

def _discover_py_migrations() -> List[PyMigration]:
    """
    Discover Python migration modules in MIGRATIONS_PKG.
    A valid migration defines: up() and down().
    Order is by module filename: mXXXX_*.py
    """
    spec = importlib.util.find_spec(MIGRATIONS_PKG)
    if spec is None or not getattr(spec, "submodule_search_locations", None):
        LOG.info("migrations_pkg_missing", extra={"pkg": MIGRATIONS_PKG})
        return []

    pkg_dir = list(spec.submodule_search_locations)[0]
    out: List[PyMigration] = []
    for finder, modname, ispkg in pkgutil.iter_modules([pkg_dir]):
        if ispkg:
            continue
        if not (modname.startswith("m") and modname[1:5].isdigit()):
            continue

        fq = f"{MIGRATIONS_PKG}.{modname}"
        try:
            mod = importlib.import_module(fq)
        except Exception as e:
            LOG.warning("migration_import_failed", extra={"module": fq, "reason": repr(e)})
            continue

        up = getattr(mod, "up", None)
        down = getattr(mod, "down", None)
        if not callable(up) or not callable(down):
            LOG.warning("migration_missing_ud", extra={"module": fq})
            continue

        # Try to get file path for hashing
        file_path = None
        try:
            file_path = inspect.getsourcefile(mod)
        except Exception:
            pass

        # Extract numeric order from filename prefix mXXXX_...
        try:
            order = int(modname[1:5])
        except Exception:
            order = 0

        out.append(PyMigration(name=modname + ".py", order_index=order, module=mod, file_path=file_path))

    out.sort(key=lambda m: (m.order_index, m.name))
    return out

# ---------------------------- Migrator -----------------------------

class DevMetaMigrator:
    """
    Python-file migrator for DevMeta.
    - Tracks applied files in DEV_MIGR_TABLE
    - Applies modules from apps.devmeta.database.migrations in sorted order
    """
    def __init__(self, db_path: str):
        self.db_path = db_path

    def migrate(self) -> int:
        applied = 0
        with connect_sqlite(self.db_path) as conn:
            _ensure_migrations_table(conn, DEV_MIGR_TABLE)

            done = {
                row["name"]
                for row in conn.execute(
                    f"SELECT name FROM {DEV_MIGR_TABLE} ORDER BY order_index"
                ).fetchall()
            }

            migrations = _discover_py_migrations()
            for mig in migrations:
                if mig.name in done:
                    continue
                LOG.info("apply_migration", extra={"file": mig.name, "index": mig.order_index})
                # Run migration
                mig.module.up()
                # Hash (best effort)
                h = _sha256_file(mig.file_path) if mig.file_path and os.path.exists(mig.file_path) else "NA"
                conn.execute(
                    f"INSERT INTO {DEV_MIGR_TABLE}(name, order_index, hash) VALUES (?,?,?)",
                    (mig.name, mig.order_index, h),
                )
                applied += 1

            conn.commit()
        return applied

    def rollback(self, steps: int = 1) -> int:
        """
        Roll back N applied migrations in reverse order by calling down().
        """
        rolled = 0
        steps = max(0, int(steps or 0))
        if steps == 0:
            return 0

        with connect_sqlite(self.db_path) as conn:
            _ensure_migrations_table(conn, DEV_MIGR_TABLE)
            rows = conn.execute(
                f"SELECT name, order_index FROM {DEV_MIGR_TABLE} ORDER BY order_index DESC"
            ).fetchall()

            by_name = {m.name: m for m in _discover_py_migrations()}
            for row in rows:
                if rolled >= steps:
                    break
                name, order_index = row["name"], row["order_index"]
                mig = by_name.get(name)
                if not mig:
                    LOG.warning("rollback_missing_module", extra={"name": name})
                    # Still remove record to unblock future migrations
                    conn.execute(f"DELETE FROM {DEV_MIGR_TABLE} WHERE name = ?", (name,))
                    rolled += 1
                    continue

                LOG.info("rollback_migration", extra={"file": name, "index": order_index})
                mig.module.down()
                conn.execute(f"DELETE FROM {DEV_MIGR_TABLE} WHERE name = ?", (name,))
                rolled += 1

            conn.commit()
        return rolled

# ---------------------------- Provider -----------------------------

class DevMetaProvider:
    """
    Prefiq-style provider for DevMeta (SQLite local DB + Python migrations).
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
        path = resolve_sqlite_path(settings) or DEFAULT_SQLITE_PATH
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

        # Optional services
        try:
            bind_todo_service(app, db_path=self.sqlite_path)
        except Exception as e:
            LOG.error("todo_service_bind_failed", extra={"error": repr(e)})

        LOG.info("register_done")

    def boot(self, app) -> None:
        LOG.info("boot_start")
        try:
            mount_devmeta_cli(app)
        except Exception as e:
            LOG.error("cli_mount_failed", extra={"error": repr(e)})
        LOG.info("boot_done")
