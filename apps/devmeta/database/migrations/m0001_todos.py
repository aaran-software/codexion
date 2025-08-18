# apps/devmeta/database/migrations/m0001_todos.py
from __future__ import annotations

# Builder is optional: only used if no conn is passed
try:
    from prefiq.database.schemas.builder import create, dropIfExists  # type: ignore
except Exception:  # pragma: no cover
    create = dropIfExists = None  # type: ignore

TABLE = "todos"

def up(conn=None):
    """
    Create the todos table.
    Prefer executing on the provided SQLite connection (used by tests),
    fall back to the builder if no connection is passed.
    """
    if conn is not None:
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

            CREATE INDEX IF NOT EXISTS ix_{TABLE}_status  ON {TABLE}(status);
            CREATE INDEX IF NOT EXISTS ix_{TABLE}_project ON {TABLE}(project);
            CREATE INDEX IF NOT EXISTS ix_{TABLE}_due_at  ON {TABLE}(due_at);
            """
        )
        return

    # Fallback: builder path (no explicit conn)
    if create is None:
        raise RuntimeError("Builder not available and no DB connection provided to up()")

    create(TABLE, lambda t: [
        t.id(),
        t.string("title", nullable=False),
        t.string("status", default="open", nullable=False),
        t.integer("priority", default=3, nullable=False),
        t.string("project", nullable=True),
        t.datetime("due_at", nullable=True),
        t.datetime("created_at", default="CURRENT_TIMESTAMP", nullable=False),
        t.datetime("updated_at", default="CURRENT_TIMESTAMP", nullable=False),
        t.datetime("completed_at", nullable=True),
    ])


def down(conn=None):
    """
    Drop the todos table (handy for tests).
    """
    if conn is not None:
        conn.executescript(f"DROP TABLE IF EXISTS {TABLE};")
        return

    if dropIfExists is None:
        raise RuntimeError("Builder not available and no DB connection provided to down()")

    dropIfExists(TABLE)
