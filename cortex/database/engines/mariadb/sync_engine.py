# sync_engine.py

import time
import mariadb
from typing import Optional, Sequence, Any

from .abstract import AbstractEngine
from .retry import with_retry
from .logger import log_query
from core.database.config_loader.base import use_thread_config

class SyncMariaDBEngine(AbstractEngine):
    """
    Synchronous MariaDB engine using reusable config loader.
    Automatically fetches config from the active thread-local DatabaseConfig.
    """
    def __init__(self):
        super().__init__()
        self.config = use_thread_config().get_config_dict()
        self.conn: Optional[mariadb.Connection] = None

    def connect(self) -> None:
        self.conn = mariadb.connect(**self.config)

    def close(self) -> None:
        if self.conn:
            self.conn.close()
            self.conn = None

    def begin(self) -> None:
        if self.conn:
            self.conn.autocommit = False

    def commit(self) -> None:
        if self.conn:
            self.conn.commit()

    def rollback(self) -> None:
        if self.conn:
            self.conn.rollback()

    def execute(self, query: str, params: Optional[tuple] = None) -> None:
        self._run_hooks('before', query, params)
        start_time = time.time()

        def action():
            with self.conn.cursor() as cur:
                cur.execute(query, params or ())
            self.conn.commit()

        with_retry(action)
        log_query(query, start_time)
        self._run_hooks('after', query, params)

    def executemany(self, query: str, param_list: Sequence[tuple]) -> None:
        self._run_hooks('before', query)

        def action():
            with self.conn.cursor() as cur:
                cur.executemany(query, param_list)
            self.conn.commit()

        with_retry(action)
        self._run_hooks('after', query)

    def fetchone(self, query: str, params: Optional[tuple] = None) -> Any:
        self._run_hooks('before', query, params)
        start_time = time.time()

        def action():
            with self.conn.cursor() as cur:
                cur.execute(query, params or ())
                return cur.fetchone()

        result = with_retry(action)
        log_query(query, start_time)
        self._run_hooks('after', query, params)
        return result

    def fetchall(self, query: str, params: Optional[tuple] = None) -> list[Any]:
        self._run_hooks('before', query, params)
        start_time = time.time()

        def action():
            with self.conn.cursor() as cur:
                cur.execute(query, params or ())
                return cur.fetchall()

        result = with_retry(action)
        log_query(query, start_time)
        self._run_hooks('after', query, params)
        return result

    def test_connection(self) -> bool:
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT 1")
                return cur.fetchone() is not None
        except:
            return False
