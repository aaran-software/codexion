# prefiq/database/engines/mysql/sync_engine.py

from __future__ import annotations

import time
from contextlib import contextmanager
from typing import Optional, Sequence, Any, cast

import pymysql

from prefiq.database.engines.abstract_engine import AbstractEngine
from prefiq.database.engines.mysql.retry import with_retry
from prefiq.database.engines.mysql.logger import log_query
from prefiq.database.config_loader.base import use_thread_config


class SyncMariaDBEngine(AbstractEngine[Any]):
    """
    Synchronous mysql engine using reusable config loader.
    Automatically fetches config from the active thread-local DatabaseConfig.
    """

    def __init__(self) -> None:
        super().__init__()
        self.conn: Optional[pymysql.Connection] = None

    # -------- lifecycle --------

    def connect(self) -> None:
        """Establish a new mysql connection using the latest thread-local config."""
        config = use_thread_config().get_config_dict()
        self.conn = pymysql.connect(**config)
        # Prefer autocommit for single statements
        try:
            self.conn.autocommit = True  # type: ignore[attr-defined]
        except Exception:
            pass

    def close(self) -> None:
        """Safely close the connection."""
        conn = self.conn
        if conn is not None:
            try:
                conn.close()
            finally:
                self.conn = None

    # -------- connection guard / narrowing --------

    def _get_conn(self) -> pymysql.Connection:
        """
        Ensure we have a live connection and return it.
        This function *narrows* self.conn for the type checker.
        """
        if self.conn is None:
            self.connect()
        conn = self.conn
        # Type-narrowing assert so static checker knows conn is not None
        assert conn is not None, "Failed to establish mysql connection"
        return conn

    def _validate_connection(self) -> pymysql.Connection:
        """
        Ensure we have a live connection; reconnect on ping failure.
        Returns a non-None connection (type-narrowed).
        """
        conn = self._get_conn()
        try:
            conn.ping()
        except pymysql.Error:
            self.connect()
            conn = self._get_conn()
        return conn

    # -------- transactions --------

    def begin(self) -> None:
        """Disable autocommit for manual transaction management."""
        conn = self._validate_connection()
        try:
            conn.autocommit = False  # type: ignore[attr-defined]
        except Exception:
            with conn.cursor() as cur:
                cur.execute("START TRANSACTION")

    def commit(self) -> None:
        """Commit the current transaction and restore autocommit."""
        conn = self._validate_connection()
        conn.commit()
        try:
            conn.autocommit = True  # type: ignore[attr-defined]
        except Exception:
            pass

    def rollback(self) -> None:
        """Rollback the current transaction and restore autocommit."""
        conn = self._validate_connection()
        conn.rollback()
        try:
            conn.autocommit = True  # type: ignore[attr-defined]
        except Exception:
            pass

    @contextmanager
    def transaction(self):
        """
        Pin the connection for a multi-statement transaction.

        Usage:
            with db.transaction() as cur:
                cur.execute("INSERT ...", (...,))
                cur.execute("UPDATE ...", (...,))
        """
        conn = self._validate_connection()

        def _begin():
            try:
                conn.autocommit = False  # type: ignore[attr-defined]
            except Exception:
                with conn.cursor() as c:
                    c.execute("START TRANSACTION")

        def _commit():
            conn.commit()
            try:
                conn.autocommit = True  # type: ignore[attr-defined]
            except Exception:
                pass

        def _rollback():
            conn.rollback()
            try:
                conn.autocommit = True  # type: ignore[attr-defined]
            except Exception:
                pass

        with_retry(_begin)

        cur = conn.cursor()
        try:
            yield cur
            with_retry(_commit)
        except Exception:
            with_retry(_rollback)
            raise
        finally:
            try:
                cur.close()
            except Exception:
                pass

    # -------- queries --------

    def execute(self, query: str, params: Optional[tuple] = None) -> None:
        """Run a single write query (INSERT/UPDATE/DELETE)."""
        conn = self._validate_connection()
        self._run_hooks("before", query, params)
        start_time = time.time()

        def action():
            with conn.cursor() as cur:
                cur.execute(query, params or ())
            conn.commit()

        with_retry(action)
        log_query(query, start_time)
        self._run_hooks("after", query, params)

    def executemany(self, query: str, param_list: Sequence[tuple]) -> None:
        """Run bulk insert/update with many param sets."""
        conn = self._validate_connection()
        self._run_hooks("before", query, None)
        start_time = time.time()

        def action():
            with conn.cursor() as cur:
                cur.executemany(query, list(param_list))
            conn.commit()

        with_retry(action)
        log_query(query, start_time)
        self._run_hooks("after", query, None)

    def fetchone(self, query: str, params: Optional[tuple] = None) -> Any:
        """Fetch a single row from the result set."""
        conn = self._validate_connection()
        self._run_hooks("before", query, params)
        start_time = time.time()

        def action():
            with conn.cursor() as cur:
                cur.execute(query, params or ())
                return cur.fetchone()

        result = with_retry(action)
        log_query(query, start_time)
        self._run_hooks("after", query, params)
        return result

    def fetchall(self, query: str, params: Optional[tuple] = None) -> list[Any]:
        """Fetch all rows from the result set."""
        conn = self._validate_connection()
        self._run_hooks("before", query, params)
        start_time = time.time()

        def action():
            with conn.cursor() as cur:
                cur.execute(query, params or ())
                return list(cur.fetchall())

        result = with_retry(action)
        log_query(query, start_time)
        self._run_hooks("after", query, params)
        return result

    # -------- health --------

    def test_connection(self) -> bool:
        """Simple connectivity check."""
        try:
            conn = self._validate_connection()
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                return cur.fetchone() is not None
        except (pymysql.Error, OSError):
            return False
