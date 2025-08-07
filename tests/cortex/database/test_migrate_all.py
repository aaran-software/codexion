# # tests/test_migrate_all.py
#
from cortex.database.connection import db
from cortex.database.migrations.runner import drop_all, migrate_all
from cortex.database.schemas.queries import count, select_all
#
#
def test_migrate_all_table():
    # 1. Ensure clean state
    drop_all()

    # 2. Run all migrations
    migrate_all()

    # 3. Check if 'migrations' system table exists
    result = db.fetchone("SHOW TABLES LIKE 'migrations'")
    assert result is not None, "❌ 'migrations' table was not created."
    print("✅ 'migrations' table created.")

    # 4. Check migration rows exist
    total = count("migrations")
    assert total > 0, "❌ No migrations were recorded."
    print(f"✅ {total} migrations were recorded.")

    # 5. Optional: print first few for manual inspection
    recent = select_all("migrations", "app, name, order_index")
    for row in recent:
        print(f"🧩 Migration applied → App: {row[0]}, Name: {row[1]}, Order: {row[2]}")
