# prefiq/cli/doctor.py
from __future__ import annotations

import asyncio
import inspect
import os
import time
import logging
from dataclasses import dataclass
from typing import Any, List, Tuple, Optional, Dict
from collections.abc import Sequence, Mapping

import typer

from prefiq.core.logger import get_logger, banner, okc, failx, colorize
from prefiq.core.application import Application
from prefiq.core.service_providers import get_service_providers
from prefiq.settings.get_settings import load_settings, clear_settings_cache
from prefiq.database.connection import (
    get_engine,
    reset_engine,
    reload_engine_from_env,
)

app = typer.Typer(help="Health checks and diagnostics")
log = get_logger("cli.doctor")

# Keys we understand for DB config
_DB_KEYS = (
    "DB_ENGINE",
    "DB_MODE",
    "DB_HOST",
    "DB_PORT",
    "DB_USER",
    "DB_PASS",
    "DB_NAME",
    "DB_POOL_WARMUP",
)


@dataclass
class CheckResult:
    name: str
    ok: bool
    detail: str = ""


def _fmt(ok: bool) -> str:
    return "✅" if ok else "❌"


# ──────────────────────────────────────────────
# Boot diagnostics
# ──────────────────────────────────────────────

def run_boot_diagnostics(verbose: bool = False) -> Tuple[bool, List[CheckResult]]:
    results: List[CheckResult] = []

    try:
        settings = load_settings()
        results.append(CheckResult("Settings loaded", True, f"ENV={getattr(settings, 'ENV', 'development')}"))
    except Exception as e:
        results.append(CheckResult("Settings loaded", False, str(e)))
        return False, results

    try:
        providers = list(get_service_providers())
        prov_names = [getattr(p, "__name__", str(p)) for p in providers]
        results.append(CheckResult("Providers discovered", True, ", ".join(prov_names)))
    except Exception as e:
        results.append(CheckResult("Providers discovered", False, str(e)))
        return False, results

    try:
        _app = Application.get_app()
        for p in providers:
            _app.register(p)
        _app.boot()
        results.append(CheckResult("Application booted", True, "Lifecycle callbacks executed"))
    except Exception as e:
        results.append(CheckResult("Application booted", False, str(e)))
        return False, results

    overall = all(r.ok for r in results)
    return overall, results


def _maybe_verbose(verbose: bool) -> None:
    if verbose:
        try:
            logging.getLogger().setLevel(logging.DEBUG)
        except (ValueError, TypeError):
            pass


@app.command("boot")
def cmd_boot(verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")) -> None:
    _maybe_verbose(verbose)
    log.info("%s", banner("=== Prefiq Boot Doctor ===", color="cyan", blank_before=True))
    ok, checks = run_boot_diagnostics(verbose=verbose)
    for c in checks:
        badge = _fmt(c.ok)
        (log.info if c.ok else log.error)("%s %s  ·  %s", badge, c.name, c.detail)
    if ok:
        log.info("%s", okc("Result: ALL GOOD ✅"))
    else:
        log.error("%s", failx("Result: ISSUES FOUND ❌"))
    raise typer.Exit(0 if ok else 1)


# ──────────────────────────────────────────────
# Env patching for named profiles
# ──────────────────────────────────────────────

def _read_prefixed_env(name: str) -> Dict[str, str]:
    pref = name.upper()
    out: Dict[str, str] = {}
    for k in _DB_KEYS:
        v = os.getenv(f"{pref}_{k}")
        if v is not None:
            out[k] = v
    return out


from contextlib import contextmanager
@contextmanager
def _scoped_db_env_from_profile(profile: str):
    overrides = _read_prefixed_env(profile)
    if not overrides and profile != "DEFAULT":
        yield
        return
    prior: Dict[str, Optional[str]] = {k: os.getenv(k) for k in overrides.keys()}
    try:
        for k, v in overrides.items():
            os.environ[k] = v
        clear_settings_cache()
        reset_engine()
        log.debug("Scoped to profile %s with overrides: %s", profile, list(overrides.keys()))
        yield
    finally:
        for k, old in prior.items():
            if old is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = old
        clear_settings_cache()
        reset_engine()
        log.debug("Restored env after profile %s", profile)


# ──────────────────────────────────────────────
# Database helpers
# ──────────────────────────────────────────────

def _engine_name(e: Any) -> str:
    for attr in ("name", "dialect_name", "driver"):
        v = getattr(e, attr, None)
        if isinstance(v, str) and v.strip():
            return v
    cls = type(e).__name__
    if "Maria" in cls: return f"MariaDB/{cls}"
    if "SQLite" in cls or "Sqlite" in cls: return f"SQLite/{cls}"
    if "Postgres" in cls or "Pg" in cls: return f"Postgres/{cls}"
    return cls


def _mask_dsn(dsn: Optional[str]) -> str:
    if not dsn: return "<none>"
    s = load_settings()
    pw = getattr(s, "DB_PASS", None)
    try:
        if pw and pw in dsn:
            return dsn.replace(pw, "*****")
    except (ValueError, TypeError):
        pass
    return dsn


def _display_dsn(engine: Any) -> str:
    for attr in ("url", "database_url", "dsn"):
        v = getattr(engine, attr, None)
        if isinstance(v, str) and v.strip():
            return v
    return _mask_dsn(load_settings().dsn())


def _select1_ok(val: Any) -> bool:
    if val is None: return False
    try:
        if val is True: return True
        if isinstance(val, (int, float)): return int(val) == 1
        return str(val) == "1"
    except Exception:
        return False


def _first_value(row: Any) -> Any:
    try:
        if isinstance(row, Sequence) and not isinstance(row, (str, bytes, bytearray)):
            return row[0]
        if isinstance(row, Mapping):
            for _, v in row.items(): return v
        if hasattr(row, "__getitem__") and not isinstance(row, (str, bytes, bytearray)):
            try: return row[0]
            except Exception: pass
        return row
    except Exception:
        return row


def _await_if_needed(x: Any, timeout: float | None) -> Any:
    if inspect.isawaitable(x):
        try: loop = asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(asyncio.wait_for(x, timeout)) if timeout else asyncio.run(x)
        else:
            return loop.run_until_complete(asyncio.wait_for(x, timeout)) if timeout else loop.run_until_complete(x)
    return x


def _get_scalar(engine: Any, sql: str, timeout: float | None = 3.0) -> Any:
    if hasattr(engine, "fetch_value"): return _await_if_needed(engine.fetch_value(sql), timeout)
    if hasattr(engine, "scalar"): return _await_if_needed(engine.scalar(sql), timeout)
    if hasattr(engine, "fetchone"): return _first_value(_await_if_needed(engine.fetchone(sql), timeout))
    if hasattr(engine, "execute"):
        cur = _await_if_needed(engine.execute(sql), timeout)
        if cur is not None and hasattr(cur, "fetchone"):
            return _first_value(cur.fetchone())
    raise RuntimeError("No compatible scalar fetch method found on engine")


def _probe_health(engine: Any, timeout: float | None = 3.0) -> bool:
    try: return _select1_ok(_get_scalar(engine, "SELECT 1", timeout))
    except Exception: return False


def _pool_stats(engine: Any) -> dict[str, Any]:
    stats: dict[str, Any] = {}
    try:
        if hasattr(engine, "pool_stats"): stats = dict(engine.pool_stats())
    except Exception: pass
    return stats


# ──────────────────────────────────────────────
# Database diagnostics
# ──────────────────────────────────────────────

def _check_current_engine(verbose: bool = False, strict: bool = False) -> int:
    s = load_settings()
    log.info("DB_ENGINE=%r  DB_MODE=%r", getattr(s, "DB_ENGINE", None), getattr(s, "DB_MODE", None))
    engine = get_engine()
    log.info("Engine: %s", _engine_name(engine))
    if verbose:
        log.debug("DSN: %s", _display_dsn(engine))
        log.debug("DB_POOL_WARMUP: %s", getattr(s, "DB_POOL_WARMUP", 0))
    t0 = time.perf_counter()
    healthy = _probe_health(engine, timeout=3.0)
    dt_ms = (time.perf_counter() - t0) * 1000.0
    (log.info if healthy else log.error)(
        "Health: %s%s", "OK" if healthy else "FAIL", f" ({dt_ms:.1f} ms)" if verbose else ""
    )
    if strict and not healthy: return 1
    try:
        log.info("-> Running smoke test (SELECT 1)")
        val = _first_value(_get_scalar(engine, "SELECT 1", timeout=3.0))
        ok = _select1_ok(val)
        (log.info if ok else log.error)("SELECT 1 => %r  (%s)", val, "OK" if ok else "FAIL")
        if strict and not ok: return 2
    except Exception as e:
        log.exception("Smoke test error: %s: %s", type(e).__name__, e)
        if strict: return 2
    return 0


@app.command("database")
def cmd_database(verbose: bool = typer.Option(False, "--verbose", "-v"), strict: bool = typer.Option(False, "--strict")) -> None:
    _maybe_verbose(verbose)
    log.info("%s", banner("=== Prefiq Database Doctor (default) ===", color="cyan", blank_before=True))
    code = _check_current_engine(verbose=verbose, strict=strict)
    if code == 0:
        log.info("%s", okc("Database doctor finished — ALL GOOD ✅"))
    else:
        log.error("%s", failx("Database doctor finished — ISSUES FOUND ❌"))
    raise typer.Exit(code)


@app.command("database-all")
def cmd_database_all(verbose: bool = typer.Option(False, "--verbose", "-v"), strict: bool = typer.Option(False, "--strict")) -> None:
    _maybe_verbose(verbose)
    profiles = [("DEFAULT", None), ("DEV", "DEV"), ("ANALYTICS", "ANALYTICS")]
    worst_code = 0
    for label, pref in profiles:
        log.info("%s", banner(f"=== Prefiq Database Doctor [{label}] ===", color="cyan", blank_before=True))
        if pref is None:
            clear_settings_cache(); reset_engine()
            code = _check_current_engine(verbose=verbose, strict=strict)
        else:
            with _scoped_db_env_from_profile(pref):
                reload_engine_from_env(force_refresh=True)
                code = _check_current_engine(verbose=verbose, strict=strict)
        worst_code = max(worst_code, code)
    if worst_code == 0:
        log.info("%s", okc("Database doctor (all) finished — ALL GOOD ✅"))
    else:
        log.error("%s", failx("Database doctor (all) finished — ISSUES FOUND ❌"))
    raise typer.Exit(worst_code)


# ──────────────────────────────────────────────
# Migration diagnostics
# ──────────────────────────────────────────────

def run_migration_diagnostics(verbose: bool = False) -> Tuple[bool, List[CheckResult]]:
    results: List[CheckResult] = []
    try:
        providers = list(get_service_providers())
        _app = Application.get_app()
        for p in providers:
            _app.register(p)
        _app.boot()
        results.append(CheckResult("Application booted", True, "Providers registered & booted"))
    except Exception as e:
        results.append(CheckResult("Application booted", False, str(e)))
        return False, results
    try:
        migrator = _app.resolve("migrator")
        assert migrator is not None, "migrator not bound"
        results.append(CheckResult("Migrator bound", True, "Service key 'migrator' is available"))
    except Exception as e:
        results.append(CheckResult("Migrator bound", False, str(e)))
        return False, results
    return all(r.ok for r in results), results


@app.command("migrate")
def cmd_migrate(verbose: bool = typer.Option(False, "--verbose", "-v")) -> None:
    _maybe_verbose(verbose)
    log.info("%s", banner("=== Prefiq Migration Doctor ===", color="cyan", blank_before=True))
    ok, checks = run_migration_diagnostics(verbose=verbose)
    for c in checks:
        badge = _fmt(c.ok)
        (log.info if c.ok else log.error)("%s %s  ·  %s", badge, c.name, c.detail)
    if ok:
        log.info("%s", okc("Result: 💚 ALL GOOD ✅"))
    else:
        log.error("%s", failx("Result: ISSUES FOUND ❌"))
    raise typer.Exit(0 if ok else 1)


cli = app
def main() -> None: app()
if __name__ == "__main__": main()
