# tests/devmeta/test_devmeta_m002_add_tags.py
import os
import gc
import shutil
import sqlite3
import tempfile
from pathlib import Path

from apps.devmeta.core.migrator import DevMetaMigrator
from apps.devmeta.core.helper import connect_sqlite

MIGR_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "apps", "devmeta", "database", "migrations")
)

def test_add_tags_migration_applies_and_tracks():
    # Ensure m002 exists and will be discovered
    assert any(p.name.startswith("m002_") and p.suffix == ".py"
               for p in Path(MIGR_DIR).glob("m*.py")), f"m002 not found in {MIGR_DIR}"

    # Make our own temp dir so we control cleanup order
    td = tempfile.mkdtemp()
    try:
        db_path = os.path.join(td, "devmeta.sqlite")

        migrator = DevMetaMigrator(db_path=db_path, migrations_dir=MIGR_DIR)
        applied = migrator.migrate()
        assert applied >= 1

        # Do all DB work inside a context so the handle closes
        with connect_sqlite(db_path) as conn:
            cols = {row["name"] for row in conn.execute("PRAGMA table_info(todos)")}
            assert "tags" in cols, f"'tags' not found, columns present: {sorted(cols)}"

            rows = conn.execute(
                "SELECT name FROM devmeta_migrations WHERE name LIKE 'm002_%'"
            ).fetchall()
            assert rows, "m002 migration not recorded"

        # Extra belt-and-braces to release any shared cache handles
        sqlite3.connect(db_path).close()
        gc.collect()

        # IMPORTANT: do NOT unlink the DB explicitly on Windows.
        # Let the directory removal happen with ignore_errors=True.
    finally:
        shutil.rmtree(td, ignore_errors=True)
