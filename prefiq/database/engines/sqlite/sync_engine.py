# =============================================================
# SyncSQLiteEngine
# file path: prefiq/database/engines/sqlite/sync_engine.py
#
# Author: Sundar
# Created: 2025-08-18
#
# Purpose:
#   - Synchronous SQLite engine implementing AbstractEngine[Any]
#   - Hook-aware (before/after)
#   - Pragmas tuned for local/dev usage
# =============================================================

from __future__ import annotations

import os
import time
import sqlite3
from contextlib import contextmanager
from typing import Any, Optional, Sequence, List

from prefiq.database.engines.abstract_engine import AbstractEngine
from prefiq.database.config_loader.base import use_thread_config
from prefiq.core.logger import get_logger

LOG = get_logger("prefiq.database.sqlite.sync")

_DEFAULT_PATH = os.path.join(".prefiq", "devmeta.sqlite")


def _resolve_sqlite_path() -> str:
    """
    Resolve the sqlite file path from thread-local DatabaseConfig.
    Accepts flexible keys: path | database | filename
    Fallback: ./.prefiq/devmeta.sqlite
    """
    cfg = {}
    try:
        cfg = use_thread_config().get_config_dict() or {}
    except Exception:
        pass

    for key in ("path", "database", "filename"):
        val = cfg.get(key)
        if isinstance(val, str) and val.strip():
            return val
    return _DEFAULT_PATH


def _apply_pragmas(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        PRAGMA journal_mode=WAL;
        PRAGMA foreign_keys=ON;
        PRAGMA synchronous=NORMAL;
        PRAGMA temp_store=MEMORY;
        """
    )


class SQLiteEngine(AbstractEngine[Any]):
    """
    Synchronous SQLite engine implementing AbstractEngine.
    """

    def __init__(self, db_path: Optional[str] = None) -> None:
        super().__init__()
        self._db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None

    # -------- lifecycle --------

    def connect(self) -> None:
        path = self._db_path or _resolve_sqlite_path()
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        self.conn = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
        self.conn.row_factory = sqlite3.Row
        _apply_pragmas(self.conn)

    def close(self) -> None:
        conn = self.conn
        if conn is not None:
            try:
                conn.close()
            finally:
                self.conn = None

    # -------- connection guard --------

    def _get_conn(self) -> sqlite3.Connection:
        if self.conn is None:
            self.connect()
        assert self.conn is not None, "Failed to establish SQLite connection"
        return self.conn

    # -------- transactions --------

    def begin(self) -> None:
        self._get_conn().execute("BEGIN")

    def commit(self) -> None:
        self._get_conn().commit()

    def rollback(self) -> None:
        self._get_conn().rollback()

    @contextmanager
    def transaction(self):
        """
        Context-managed explicit transaction.

        Usage:
            with engine.transaction():
                engine.execute("INSERT ...", (...,))
                engine.execute("UPDATE ...", (...,))
        """
        conn = self._get_conn()
        try:
            conn.execute("BEGIN")
            yield
            conn.commit()
        except Exception:
            conn.rollback()
            raise

    # -------- queries --------

    def execute(self, query: str, params: Optional[tuple] = None) -> None:
        conn = self._get_conn()
        self._run_hooks("before", query, params)
        t0 = time.time()
        with conn:
            conn.execute(query, params or ())
        self._run_hooks("after", query, params)
        LOG.debug("sqlite_execute", extra={"elapsed_ms": int((time.time() - t0) * 1000)})

    def executemany(self, query: str, param_list: Sequence[tuple]) -> None:
        conn = self._get_conn()
        self._run_hooks("before", query, None)
        t0 = time.time()
        with conn:
            conn.executemany(query, list(param_list))
        self._run_hooks("after", query, None)
        LOG.debug("sqlite_executemany", extra={"elapsed_ms": int((time.time() - t0) * 1000)})

    def fetchone(self, query: str, params: Optional[tuple] = None) -> Optional[Any]:
        conn = self._get_conn()
        self._run_hooks("before", query, params)
        t0 = time.time()
        cur = conn.execute(query, params or ())
        row = cur.fetchone()
        self._run_hooks("after", query, params)
        LOG.debug("sqlite_fetchone", extra={"elapsed_ms": int((time.time() - t0) * 1000)})
        return row

    def fetchall(self, query: str, params: Optional[tuple] = None) -> List[Any]:
        conn = self._get_conn()
        self._run_hooks("before", query, params)
        t0 = time.time()
        cur = conn.execute(query, params or ())
        rows = cur.fetchall()
        self._run_hooks("after", query, params)
        LOG.debug("sqlite_fetchall", extra={"elapsed_ms": int((time.time() - t0) * 1000)})
        return list(rows)

    # -------- health --------

    def test_connection(self) -> bool:
        try:
            cur = self._get_conn().execute("SELECT 1")
            return cur.fetchone() is not None
        except Exception:
            return False
