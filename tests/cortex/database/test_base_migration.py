# tests/test_base_table_migrate.py

from cortex.database.migrations.runner import migrate_module
from cortex.database.base_tables._table_list import get_base_table_files
from cortex.database.schemas.queries import select_all

def test_migrate_all_base_migrations():
    files = get_base_table_files("base")

    expected_tables = []
    for file in files:
        migrate_module(file.module, file.path)
        parts = file.path.stem.split("_", 1)
        if len(parts) == 2:
            expected_tables.append(parts[1])

    # ✅ FIXED: Query with parameters
    rows = select_all("migrations", where="app = %s", params=("base",))
    applied_migrations = [row["name"] for row in rows]

    assert applied_migrations, "❌ No base migrations recorded"

    for expected in expected_tables:
        assert expected in applied_migrations, f"❌ Expected migration not found: {expected}"

    print("✅ Base migrations applied:", applied_migrations)
