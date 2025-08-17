# prefiq/database/connection.py
from typing import Optional
from prefiq.settings.get_settings import get_settings
from prefiq.database.engines.mariadb.sync_engine import SyncMariaDBEngine
from prefiq.database.engines.mariadb.async_engine import AsyncMariaDBEngine

_engine_singleton = None  # type: Optional[object]

def _is_async(mode: str) -> bool:
    return (mode or "").lower() == "async"

def _make_engine():
    settings = get_settings()  # cached settings loader
    # strict: we only support MariaDB right now
    if settings.DB_ENGINE.lower() != "mariadb":
        raise RuntimeError(f"Unsupported DB_ENGINE '{settings.DB_ENGINE}'. Only 'mariadb' is implemented now.")
    return AsyncMariaDBEngine() if _is_async(settings.DB_MODE) else SyncMariaDBEngine()

def get_engine():
    global _engine_singleton
    if _engine_singleton is None:
        _engine_singleton = _make_engine()
    return _engine_singleton
