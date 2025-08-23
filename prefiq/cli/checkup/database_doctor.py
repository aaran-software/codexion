# prefiq/cli/checkup/database_doctor.py
from __future__ import annotations

import asyncio
import inspect
import os
import time
from typing import Any, Optional

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

def _select1_ok(row: Any) -> bool:
    if row is None:
        return False
    try:
        first = row[0] if isinstance(row, (list, tuple)) else row
        return first == 1 or first is True or str(first) == "1"
    except Exception:
        return False

def _probe_health(engine: Any, timeout: float | None = 3.0) -> bool:
    """
    Portable health probe:
      - engine.fetchone('SELECT 1')
      - if awaitable, run with optional timeout
    """
    try:
        res = engine.fetchone("SELECT 1")
        if inspect.isawaitable(res):
            if timeout and timeout > 0:
                row = asyncio.run(asyncio.wait_for(res, timeout=timeout))
            else:
                row = asyncio.run(res)
            return _select1_ok(row)
        return _select1_ok(res)
    except Exception:
        return False

def _pool_stats(engine: Any) -> dict[str, Any]:
    """
    Best-effort pool stats across engines. Returns a small dict suitable for printing.
    """
    stats: dict[str, Any] = {}
    try:
        if hasattr(engine, "pool_stats") and callable(engine.pool_stats):
            stats = dict(engine.pool_stats())  # type: ignore[call-arg]
        elif hasattr(engine, "get_pool_info") and callable(engine.get_pool_info):
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
        row = engine.fetchone("SELECT 1")
        if inspect.isawaitable(row):
            row = asyncio.run(row)
        print(f"   SELECT 1 => {_select1_ok(row)}")
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
