# prefiq/database/schemas/builder.py

from __future__ import annotations
from typing import Callable, Any, Iterable
from prefiq.database.schemas.router import impl

def _bld():
    # Resolve the active driver every call (so engine_swap works in tests)
    return impl()[1]

def create(table_name: str, schema_callback: Callable[[Any], Any]) -> None:
    _bld().create(table_name, schema_callback)

def dropIfExists(table_name: str) -> None:
    _bld().dropIfExists(table_name)

def createIndex(table_name: str, index_name: str, columns: Iterable[str]) -> None:
    _bld().createIndex(table_name, index_name, columns)

def dropIndexIfExists(table_name: str, index_name: str) -> None:
    _bld().dropIndexIfExists(table_name, index_name)

# aliases
def drop_if_exists(table_name: str) -> None:
    dropIfExists(table_name)

def create_index(table_name: str, index_name: str, columns: Iterable[str]) -> None:
    createIndex(table_name, index_name, columns)

def drop_index_if_exists(table_name: str, index_name: str) -> None:
    dropIndexIfExists(table_name, index_name)

# -----------------------------
# NEW: ensure_migrations_table
# -----------------------------
def ensure_migrations_table() -> None:
    """
    Create the 'migrations' table if it doesn't exist.
    Columns: id, app, name, order_index, hash, created_at, updated_at
    Adds UNIQUE(app, name) and an index on app when supported by the blueprint.
    """
    def _schema(t: Any):
        parts = [
            t.id(),                      # auto-increment / serial / integer pk (blueprint-resolved)
            t.string("app", nullable=False),
            t.string("name", nullable=False),
            t.integer("order_index", nullable=False),
            t.string("hash", nullable=False),
            # IMPORTANT: timestamps() should be dialect-aware (no ON UPDATE on SQLite/Postgres)
            t.timestamps(),
        ]

        # Unique constraint on (app, name) to prevent duplicates
        if hasattr(t, "unique"):
            parts.append(t.unique(["app", "name"]))

        # Index on app to speed lookups; some builders accept str or list[str]
        if hasattr(t, "index"):
            try:
                parts.append(t.index("idx_migrations_app", ["app"]))
            except TypeError:
                parts.append(t.index("idx_migrations_app", "app"))

        return parts

    create("migrations", _schema)


# Optional camelCase alias (if used elsewhere)
def ensureMigrationsTable() -> None:
    ensure_migrations_table()
