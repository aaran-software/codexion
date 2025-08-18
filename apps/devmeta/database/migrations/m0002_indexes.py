# apps/devmeta/database/migrations/m0002_indexes.py

from prefiq.database.schemas.builder import createIndex, dropIndexIfExists

TABLE = "todos"

def up():
    createIndex(TABLE, "ix_todos_status", ["status"])
    createIndex(TABLE, "ix_todos_due_at", ["due_at"])

def down():
    dropIndexIfExists(TABLE, "ix_todos_status")
    dropIndexIfExists(TABLE, "ix_todos_due_at")
