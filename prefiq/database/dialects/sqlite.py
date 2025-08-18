# prefiq/database/dialects/sqlite.py

from __future__ import annotations
import re
from typing import Any, Tuple
from prefiq.database.dialects.base import Dialect

# simple, safe conversion: replace each %s with ?
_PERC_S = re.compile(r"%s")

class SQLiteDialect(Dialect):
    def name(self) -> str: return "sqlite"

    def normalize_params(self, sql: str, params: Tuple[Any, ...] | None):
        # Convert %s placeholders to ? for sqlite3
        # NOTE: does not inspect literals; keep SQL from builder paramized properly.
        converted = _PERC_S.sub("?", sql)
        return converted, params

    def quote_ident(self, name: str) -> str:
        return f'"{name}"'  # standard SQL quoting

    def list_tables_sql(self) -> str:
        return "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
