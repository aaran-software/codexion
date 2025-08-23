# prefiq/cli/checkup/database_doctor.py
from __future__ import annotations

import asyncio
import inspect
import os
import time
from typing import Any, Optional
from collections.abc import Sequence, Mapping

from prefiq.settings.get_settings import load_settings
from prefiq.database.connection import get_engine, reset_engine


# --------------------------- helpers ---------------------------

def _engine_name(e: Any) -> str:
    # Prefer explicit attributes if engines expose them
    for attr in ("name", "dialect_name", "driver"):
        v = getattr(e, attr, None)
        if isinstance(v, str) and v.strip():
            return v
    cls = type(e).__name__
    if "Maria" in cls:
        return f"MariaDB/{cls}"
    if "SQLite" in cls or "Sqlite" in cls:
        return f"SQLite/{cls}"
    if "Postgres" in cls or "Pg" in cls:
        return f"Postgres/{cls}"
    return cls


def _print_header() -> None:
    s = load_settings()
    print("=== Prefiq Database Doctor ===")
    print(f"DB_ENGINE='{getattr(s, 'DB_ENGINE', None)}'  DB_MODE='{getattr(s, 'DB_MODE', None)}'")


def _mask_dsn(dsn: Optional[str]) -> str:
    if not dsn:
        return "<none>"
    s = load_settings()
    pw = getattr(s, "DB_PASS", None)
    try:
        if pw and pw in dsn:
            return dsn.replace(pw, "*****")
    except Exception:
        pass
    return dsn


def _display_dsn(engine: Any) -> str:
    # Prefer engine-provided url/dsn (our PG engine sets .url with a masked password)
    for attr in ("url", "database_url", "dsn"):
        v = getattr(engine, attr, None)
        if isinstance(v, str) and v.strip():
            return v
    # Fallback to settings-derived DSN (mask password)
    return _mask_dsn(load_settings().dsn())


def _select1_ok(val: Any) -> bool:
    """Return True iff the scalar value represents 1."""
    if val is None:
        return False
    try:
        if val is True:
            return True
        if isinstance(val, (int, float)):
            return int(val) == 1
        return str(val) == "1"
    except Exception:
        return False


def _first_value(row: Any) -> Any:
    """
    Best-effort extraction of the first column from:
    - tuple/list
    - sqlite3.Row (sequence-like; supports row[0])
    - mappings like {"1": 1} (take first value)
    Otherwise, assume it's already a scalar.
    """
    try:
        if isinstance(row, Sequence) and not isinstance(row, (str, bytes, bytearray)):
            return row[0]  # covers tuple/list/sqlite3.Row
        if isinstance(row, Mapping):
            # take first value if any
            for _, v in row.items():
                return v
        # duck-typing: has __getitem__ -> try [0]
        if hasattr(row, "__getitem__") and not isinstance(row, (str, bytes, bytearray)):
            try:
                return row[0]
            except Exception:
                pass
        return row
    except Exception:
        return row


def _await_if_needed(x: Any, timeout: float | None) -> Any:
    if inspect.isawaitable(x):
        if timeout and timeout > 0:
            return asyncio.run(asyncio.wait_for(x, timeout=timeout))
        return asyncio.run(x)
    return x


def _get_scalar(engine: Any, sql: str, timeout: float | None = 3.0) -> Any:
    """
    Portable scalar fetch:
      1) engine.fetch_value(sql)
      2) engine.scalar(sql)
      3) engine.fetchone(sql) -> first col
      4) raw DB-API via engine.raw_connection()/connection/conn
      5) last resort: engine.execute(sql) returning cursor-like
    Returns the first column value or raises on error.
    """
    # 1) fetch_value
    if hasattr(engine, "fetch_value") and callable(getattr(engine, "fetch_value")):
        res = _await_if_needed(engine.fetch_value(sql), timeout)
        return res
    # 2) scalar
    if hasattr(engine, "scalar") and callable(getattr(engine, "scalar")):
        res = _await_if_needed(engine.scalar(sql), timeout)
        return res
    # 3) fetchone
    if hasattr(engine, "fetchone") and callable(getattr(engine, "fetchone")):
        row = _await_if_needed(engine.fetchone(sql), timeout)
        return _first_value(row)
    # 4) raw DB-API fallback
    conn = None
    for attr in ("raw_connection", "connection", "conn"):
        if hasattr(engine, attr):
            obj = getattr(engine, attr)
            conn = obj() if callable(obj) else obj
            if conn:
                break
    if conn and hasattr(conn, "cursor"):
        cur = conn.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        try:
            cur.close()
        except Exception:
            pass
        return _first_value(row)
    # 5) generic execute -> cursor-like
    if hasattr(engine, "execute") and callable(getattr(engine, "execute")):
        cur = _await_if_needed(engine.execute(sql), timeout)
        if cur is not None and hasattr(cur, "fetchone"):
            row = cur.fetchone()
            return _first_value(row)
    raise RuntimeError("No compatible scalar fetch method found on engine")


def _probe_health(engine: Any, timeout: float | None = 3.0) -> bool:
    """Portable health probe: fetch scalar 1 from 'SELECT 1'."""
    try:
        val = _get_scalar(engine, "SELECT 1", timeout=timeout)
        return _select1_ok(val)
    except Exception:
        return False


def _pool_stats(engine: Any) -> dict[str, Any]:
    """
    Best-effort pool stats across engines. Returns a small dict suitable for printing.
    """
    stats: dict[str, Any] = {}
    try:
        if hasattr(engine, "pool_stats") and callable(engine.pool_stats):  # type: ignore[attr-defined]
            stats = dict(engine.pool_stats())  # type: ignore[call-arg]
        elif hasattr(engine, "get_pool_info") and callable(engine.get_pool_info):  # type: ignore[attr-defined]
            stats = dict(engine.get_pool_info())  # type: ignore[call-arg]
        elif hasattr(engine, "pool"):
            pool = getattr(engine, "pool")
            for key in ("size", "min_size", "max_size", "in_use", "free"):
                if hasattr(pool, key):
                    stats[key] = getattr(pool, key)
    except Exception:
        pass
    return stats


# --------------------------- entrypoint ---------------------------

def main(verbose: bool = False, strict: bool = False) -> int:
    _print_header()

    engine = get_engine()
    print(f"Engine: {_engine_name(engine)}")

    # verbose: show DSN (masked), warmup, and pool stats
    if verbose:
        s = load_settings()
        print(f"[verbose] DSN: {_display_dsn(engine)}")
        print(f"[verbose] DB_POOL_WARMUP: {getattr(s, 'DB_POOL_WARMUP', 0)}")
        st = _pool_stats(engine)
        if st:
            print(f"[verbose] pool: {st}")

    # health (time + status)
    t0 = time.perf_counter()
    healthy = _probe_health(engine, timeout=3.0)
    dt_ms = (time.perf_counter() - t0) * 1000.0
    print(f"Health: {'OK' if healthy else 'FAIL'}" + (f"  ({dt_ms:.1f} ms)" if verbose else ""))

    # strict mode: fail fast if unhealthy
    if strict and not healthy:
        print("Strict mode: health check failed.")
        return 1

    # smoke test (SELECT 1 only — no BEGIN/COMMIT to avoid driver hangs)
    try:
        print("-> Running smoke test (SELECT 1)")
        raw = _get_scalar(engine, "SELECT 1", timeout=3.0)
        val = _first_value(raw)
        ok = _select1_ok(val)
        print(f"   SELECT 1 => {val!r}  ({'OK' if ok else 'FAIL'})")
    except Exception as e:
        print(f"Smoke test error: {type(e).__name__}: {e}")
        # not fatal unless strict
        if strict:
            return 2

    # optional swap demo (kept; disabled by default)
    if os.getenv("DB_DOCTOR_SWAP_DEMO", "0") == "1":
        from prefiq.database.connection import swap_engine
        current = (load_settings().DB_ENGINE or "").lower()
        target = "sqlite" if current in ("mariadb", "postgres") else "mariadb"
        print(f"Swapping engine to: {target}")
        try:
            swap_engine(target)
            eng2 = get_engine()
            print(f"Now using: {_engine_name(eng2)}")
        finally:
            reset_engine()

    print("Database doctor finished.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
