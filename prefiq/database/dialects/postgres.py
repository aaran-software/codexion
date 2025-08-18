# prefiq/database/dialects/postgres.py

from __future__ import annotations
from typing import Any, Tuple
from prefiq.database.dialects.base import Dialect

class PostgresDialect(Dialect):
    def name(self) -> str: return "postgres"

    def normalize_params(self, sql: str, params: Tuple[Any, ...] | None):
        # Convert %s → $1,$2,... (basic passthrough; assumes no literal %s in SQL text)
        if not params:
            return sql, params
        out = []
        idx = 1
        i = 0
        while i < len(sql):
            if sql[i:i+2] == "%s":
                out.append(f"${idx}")
                idx += 1
                i += 2
            else:
                out.append(sql[i])
                i += 1
        return "".join(out), params

    def quote_ident(self, name: str) -> str:
        return f'"{name}"'

    def list_tables_sql(self) -> str:
        # exclude system schemas
        return (
            "SELECT tablename FROM pg_catalog.pg_tables "
            "WHERE schemaname NOT IN ('pg_catalog','information_schema')"
        )
