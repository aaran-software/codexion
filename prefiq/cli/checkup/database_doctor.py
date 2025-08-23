# prefiq/cli/checkup/database_doctor.py
from __future__ import annotations
import asyncio
import inspect
import os
import time
from typing import Any, Optional

from prefiq.settings.get_settings import load_settings
from prefiq.database.connection import get_engine, reset_engine
from prefiq.database.connection_manager import connection_manager
from prefiq.database.engines.abstract_engine import AbstractEngine


# --------------------------- helpers ---------------------------

def _engine_name(e: Any) -> str:
    cls = type(e).__name__
    if "Maria" in cls:
        return f"MariaDB/{cls}"
    if "SQLite" in cls or "Sqlite" in cls:
        return f"SQLite/{cls}"
    return cls

def _print_header():
    s = load_settings()
    print("=== Prefiq Database Doctor ===")
    print(f"DB_ENGINE={getattr(s, 'DB_ENGINE', None)!r}  DB_MODE={getattr(s, 'DB_MODE', None)!r}")

def _mask_dsn(dsn: Optional[str]) -> str:
    if not dsn:
        return "<none>"
    s = load_settings()
    pw = getattr(s, "DB_PASS", None)
    if pw and pw in dsn:
        return dsn.replace(pw, "*****")
    return dsn

def _probe_health(engine: Any, timeout: float | None = 3.0) -> bool:
    """
    Works for both sync and async engines without leaking coroutines.
    """
    try:
        res = engine.test_connection()
        if inspect.isawaitable(res):
            if timeout is not None and timeout > 0:
                return bool(asyncio.run(asyncio.wait_for(res, timeout=timeout)))
            return bool(asyncio.run(res))
        return bool(res)
    except Exception:
        return False

def _pool_stats(engine: Any) -> dict[str, Any]:
    """
    Best-effort pool stats across engines. Returns a small dict suitable for printing.
    """
    stats: dict[str, Any] = {}
    # Common patterns:
    # - engine.pool.size / in_use / free
    # - engine.pool_stats() -> dict
    # - engine.get_pool_info() -> dict
    try:
        if hasattr(engine, "pool_stats") and callable(engine.pool_stats):
            stats = dict(engine.pool_stats())  # type: ignore[call-arg]
        elif hasattr(engine, "get_pool_info") and callable(engine.get_pool_info):
            stats = dict(engine.get_pool_info())  # type: ignore[call-arg]
        elif hasattr(engine, "pool"):
            pool = engine.pool
            for key in ("size", "min_size", "max_size", "in_use", "free"):
                if hasattr(pool, key):
                    stats[key] = getattr(pool, key)
    except Exception:
        pass
    return stats

def _sync_smoketest(engine: AbstractEngine[Any]) -> None:
    print("-> Running sync smoke test (BEGIN/COMMIT, SELECT 1)")
    if hasattr(engine, "transaction"):
        with engine.transaction():  # type: ignore[call-arg]
            pass
    one = engine.fetchone("SELECT 1")
    ok = bool(one is not None)
    print(f"   SELECT 1 => {ok}")

async def _async_smoketest(engine: Any) -> None:
    print("-> Running async smoke test (BEGIN/COMMIT, SELECT 1)")
    if hasattr(engine, "transaction"):
        async with engine.transaction():  # type: ignore[misc]
            pass
    row = await engine.fetchone("SELECT 1")
    ok = bool(row is not None)
    print(f"   SELECT 1 => {ok}")


# --------------------------- entrypoint ---------------------------

def main(verbose: bool = False, strict: bool = False) -> int:
    _print_header()
    engine = get_engine()
    print(f"Engine: {_engine_name(engine)}")

    # verbose: show DSN (masked), warmup, and pool stats
    if verbose:
        s = load_settings()
        print(f"[verbose] DSN: {_mask_dsn(s.dsn())}")
        print(f"[verbose] DB_POOL_WARMUP: {getattr(s, 'DB_POOL_WARMUP', 0)}")
        st = _pool_stats(engine)
        if st:
            print(f"[verbose] pool: {st}")

    # health (with optional timing when verbose)
    t0 = time.perf_counter()
    healthy = _probe_health(engine, timeout=3.0)
    dt_ms = (time.perf_counter() - t0) * 1000.0
    print(f"Health: {'OK' if healthy else 'FAIL'}" + (f"  ({dt_ms:.1f} ms)" if verbose else ""))

    # strict mode: fail fast if unhealthy
    if strict and not healthy:
        print("Strict mode: health check failed.")
        return 1

    # smoke test
    try:
        if asyncio.iscoroutinefunction(getattr(engine, "begin", None)):  # async engine
            asyncio.run(_async_smoketest(engine))
        else:
            _sync_smoketest(engine)
    except Exception as e:
        print(f"Smoke test error: {type(e).__name__}: {e}")
        return 2

    # optional swap demo (kept; disabled by default)
    if os.getenv("DB_DOCTOR_SWAP_DEMO", "0") == "1":
        from prefiq.database.connection import swap_engine
        current = (load_settings().DB_ENGINE or "").lower()
        target = "sqlite" if current == "mariadb" else "mariadb"
        print(f"Swapping engine to: {target}")
        try:
            swap_engine(target)
            eng2 = get_engine()
            print(f"Now using: {_engine_name(eng2)}")
        finally:
            reset_engine()

    print("Database doctor finished.")
    return 0
