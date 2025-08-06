# tests/test_create_users_table.py

# from cortex.database.connection import db
# from cortex.database.migrations.runner import migrate_all


# def test_create_users_table():
#     drop_migrate("001_users")
#
#     migrate_table("001_users")
#
#     # Verify if table now exists
#     result = db.fetchone("SHOW TABLES LIKE 'users'")
#     assert result is not None, "❌ 'users' table was not created."
#     print("✅ 'users' table created successfully.")


# def test_create_all_table():
#     drop_all_migrate()
#
#     migrate_all_table()
#
#     # Verify if table now exists
#     result = db.fetchone("SHOW TABLES LIKE 'migrations'")
#     assert result is not None, "❌ 'migrations' table was not created."
#     print("✅ 'migrations' table created successfully.")
