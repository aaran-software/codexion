# tests/test_create_users_table.py
from cortex.database.connection import db
from cortex.database.schemas.builder import create, dropIfExists

def test_create_users_table():
    # Step 1: Drop the table if it exists
    dropIfExists("users")

    # Step 2: Create the users table
    create("users", lambda table: [
        table.id(),
        table.string("name", 100),
        table.string("email", 150),
        table.boolean("is_active"),
        table.timestamps()
    ])

    # Verify if table now exists
    result = db.fetchone("SHOW TABLES LIKE 'users'")
    assert result is not None, "❌ 'users' table was not created."
    print("✅ 'users' table created successfully.")
