# prefiq/database/dialects/registry.py

from __future__ import annotations
from typing import Dict
from prefiq.settings.get_settings import load_settings
from prefiq.database.dialects.base import Dialect
from prefiq.database.dialects.mariadb import MariaDBDialect
from prefiq.database.dialects.mysql import MySQLDialect
from prefiq.database.dialects.sqlite import SQLiteDialect
from prefiq.database.dialects.postgres import PostgresDialect

_DIALECTS: Dict[str, Dialect] = {
    "mysql": MySQLDialect(),
    "mariadb": MariaDBDialect(),
    "sqlite": SQLiteDialect(),
    "postgres": PostgresDialect(),
    "postgresql": PostgresDialect(),
}

def get_dialect() -> Dialect:
    s = load_settings()
    eng = (s.DB_ENGINE or "").lower()
    if eng not in _DIALECTS:
        # default to mysql-style (mariadb) if not set
        eng = "mariadb"
    return _DIALECTS[eng]
