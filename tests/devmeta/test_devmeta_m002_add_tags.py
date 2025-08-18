# tests/devmeta/test_devmeta_m002_add_tags.py
import os
import gc
import tempfile
from pathlib import Path

from apps.devmeta.core.migrator import DevMetaMigrator
from apps.devmeta.core.helper import connect_sqlite

MIGR_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "apps", "devmeta", "database", "migrations")
)

def test_add_tags_migration_applies_and_tracks():
    # Sanity: make sure the m002 migration file exists and is discoverable
    has_m002 = any(p.name.startswith("m002_") and p.suffix == ".py" for p in Path(MIGR_DIR).glob("m*.py"))
    assert has_m002, f"m002 migration not found in {MIGR_DIR}"

    with tempfile.TemporaryDirectory() as td:
        db_path = os.path.join(td, "devmeta.sqlite")

        migrator = DevMetaMigrator(db_path=db_path, migrations_dir=MIGR_DIR)
        applied = migrator.migrate()
        assert applied >= 1

        # Use context manager so the file handle is released even on assertion failure
        with connect_sqlite(db_path) as conn:
            cols = {row["name"] for row in conn.execute("PRAGMA table_info(todos)")}
            assert "tags" in cols, f"'tags' not found, columns present: {sorted(cols)}"

            rows = conn.execute(
                "SELECT name FROM devmeta_migrations WHERE name LIKE 'm002_%'"
            ).fetchall()
            assert rows, "m002 migration not recorded in devmeta_migrations"

        # Extra guard for Windows file locks
        gc.collect()
