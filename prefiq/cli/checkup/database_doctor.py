# prefiq/cli/checkup/database_doctor.py

from __future__ import annotations
import asyncio
import inspect
import os
from typing import Any

from prefiq.settings.get_settings import load_settings
from prefiq.database.connection import get_engine, reset_engine
from prefiq.database.connection_manager import connection_manager
# REMOVE this import if present:
# from prefiq.database.health import is_healthy
from prefiq.database.engines.abstract_engine import AbstractEngine


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

def main(verbose: bool = False, strict: bool = False) -> int:
    _print_header()
    engine = get_engine()
    print(f"Engine: {_engine_name(engine)}")

    # health check (no dangling coroutine warnings)
    healthy = _probe_health(engine, timeout=3.0)
    print(f"Health: {'OK' if healthy else 'FAIL'}")

    try:
        if asyncio.iscoroutinefunction(getattr(engine, "begin", None)):  # async engine
            asyncio.run(_async_smoketest(engine))
        else:
            _sync_smoketest(engine)
    except Exception as e:
        print(f"Smoke test error: {type(e).__name__}: {e}")
        return 2

    if strict and not healthy:
        return 1

    if verbose:
        s = load_settings()
        masked = (s.dsn() or "").replace(s.DB_PASS, "*****") if getattr(s, "DB_PASS", None) else (s.dsn() or "")
        print(f"[verbose] DSN: {masked}")
        try:
            import time
            t0 = time.perf_counter()
            ok = _probe_health(engine, timeout=3.0)
            dt = (time.perf_counter() - t0) * 1000
            print(f"[verbose] ping: {'OK' if ok else 'FAIL'} in {dt:.1f} ms")
        except Exception as e:
            print(f"[verbose] ping error: {e}")

    # Optional swap demo preserved if you had it before
    if os.getenv("DB_DOCTOR_SWAP_DEMO", "0") == "1":
        from prefiq.database.connection import swap_engine
        current = load_settings().DB_ENGINE or ""
        target = "sqlite" if current.lower() == "mariadb" else "mariadb"
        print(f"Swapping engine to: {target}")
        try:
            swap_engine(target)
            eng2 = get_engine()
            print(f"Now using: {_engine_name(eng2)}")
        finally:
            reset_engine()

    print("Database doctor finished.")
    return 0
