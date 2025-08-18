# apps/devmeta/core/migrator.py
from __future__ import annotations

import glob
import os
import importlib.util
from typing import Optional, List, Tuple

from prefiq.log.logger import get_logger
from apps.devmeta.core.helper import connect_sqlite, sha256_file

from apps.devmeta.core.migrations_state import (
    ensure_devmeta_migrations_table,
    get_applied_migration_names,
    record_migration_applied,
    DEFAULT_TABLE_NAME as MIGR_TABLE,  # or keep your existing MIGR_TABLE constant
)

LOG = get_logger("prefiq.devmeta.migrator")


# Point to apps/devmeta/database/migrations
DEFAULT_MIGRATIONS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),  # -> apps/devmeta/core/..
    "database",
    "migrations",
)


def _load_py_migration(path: str):
    spec = importlib.util.spec_from_file_location("devmeta_migration", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)  # type: ignore[attr-defined]
    return mod


class DevMetaMigrator:
    def __init__(self, db_path: str, migrations_dir: Optional[str] = None) -> None:
        self.db_path = db_path
        self.dir = migrations_dir or DEFAULT_MIGRATIONS_DIR

    # ------- discovery helpers -------

    def _discover_sql_files(self) -> list[str]:
        return sorted(glob.glob(os.path.join(self.dir, "m*.sql")))

    def _discover_py_files(self) -> list[str]:
        return sorted(glob.glob(os.path.join(self.dir, "m*.py")))

    # ------- public API -------

    def migrate(self) -> int:
        """
        Apply all pending SQL and Python-DSL migrations, in filename order.
        Returns number of migrations applied.
        """
        applied = 0
        sql_files = self._discover_sql_files()
        py_files = self._discover_py_files()

        with connect_sqlite(self.db_path) as conn:
            ensure_devmeta_migrations_table(conn, MIGR_TABLE)
            done = set(get_applied_migration_names(conn, MIGR_TABLE))

            # 1) SQL migrations
            for idx, path in enumerate(sql_files, start=1):
                name = os.path.basename(path)
                if name in done:
                    continue
                LOG.info("apply_migration", extra={"file": name, "index": idx, "type": "sql"})
                with open(path, "r", encoding="utf-8") as f:
                    sql = f.read()
                conn.executescript(sql)
                record_migration_applied(conn, name, idx, sha256_file(path), MIGR_TABLE)
                applied += 1

            # 2) Python DSL migrations (up())
            for idx, path in enumerate(py_files, start=1):
                name = os.path.basename(path)
                if name in done:
                    continue
                LOG.info("apply_migration", extra={"file": name, "index": idx, "type": "py"})
                mod = _load_py_migration(path)
                if not hasattr(mod, "up"):
                    raise AttributeError(f"{name} has no up() function")
                mod.up()
                record_migration_applied(conn, name, idx, sha256_file(path), MIGR_TABLE)
                applied += 1

            conn.commit()

        return applied

    def rollback(self, steps: int = 1) -> int:
        """
        Roll back the last `steps` applied migrations (Python migrations only).
        - Looks up most recent rows in dev_migrations.
        - For each, if a matching .py migration with down() exists, run it and delete record.
        - If only .sql exists (no automatic down), logs a warning and skips.
        Returns number of migrations rolled back.
        """
        rolled = 0
        if steps <= 0:
            return rolled

        with connect_sqlite(self.db_path) as conn:
            ensure_devmeta_migrations_table(conn, MIGR_TABLE)

            rows: List[Tuple[int, str]] = conn.execute(
                f"SELECT id, name FROM {MIGR_TABLE} ORDER BY id DESC LIMIT ?",
                (steps,),
            ).fetchall()

            if not rows:
                LOG.info("rollback_nothing_to_do")
                return 0

            for row in rows:
                # sqlite3.Row supports both index and key access; handle tuple too
                mid = row["id"] if hasattr(row, "__getitem__") and not isinstance(row, tuple) else row[0]
                name = row["name"] if hasattr(row, "__getitem__") and not isinstance(row, tuple) else row[1]

                # Try to find a corresponding .py migration and call down()
                py_path = os.path.join(self.dir, name if name.endswith(".py") else name.replace(".sql", ".py"))
                if os.path.isfile(py_path):
                    try:
                        mod = _load_py_migration(py_path)
                        if hasattr(mod, "down") and callable(mod.down):
                            LOG.info("rollback_migration", extra={"name": name, "type": "py"})
                            mod.down()
                            conn.execute(f"DELETE FROM {MIGR_TABLE} WHERE id = ?", (mid,))
                            rolled += 1
                        else:
                            LOG.warning("rollback_skip_no_down", extra={"name": name})
                    except Exception as e:
                        LOG.error("rollback_failed", extra={"name": name, "error": repr(e)})
                        raise
                else:
                    # No python migration -> we cannot auto-rollback SQL safely
                    LOG.warning("rollback_skip_sql_migration", extra={"name": name})

            conn.commit()

        return rolled
