# apps/devmeta/database/migrations/m0002_indexes.py

from prefiq.database.schemas.builder import create_index, drop_index_if_exists

TABLE = "todos"

def up():
    create_index(TABLE, "ix_todos_status", ["status"])
    create_index(TABLE, "ix_todos_due_at", ["due_at"])

def down():
    drop_index_if_exists(TABLE, "ix_todos_status")
    drop_index_if_exists(TABLE, "ix_todos_due_at")
