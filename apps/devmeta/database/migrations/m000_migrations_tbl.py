# apps/devmeta/database/migration/m000_migrations_tbl.py

from __future__ import annotations

import sqlite3
from typing import Iterable, Set, Tuple


DEFAULT_TABLE_NAME = "dev_migrations"


DDL_CREATE_TABLE = f"""
CREATE TABLE IF NOT EXISTS {DEFAULT_TABLE_NAME}(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  order_index INTEGER NOT NULL,
  hash TEXT NOT NULL,
  applied_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

# Optional safety: unique index on (name) already implied by UNIQUE, but explicit index helps planners.
DDL_CREATE_INDEXES = (
    f"CREATE UNIQUE INDEX IF NOT EXISTS ux_{DEFAULT_TABLE_NAME}_name ON {DEFAULT_TABLE_NAME}(name);",
    f"CREATE INDEX IF NOT EXISTS ix_{DEFAULT_TABLE_NAME}_order ON {DEFAULT_TABLE_NAME}(order_index);",
)


def ensure_devmeta_migrations_table(
    conn: sqlite3.Connection,
    table_name: str = DEFAULT_TABLE_NAME,
) -> None:
    """
    Ensure the migrations bookkeeping table exists in the connected SQLite DB.
    Idempotent: safe to call multiple times.
    """
    # Rebind DDL to the requested table name (if custom)
    ddl_table = DDL_CREATE_TABLE.replace(DEFAULT_TABLE_NAME, table_name)
    ddl_indexes = [stmt.replace(DEFAULT_TABLE_NAME, table_name) for stmt in DDL_CREATE_INDEXES]

    conn.executescript(ddl_table)
    for stmt in ddl_indexes:
        conn.execute(stmt)


def get_applied_migration_names(
    conn: sqlite3.Connection,
    table_name: str = DEFAULT_TABLE_NAME,
) -> Set[str]:
    """
    Return the set of already-applied migration filenames.
    """
    rows = conn.execute(f"SELECT name FROM {table_name} ORDER BY order_index").fetchall()
    return {r["name"] for r in rows}


def record_migration_applied(
    conn: sqlite3.Connection,
    name: str,
    order_index: int,
    file_hash: str,
    table_name: str = DEFAULT_TABLE_NAME,
) -> None:
    """
    Insert a row marking a migration file as applied.
    """
    conn.execute(
        f"INSERT INTO {table_name}(name, order_index, hash) VALUES (?,?,?)",
        (name, order_index, file_hash),
    )
