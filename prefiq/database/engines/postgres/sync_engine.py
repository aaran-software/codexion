# prefiq/database/engines/postgres/sync_engine.py
from typing import Any, Optional
try:
    import psycopg  # psycopg 3
except Exception:
    psycopg = None

class SyncPostgresEngine:
    def __init__(self, settings) -> None:
        if psycopg is None:
            raise RuntimeError("psycopg (v3) not installed. pip install psycopg[binary]")
        host = getattr(settings, "DB_HOST", "127.0.0.1")
        port = int(getattr(settings, "DB_PORT", 5432))
        user = getattr(settings, "DB_USER", "postgres")
        password = getattr(settings, "DB_PASS", "")
        db = getattr(settings, "DB_NAME", "postgres")
        self._conn = psycopg.connect(
            host=host, port=port, user=user, password=password, dbname=db, autocommit=True
        )

    def execute(self, sql: str, params: Optional[Any] = None) -> None:
        with self._conn.cursor() as cur:
            cur.execute(sql, params)

    def close(self) -> None:
        try:
            self._conn.close()
        except Exception:
            pass

    @property
    def name(self) -> str:
        return "postgres"
