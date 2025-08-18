# prefiq/database/dialects/mariadb.py

from __future__ import annotations
from typing import Any, Tuple
from prefiq.database.dialects.base import Dialect

class MariaDBDialect(Dialect):
    def name(self) -> str: return "mariadb"

    def normalize_params(self, sql: str, params: Tuple[Any, ...] | None):
        # MariaDB already use %s
        return sql, params

    def list_tables_sql(self) -> str:
        return "SHOW TABLES"

    def create_table_suffix(self) -> str:
        return " ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
