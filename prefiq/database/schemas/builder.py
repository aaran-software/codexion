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
# ensure_migrations_table (portable)
# -----------------------------
def ensure_migrations_table() -> None:
    """
    Create the 'migrations' table if it doesn't exist.
    Columns: id, app, name, order_index, hash, created_at, updated_at
    Adds UNIQUE(app, name) and an index on app, adapting to different blueprint signatures.
    """
    def _schema(t: Any):
        parts = [
            t.id(),                              # pk (dialect-specific)
            t.string("app", nullable=False),
            t.string("name", nullable=False),
            t.integer("order_index", nullable=False),
            t.string("hash", nullable=False),
            t.timestamps(),                      # created_at, updated_at (no ON UPDATE for PG/SQLite)
        ]

        # UNIQUE(app, name)
        if hasattr(t, "unique"):
            # Try (name, columns)
            try:
                parts.append(t.unique("uniq_migrations_app_name", ["app", "name"]))
            except TypeError:
                # Fallbacks for other signatures
                try:
                    parts.append(t.unique(["app", "name"]))
                except TypeError:
                    try:
                        parts.append(t.unique("uniq_migrations_app_name", "app", "name"))
                    except TypeError:
                        pass  # give up silently if blueprint differs

        # INDEX(app)
        if hasattr(t, "index"):
            # Some builders accept (name, ["col"]), some (name, "col"), some just ("col")
            try:
                parts.append(t.index("idx_migrations_app", ["app"]))
            except TypeError:
                try:
                    parts.append(t.index("idx_migrations_app", "app"))
                except TypeError:
                    try:
                        parts.append(t.index("app"))
                    except TypeError:
                        pass

        return parts

    create("migrations", _schema)


# Optional camelCase alias if used elsewhere
def ensureMigrationsTable() -> None:
    ensure_migrations_table()