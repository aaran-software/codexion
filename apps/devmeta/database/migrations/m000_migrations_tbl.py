# apps/devmeta/database/migrations/m000_migrations_tbl.py

from __future__ import annotations

# Builder is optional: we only use it if no conn is passed
try:
    from prefiq.database.schemas.builder import create, dropIfExists  # type: ignore
except Exception:  # pragma: no cover
    create = dropIfExists = None  # type: ignore

MIGRATIONS_TABLE = "devmeta_migrations"

def up(conn=None):
    """
    Create the migrations bookkeeping table.
    Prefer executing on the provided SQLite connection (used by tests),
    fall back to the builder if no connection is passed.
    """
    if conn is not None:
        conn.executescript(
            f"""
            CREATE TABLE IF NOT EXISTS {MIGRATIONS_TABLE}(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL UNIQUE,
              order_index INTEGER NOT NULL,
              hash TEXT NOT NULL,
              applied_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );

            CREATE UNIQUE INDEX IF NOT EXISTS ux_{MIGRATIONS_TABLE}_name
              ON {MIGRATIONS_TABLE}(name);
            CREATE INDEX IF NOT EXISTS ix_{MIGRATIONS_TABLE}_order
              ON {MIGRATIONS_TABLE}(order_index);
            """
        )
        return

    # Fallback: builder path (no explicit conn)
    if create is None:
        raise RuntimeError("Builder not available and no DB connection provided to up()")

    create(MIGRATIONS_TABLE, lambda t: [
        t.id(),                                  # INTEGER PRIMARY KEY AUTOINCREMENT
        t.string("name", unique=True, nullable=False),
        t.integer("order_index", nullable=False),
        t.string("hash", nullable=False),
        t.datetime("applied_at", default="CURRENT_TIMESTAMP"),
    ])


def down(conn=None):
    """
    Drop the bookkeeping table (usually not needed in prod, handy for tests).
    """
    if conn is not None:
        conn.execute(f"DROP TABLE IF EXISTS {MIGRATIONS_TABLE}")
        return

    if dropIfExists is None:
        raise RuntimeError("Builder not available and no DB connection provided to down()")

    dropIfExists(MIGRATIONS_TABLE)
