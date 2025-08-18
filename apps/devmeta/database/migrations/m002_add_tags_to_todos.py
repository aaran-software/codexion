# apps/devmeta/database/migrations/m002_add_tags_to_todos.py
from __future__ import annotations

TABLE = "todos"
COLUMN = "tags"

def up(conn=None):
    if conn is None:
        raise RuntimeError("m002_add_tags_to_todos.up() requires a DB connection")

    # Ensure base table exists (in case tests run with a subset of migrations)
    # No-op if it's already there.
    conn.executescript(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE} (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          title TEXT NOT NULL,
          status TEXT NOT NULL DEFAULT 'open',
          priority INTEGER NOT NULL DEFAULT 3,
          project TEXT NULL,
          due_at DATETIME NULL,
          created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
          updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
          completed_at DATETIME NULL
        );
        """
    )

    # Add column only if missing (idempotent)
    cols = {row["name"] for row in conn.execute(f"PRAGMA table_info({TABLE})")}
    if COLUMN not in cols:
        conn.execute(f"ALTER TABLE {TABLE} ADD COLUMN {COLUMN} TEXT")

def down(conn=None):
    # SQLite cannot drop columns without table rebuild; leave as no-op.
    return
