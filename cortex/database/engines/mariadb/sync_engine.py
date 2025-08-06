# =============================================================
# SyncMariaDBEngine (sync_engine.py)
#
# Author: ChatGPT (refactored for dynamic configuration)
# Created: 2025-08-06
#
# Purpose:
#   - Synchronous MariaDB engine implementation.
#   - Pulls connection settings dynamically via config loader.
#   - Supports hooks, retries, slow query logging.
#
# Notes for Developers:
#   - Uses thread-local config (see: use_thread_config).
#   - Suitable for synchronous FastAPI or CLI tools.
#   - Apply `override_thread_config()` for per-request changes.
# =============================================================

import time
import mariadb
from typing import Optional, Sequence, Any

from cortex.database.engines.abstract_engine import AbstractEngine  # Base class defining interface and hooks
from cortex.database.engines.mariadb.retry import with_retry  # Retry wrapper for resilience
from cortex.database.engines.mariadb.logger import log_query  # Logs execution time and flags slow queries
from cortex.database.config_loader.base import use_thread_config  # Dynamic config access

class SyncMariaDBEngine(AbstractEngine):
    """
    Synchronous MariaDB engine using reusable config loader.
    Automatically fetches config from the active thread-local DatabaseConfig.
    """

    def __init__(self):
        super().__init__()
        self.config = use_thread_config().get_config_dict()  # Load config from thread-local context
        self.conn: Optional[mariadb.Connection] = None  # Connection instance

    def connect(self) -> None:
        # Establish a new MariaDB connection using the loaded config
        self.conn = mariadb.connect(**self.config)

    def close(self) -> None:
        # Safely close the connection
        if self.conn:
            self.conn.close()
            self.conn = None

    def begin(self) -> None:
        # Disable autocommit for manual transaction management
        if self.conn:
            self.conn.autocommit = False

    def commit(self) -> None:
        # Commit the current transaction
        if self.conn:
            self.conn.commit()

    def rollback(self) -> None:
        # Roll back the current transaction
        if self.conn:
            self.conn.rollback()

    def execute(self, query: str, params: Optional[tuple] = None) -> None:
        # Run a single query without returning rows
        self._run_hooks('before', query, params)  # Trigger before hook
        start_time = time.time()  # Track time for logging

        def action():
            with self.conn.cursor() as cur:
                cur.execute(query, params or ())
            self.conn.commit()

        with_retry(action)  # Execute with retries
        log_query(query, start_time)  # Log query duration
        self._run_hooks('after', query, params)  # Trigger after hook

    def executemany(self, query: str, param_list: Sequence[tuple]) -> None:
        # Run bulk insert/update with many param sets
        self._run_hooks('before', query)

        def action():
            with self.conn.cursor() as cur:
                cur.executemany(query, param_list)
            self.conn.commit()

        with_retry(action)
        self._run_hooks('after', query)

    def fetchone(self, query: str, params: Optional[tuple] = None) -> Any:
        # Fetch a single row from the result set
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
        # Fetch all rows from the result set
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
        # Simple health check for connectivity
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT 1")
                return cur.fetchone() is not None
        except:
            return False
