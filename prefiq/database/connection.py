# prefiq/database/connection.py

from typing import Optional
from prefiq.settings.get_settings import load_settings
from prefiq.database.engines.mariadb.sync_engine import SyncMariaDBEngine
from prefiq.database.engines.mariadb.async_engine import AsyncMariaDBEngine
from prefiq.database.engines.mysql.sync_engine import SyncMysqlEngine
from prefiq.database.engines.mysql.async_engine import AsyncMysqlEngine
from prefiq.database.engines.sqlite.sqlite_engine import SQLiteEngine

_engine_singleton: Optional[object] = None

def _is_async(mode: str) -> bool:
    return (mode or "").lower() == "async"

def _make_engine():
    s = load_settings()
    eng = (s.DB_ENGINE or "").lower()

    if eng == "mariadb":
        return AsyncMariaDBEngine() if _is_async(s.DB_MODE) else SyncMariaDBEngine()

    if eng == "mysql":
        return AsyncMysqlEngine() if _is_async(s.DB_MODE) else SyncMysqlEngine()

    if eng == "sqlite":
        return SQLiteEngine()

    raise RuntimeError(
        f"Unsupported DB_ENGINE '{s.DB_ENGINE}'. "
        "Use one of: mariadb, mysql, sqlite, postgres, postgresql, mongodb."
    )

def get_engine():
    global _engine_singleton
    if _engine_singleton is None:
        _engine_singleton = _make_engine()
    return _engine_singleton
