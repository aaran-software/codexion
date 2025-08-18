# apps/devmeta/database/migrations/m002_add_tags_to_todos.py
from __future__ import annotations

TABLE = "todos"
COLUMN = "tags"

def up(conn=None):
    if conn is None:
        raise RuntimeError("m002_add_tags_to_todos.up() requires a DB connection")
    # Check existing columns; add only if missing (idempotent)
    cols = {row["name"] for row in conn.execute(f"PRAGMA table_info({TABLE})")}
    if COLUMN not in cols:
        conn.execute(f"ALTER TABLE {TABLE} ADD COLUMN {COLUMN} TEXT")

def down(conn=None):
    # No-op in SQLite (dropping a column requires table rebuild).
    return
