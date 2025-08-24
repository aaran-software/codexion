# prefiq/cli/doctor.py
from __future__ import annotations

import asyncio
import inspect
import os
import time
from dataclasses import dataclass
from typing import Any, List, Tuple, Optional
from collections.abc import Sequence, Mapping

import typer

# —— core wiring (no inline logging) ——
from prefiq.core.application import Application
from prefiq.core.service_providers import get_service_providers
from prefiq.settings.get_settings import load_settings
from prefiq.database.connection import get_engine, reset_engine

app = typer.Typer(help="Health checks and diagnostics")


# ──────────────────────────────────────────────────────────────────────────────
# Small data shape for pretty prints
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class CheckResult:
    name: str
    ok: bool
    detail: str = ""


def _fmt(ok: bool) -> str:
    return "✅" if ok else "❌"


# ──────────────────────────────────────────────────────────────────────────────
# Boot diagnostics
# ──────────────────────────────────────────────────────────────────────────────

def run_boot_diagnostics(verbose: bool = False) -> Tuple[bool, List[CheckResult]]:
    results: List[CheckResult] = []

    # 1) Settings load
    try:
        settings = load_settings()
        results.append(CheckResult("Settings loaded", True, f"ENV={getattr(settings, 'ENV', 'development')}"))
    except Exception as e:
        results.append(CheckResult("Settings loaded", False, str(e)))
        return False, results

    # 2) Providers discovery (hybrid)
    try:
        providers = list(get_service_providers())
        prov_names = [getattr(p, "__name__", str(p)) for p in providers]
        results.append(CheckResult("Providers discovered", True, ", ".join(prov_names)))
    except Exception as e:
        results.append(CheckResult("Providers discovered", False, str(e)))
        return False, results

    # 3) Application boot (register + boot)
    try:
        app = Application.get_app()
        for p in providers:
            app.register(p)
        app.boot()
        results.append(CheckResult("Application booted", True, "Lifecycle callbacks executed"))
    except Exception as e:
        results.append(CheckResult("Application booted", False, str(e)))
        return False, results

    overall = all(r.ok for r in results)
    return overall, results


@app.command("boot")
def cmd_boot(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
) -> None:
    ok, checks = run_boot_diagnostics(verbose=verbose)
    print("\nPrefiq Boot Doctor")
    print("------------------")
    for c in checks:
        line = f"{_fmt(c.ok)} {c.name}"
        if c.detail:
            line += f"  ·  {c.detail}"
        print(line)
    print("\nResult:", "ALL GOOD ✅" if ok else "ISSUES FOUND ❌")
    raise typer.Exit(0 if ok else 1)


# ──────────────────────────────────────────────────────────────────────────────
# Database helpers (portable, engine-agnostic)
# ──────────────────────────────────────────────────────────────────────────────

def _engine_name(e: Any) -> str:
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
    for attr in ("url", "database_url", "dsn"):
        v = getattr(engine, attr, None)
        if isinstance(v, str) and v.strip():
            return v
    return _mask_dsn(load_settings().dsn())


def _select1_ok(val: Any) -> bool:
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
    try:
        if isinstance(row, Sequence) and not isinstance(row, (str, bytes, bytearray)):
            return row[0]
        if isinstance(row, Mapping):
            for _, v in row.items():
                return v
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
    if hasattr(engine, "fetch_value") and callable(getattr(engine, "fetch_value")):
        return _await_if_needed(engine.fetch_value(sql), timeout)
    if hasattr(engine, "scalar") and callable(getattr(engine, "scalar")):
        return _await_if_needed(engine.scalar(sql), timeout)
    if hasattr(engine, "fetchone") and callable(getattr(engine, "fetchone")):
        row = _await_if_needed(engine.fetchone(sql), timeout)
        return _first_value(row)

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

    if hasattr(engine, "execute") and callable(getattr(engine, "execute")):
        cur = _await_if_needed(engine.execute(sql), timeout)
        if cur is not None and hasattr(cur, "fetchone"):
            row = cur.fetchone()
            return _first_value(row)

    raise RuntimeError("No compatible scalar fetch method found on engine")


def _probe_health(engine: Any, timeout: float | None = 3.0) -> bool:
    try:
        val = _get_scalar(engine, "SELECT 1", timeout=timeout)
        return _select1_ok(val)
    except Exception:
        return False


def _pool_stats(engine: Any) -> dict[str, Any]:
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


# ──────────────────────────────────────────────────────────────────────────────
# Database diagnostics
# ──────────────────────────────────────────────────────────────────────────────

@app.command("database")
def cmd_database(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
    strict: bool = typer.Option(False, "--strict", help="Exit non‑zero if unhealthy"),
) -> None:
    s = load_settings()
    print("=== Prefiq Database Doctor ===")
    print(f"DB_ENGINE='{getattr(s, 'DB_ENGINE', None)}'  DB_MODE='{getattr(s, 'DB_MODE', None)}'")

    engine = get_engine()
    print(f"Engine: {_engine_name(engine)}")

    if verbose:
        print(f"[verbose] DSN: {_display_dsn(engine)}")
        print(f"[verbose] DB_POOL_WARMUP: {getattr(s, 'DB_POOL_WARMUP', 0)}")
        st = _pool_stats(engine)
        if st:
            print(f"[verbose] pool: {st}")

    t0 = time.perf_counter()
    healthy = _probe_health(engine, timeout=3.0)
    dt_ms = (time.perf_counter() - t0) * 1000.0
    print(f"Health: {'OK' if healthy else 'FAIL'}" + (f"  ({dt_ms:.1f} ms)" if verbose else ""))

    if strict and not healthy:
        print("Strict mode: health check failed.")
        raise typer.Exit(1)

    # Smoke test
    try:
        print("-> Running smoke test (SELECT 1)")
        raw = _get_scalar(engine, "SELECT 1", timeout=3.0)
        val = _first_value(raw)
        ok = _select1_ok(val)
        print(f"   SELECT 1 => {val!r}  ({'OK' if ok else 'FAIL'})")
        if strict and not ok:
            raise typer.Exit(2)
    except Exception as e:
        print(f"Smoke test error: {type(e).__name__}: {e}")
        if strict:
            raise typer.Exit(2)

    # Optional engine swap demo (off by default)
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
    raise typer.Exit(0)


# ──────────────────────────────────────────────────────────────────────────────
# Migration diagnostics
# ──────────────────────────────────────────────────────────────────────────────

def run_migration_diagnostics(verbose: bool = False) -> Tuple[bool, List[CheckResult]]:
    results: List[CheckResult] = []

    try:
        providers = list(get_service_providers())
        app = Application.get_app()
        for p in providers:
            app.register(p)
        app.boot()
        results.append(CheckResult("Application booted", True, "Providers registered & booted"))
    except Exception as e:
        results.append(CheckResult("Application booted", False, str(e)))
        return False, results

    try:
        migrator = app.resolve("migrator")
        assert migrator is not None, "migrator not bound"
        results.append(CheckResult("Migrator bound", True, "Service key 'migrator' is available"))
    except Exception as e:
        results.append(CheckResult("Migrator bound", False, str(e)))
        return False, results

    overall = all(r.ok for r in results)
    return overall, results


@app.command("migrate")
def cmd_migrate(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    ok, checks = run_migration_diagnostics(verbose=verbose)
    print("\nPrefiq Migration Doctor")
    print("-----------------------")
    for c in checks:
        line = f"{_fmt(c.ok)} {c.name}"
        if c.detail:
            line += f"  ·  {c.detail}"
        print(line)
    print("\nResult:", "ALL GOOD ✅" if ok else "ISSUES FOUND ❌")
    raise typer.Exit(0 if ok else 1)


# ──────────────────────────────────────────────────────────────────────────────
# Entrypoint
# ──────────────────────────────────────────────────────────────────────────────

cli = app

def main() -> None:
    app()


if __name__ == "__main__":
    main()
