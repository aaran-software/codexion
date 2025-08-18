# prefiq/cli/migrate.py

import typer
from typing import Optional

# --- Apply logging configuration early (dictConfig + SQL filter) ---
# This import executes the dictConfig defined in prefiq/log/logging_config.py
# BEFORE any of the providers/bootstrap code starts logging.
import prefiq.log.logging_config  # noqa: F401

from prefiq.log.logger import get_logger
from prefiq.core.runtime.bootstrap import main as bootstrap_main
from prefiq.core.contracts.base_provider import Application

log = get_logger("prefiq.migrate")  # matches keys in logging_config

def migrate(
    seed: bool = typer.Option(False, "--seed", help="Run seeders after migrations"),
    fresh: bool = typer.Option(False, "--fresh", help="Drop all non-protected tables then migrate"),
    steps: Optional[int] = typer.Option(None, "--steps", help="Rollback N steps before migrating"),
    env: Optional[str] = typer.Option(None, "--env", help="dev|prod|stage|test"),
):
    # Normalize environment first so logging reflects the right env if used in messages
    from prefiq.cli.core.server import _apply_env
    _apply_env(env)

    # Providers bind & boot — logs from here onward are filtered/configured
    log.info("boot_start (migrate)")
    bootstrap_main()

    appc = Application.get_app()
    migrator = appc.resolve("migrator")
    if not migrator:
        raise RuntimeError("Migrator service not available. Is MigrationProvider registered?")

    if steps:
        msg = f"⏪ Rolling back {steps} step(s) before migrating..."
        typer.echo(msg)
        log.info("rollback_requested", extra={"steps": steps})
        migrator.rollback(steps=steps)

    if fresh:
        typer.echo("🧹 Dropping tables (fresh) and migrating...")
        log.info("fresh_migrate_requested", extra={"seed": seed})
        migrator.fresh(seed=seed)
    else:
        typer.echo("📦 Applying migrations...")
        log.info("migrate_requested", extra={"seed": seed})
        migrator.migrate(seed=seed)

    typer.echo("✅ Migrations complete.")
    log.info("migrations_complete")
