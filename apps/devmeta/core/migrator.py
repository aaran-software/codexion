# apps/devmeta/core/migrator.py
from __future__ import annotations

import os
import importlib.util
from pathlib import Path
from typing import Optional, List, Tuple

from prefiq.log.logger import get_logger
from apps.devmeta.core.helper import connect_sqlite, sha256_file

from apps.devmeta.core.migrations_state import (
    ensure_devmeta_migrations_table,
    get_applied_migration_names,
    record_migration_applied,
    DEFAULT_TABLE_NAME as MIGR_TABLE,
)

LOG = get_logger("prefiq.devmeta.migrator")

# Point to apps/devmeta/database/migrations
DEFAULT_MIGRATIONS_DIR = Path(__file__).resolve().parent.parent / "database" / "migrations"


def _load_py_migration(path: Path):
    spec = importlib.util.spec_from_file_location("devmeta_migration", str(path))
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader is not None
    spec.loader.exec_module(mod)  # type: ignore[attr-defined]
    return mod


def _natural_key(p: Path):
    # natural sort: m2 < m10 < m100
    import re
    return [int(t) if t.isdigit() else t.lower() for t in re.findall(r"\d+|\D+", p.name)]


class DevMetaMigrator:
    def __init__(self, db_path: str, migrations_dir: Optional[str] = None) -> None:
        self.db_path = db_path
        self.dir = Path(migrations_dir).resolve() if migrations_dir else DEFAULT_MIGRATIONS_DIR.resolve()

    # ------- discovery helpers -------

    def _candidate_dirs(self) -> List[Path]:
        """
        Probe the provided dir and a plural/singular fallback.
        """
        dirs: List[Path] = []
        if self.dir.exists():
            dirs.append(self.dir)

        alt = None
        name = self.dir.name.lower()
        if name.endswith("migrations"):
            alt = self.dir.with_name("migration")
        elif name.endswith("migration"):
            alt = self.dir.with_name("migrations")

        if alt and alt.exists():
            dirs.append(alt)

        # de-dup while preserving order
        seen = set()
        out: List[Path] = []
        for d in dirs:
            rp = d.resolve()
            if rp not in seen:
                seen.add(rp)
                out.append(rp)
        return out

    def _discover_sql_files(self) -> List[Path]:
        files: List[Path] = []
        searched = []
        for d in self._candidate_dirs():
            searched.append(str(d))
            files.extend(p for p in d.glob("m*.sql") if p.is_file())
        files = sorted({p.resolve() for p in files}, key=_natural_key)

        if not files:
            LOG.warning("no_sql_migrations_found", extra={"searched_dirs": searched})
        else:
            LOG.info("sql_migrations_found", extra={"count": len(files), "files": [p.name for p in files]})
        return files

    def _discover_py_files(self) -> List[Path]:
        files: List[Path] = []
        searched = []
        for d in self._candidate_dirs():
            searched.append(str(d))
            files.extend(
                p for p in d.glob("m*.py")
                if p.is_file() and p.name != "__init__.py"
            )
        files = sorted({p.resolve() for p in files}, key=_natural_key)

        if not files:
            LOG.warning("no_py_migrations_found", extra={"searched_dirs": searched})
        else:
            LOG.info("py_migrations_found", extra={"count": len(files), "files": [p.name for p in files]})
        return files

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
                name = path.name
                if name in done:
                    continue
                LOG.info("apply_migration", extra={"file": name, "index": idx, "type": "sql"})
                sql = path.read_text(encoding="utf-8")
                conn.executescript(sql)
                record_migration_applied(conn, name, idx, sha256_file(str(path)), MIGR_TABLE)
                applied += 1

            # 2) Python DSL migrations (up())
            for idx, path in enumerate(py_files, start=1):
                name = path.name
                if name in done:
                    continue
                LOG.info("apply_migration", extra={"file": name, "index": idx, "type": "py"})
                mod = _load_py_migration(path)
                if not hasattr(mod, "up"):
                    raise AttributeError(f"{name} has no up() function")
                # Support both up() and up(conn)
                try:
                    mod.up(conn)  # type: ignore[misc]
                except TypeError:
                    mod.up()      # type: ignore[misc]
                record_migration_applied(conn, name, idx, sha256_file(str(path)), MIGR_TABLE)
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
                mid = row["id"] if not isinstance(row, tuple) else row[0]
                name = row["name"] if not isinstance(row, tuple) else row[1]

                py_path = (self.dir / (name if name.endswith(".py") else name.replace(".sql", ".py"))).resolve()
                if py_path.is_file():
                    try:
                        mod = _load_py_migration(py_path)
                        if hasattr(mod, "down") and callable(mod.down):
                            LOG.info("rollback_migration", extra={"name": name, "type": "py"})
                            # Support down() and down(conn)
                            try:
                                mod.down(conn)  # type: ignore[misc]
                            except TypeError:
                                mod.down()      # type: ignore[misc]
                            conn.execute(f"DELETE FROM {MIGR_TABLE} WHERE id = ?", (mid,))
                            rolled += 1
                        else:
                            LOG.warning("rollback_skip_no_down", extra={"name": name})
                    except Exception as e:
                        LOG.error("rollback_failed", extra={"name": name, "error": repr(e)})
                        raise
                else:
                    LOG.warning("rollback_skip_sql_migration", extra={"name": name})

            conn.commit()

        return rolled
