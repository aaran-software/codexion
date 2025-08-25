# apps/cli/devmetadatabase.py
from __future__ import annotations

import typer
import time
import inspect
from typing import Any
from collections.abc import Sequence, Mapping

from prefiq.core.logger import get_logger, banner, okc, failx
from prefiq.settings.get_settings import clear_settings_cache, load_settings
from prefiq.database.connection import (
    engine_env,
    get_engine_named,
    reload_engine_from_env,
)
from prefiq.database.connection_manager import dev_connection_manager as DEV_CM

devmeta_app = typer.Typer(help="Devmeta database tools (scoped to DEV_* env)")

log = get_logger("apps.devmeta.cli")


# ──────────────────────────────────────────────
# Small helpers (trimmed from doctor)
# ──────────────────────────────────────────────
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

def _await_if_needed(x: Any, timeout: float | None) -> Any:
    if inspect.isawaitable(x):
        # DEV profile uses sqlite sync; this is defensive
        import asyncio
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(asyncio.wait_for(x, timeout)) if timeout else asyncio.run(x)
        else:
            return loop.run_until_complete(asyncio.wait_for(x, timeout)) if timeout else loop.run_until_complete(x)
    return x

def _get_scalar(engine: Any, sql: str, timeout: float | None = 3.0) -> Any:
    if hasattr(engine, "fetch_value"):
        return _await_if_needed(engine.fetch_value(sql), timeout)
    if hasattr(engine, "scalar"):
        return _await_if_needed(engine.scalar(sql), timeout)
    if hasattr(engine, "fetchone"):
        return _first_value(_await_if_needed(engine.fetchone(sql), timeout))
    if hasattr(engine, "execute"):
        cur = _await_if_needed(engine.execute(sql), timeout)
        if cur is not None and hasattr(cur, "fetchone"):
            return _first_value(cur.fetchone())
    raise RuntimeError("No compatible scalar fetch method found on engine")


# ──────────────────────────────────────────────
# Commands
# ──────────────────────────────────────────────

@devmeta_app.command("database")
def dev_database(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
    strict: bool = typer.Option(False, "--strict", help="Non‑zero exit on failure"),
) -> None:
    """
    Health check for the DEV named database (uses DEV_DB_* env).
    """
    # Ensure Settings reflect DEV_* values while we run
    with engine_env("DEV"):
        clear_settings_cache()
        reload_engine_from_env(force_refresh=True)

        s = load_settings()
        log.info("%s", banner("=== Devmeta Database (DEV profile) ===", color="cyan", blank_before=True))
        log.info("DB_ENGINE=%r  DB_MODE=%r  DB_NAME=%r", s.DB_ENGINE, s.DB_MODE, s.DB_NAME)

        # Ensure the named engine exists
        eng = get_engine_named("DEV")
        eng_name = type(eng).__name__
        log.info("Engine: %s", eng_name)

        # quick pool/connection test (manager is pinned to DEV already)
        t0 = time.perf_counter()
        ok = False
        try:
            val = _get_scalar(eng, "SELECT 1", timeout=3.0)
            ok = _select1_ok(val)
            dt = (time.perf_counter() - t0) * 1000.0
            (log.info if ok else log.error)("SELECT 1 => %r  (%s)  %.1f ms", val, "OK" if ok else "FAIL", dt)
        except Exception as e:
            log.exception("Health check error: %s", e)

        if ok:
            log.info("%s", okc("Result: ALL GOOD ✅"))
            raise typer.Exit(0)
        else:
            log.error("%s", failx("Result: ISSUES FOUND ❌"))
            raise typer.Exit(1 if strict else 0)


@devmeta_app.command("migrate")
def dev_migrate(
    steps: int | None = typer.Option(None, "--steps", help="Run only the next N migrations"),
    fresh: bool = typer.Option(False, "--fresh", help="Drop and re-run"),
    seed: bool = typer.Option(False, "--seed", help="Run seeders after migrations"),
) -> None:
    """
    Run migrations scoped to DEV named database (DEV_DB_*).
    """
    with engine_env("DEV"):
        clear_settings_cache()
        reload_engine_from_env(force_refresh=True)

        log.info("%s", banner("=== Devmeta Migrate (DEV profile) ===", color="cyan", blank_before=True))

        # Try the shared migrator first
        try:
            from prefiq.cli.database.migrate import migrate as shared_migrate  # type: ignore
        except Exception:
            shared_migrate = None

        if shared_migrate:
            # Only pass kwargs that the shared CLI actually accepts.
            import inspect
            sig = inspect.signature(shared_migrate)
            call_kwargs = {}
            if "steps" in sig.parameters:
                call_kwargs["steps"] = steps
            if "fresh" in sig.parameters:
                call_kwargs["fresh"] = fresh
            if "seed" in sig.parameters:
                call_kwargs["seed"] = seed

            try:
                shared_migrate(**call_kwargs)  # type: ignore[misc]
            except Exception as e:
                log.debug("shared_migrate failed (%s). Falling back to inline migrator.", e)
                _run_inline_migrator(fresh=fresh, steps=steps, seed=seed)
        else:
            _run_inline_migrator(fresh=fresh, steps=steps, seed=seed)

        log.info("%s", okc("Migrations complete ✅"))
        raise typer.Exit(0)


def _run_inline_migrator(*, fresh: bool, steps: int | None, seed: bool) -> None:
    from prefiq.core.application import Application
    from prefiq.core.service_providers import get_service_providers

    app = Application.get_app()
    for pcls in get_service_providers():
        app.register(pcls)
    app.boot()

    migrator = app.resolve("migrator")
    if not migrator:
        log.error("Migrator service not found. Is MigrationProvider enabled?")
        raise typer.Exit(1)

    # Try to mirror the shared API
    if fresh and hasattr(migrator, "fresh"):
        try:
            migrator.fresh(seed=seed)  # supports seed if available
        except TypeError:
            migrator.fresh()
        return

    if steps and hasattr(migrator, "migrate_steps"):
        migrator.migrate_steps(steps)
        if seed and hasattr(migrator, "seed"):
            migrator.seed()
        return

    if hasattr(migrator, "migrate"):
        migrator.migrate()
        if seed and hasattr(migrator, "seed"):
            migrator.seed()
        return

    log.error("No compatible migrate method on migrator.")
    raise typer.Exit(1)
