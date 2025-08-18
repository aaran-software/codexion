import os, tempfile
from apps.devmeta.core.migrator import DevMetaMigrator
from apps.devmeta.core.helper import connect_sqlite

MIGR_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "apps", "devmeta", "database", "migrations")
)

def test_add_tags_migration_applies_and_tracks():
    with tempfile.TemporaryDirectory() as td:
        db_path = os.path.join(td, "devmeta.sqlite")

        migrator = DevMetaMigrator(db_path=db_path, migrations_dir=MIGR_DIR)
        applied = migrator.migrate()
        assert applied >= 1

        # open, check, then close explicitly
        conn = connect_sqlite(db_path)
        try:
            cols = {row["name"] for row in conn.execute("PRAGMA table_info(todos)")}
            assert "tags" in cols

            rows = conn.execute(
                "SELECT name FROM devmeta_migrations WHERE name LIKE 'm002_%'"
            ).fetchall()
            assert rows
        finally:
            conn.close()
