# prefiq/database/dialects/base.py

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Iterable, Tuple

class Dialect(ABC):
    """
    DB-agnostic helpers:
      - normalize_params(sql, params): translate from internal '%s' placeholders
      - list_tables_sql(): SQL to enumerate user tables
      - create_table_suffix(): optional suffix for CREATE TABLE
    """

    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def normalize_params(self, sql: str, params: Tuple[Any, ...] | None) -> tuple[str, Tuple[Any, ...] | None]:
        """Translate internal '%s' placeholders to engine-native and return (sql, params)."""
        ...

    @abstractmethod
    def list_tables_sql(self) -> str:
        """SQL to list user tables (single text column with table name)."""
        ...

    def create_table_suffix(self) -> str:
        """Optional suffix appended to CREATE TABLE; default empty."""
        return ""

    def quote_ident(self, name: str) -> str:
        """
        Quote an identifier (table/column) for this dialect.
        Default: backticks (MySQL-style). Override where needed.
        """
        return f"`{name}`"
