# tests/test_devmeta_migrations_sqlite.py
from __future__ import annotations

import os
from pathlib import Path
import tempfile

import pytest

from apps.devmeta.core.migrator import DevMetaMigrator
from apps.devmeta.core.helper import connect_sqlite, ensure_dir_for
from apps.devmeta.services.todo import TodoService


@pytest.fixture()
def temp_db_path(tmp_path: Path) -> str:
    dbp = tmp_path / "devmeta.sqlite"
    ensure_dir_for(str(dbp))
    return str(dbp)


@pytest.fixture()
def migrations_dir() -> str:
    from pathlib import Path
    import apps.devmeta as devmeta_pkg
    pkg_dir = Path(devmeta_pkg.__file__).resolve().parent
    mig_dir = pkg_dir / "database" / "migrations"
    assert mig_dir.exists(), f"Missing migrations dir at {mig_dir}"
    return str(mig_dir)


def test_sqlite_migrate_and_todo(temp_db_path: str, migrations_dir: str):
    # 1) Run migrations on a fresh temp DB
    migrator = DevMetaMigrator(db_path=temp_db_path, migrations_dir=migrations_dir)
    applied = migrator.migrate()
    assert applied >= 1, "Expected at least one migration to apply"

    # 2) Verify todos table exists
    with connect_sqlite(temp_db_path) as conn:
        rows = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='todos'"
        ).fetchall()
        assert rows, "todos table not found after migration"

    # 3) Use the TodoService to add/list/done
    svc = TodoService(db_path=temp_db_path, connect_fn=connect_sqlite)
    tid = svc.add("Write tests", priority=2, project="devmeta")
    assert isinstance(tid, int) and tid > 0

    rows = svc.list()
    assert any(r["id"] == tid for r in rows), "Inserted todo not found in list()"

    ok = svc.done(tid)
    assert ok, "Marking todo done failed"

    # 4) Roll back last step (if Python migration with down() exists)
    rolled = migrator.rollback(steps=1)
    # We can’t guarantee rollback > 0 if first migration was SQL,
    # but since we use m001_todos.py in DSL, expect 1
    assert rolled == 1, f"Expected 1 rolled back migration, got {rolled}"

    # 5) After rollback, todos table should be gone
    with connect_sqlite(temp_db_path) as conn:
        rows = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='todos'"
        ).fetchall()
        assert not rows, "todos table still present after rollback"

