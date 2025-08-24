# prefiq/cli/database/migrate.py
from __future__ import annotations
import typer

from prefiq.core.application import Application
from cortex.runtime.service_providers import PROVIDERS
from prefiq.core.logger import get_logger

log = get_logger("prefiq.run.migrate")
migrate_app = typer.Typer(help="Database migration runner")

def _boot_app():
    appc = Application.get_app()
    for p in PROVIDERS:
        appc.register(p)
    appc.boot()
    return appc

@migrate_app.command()
def migrate(
    seed: bool = typer.Option(False, "--seed", help="Run seeders after migrating"),
    fresh: bool = typer.Option(False, "--fresh", help="Drop all tables then run migrations"),
    steps: int = typer.Option(0, "--steps", help="Rollback this many steps before migrating (0=none)"),
):
    """
    Run database migrations with optional seeding or fresh (drop+recreate).
    """
    appc = _boot_app()
    migrator = appc.resolve("migrator")
    if migrator is None:
        raise typer.Exit(code=2)

    # Optional rollback N steps first
    if steps and steps > 0:
        log.info("rollback_start", extra={"steps": steps})
        migrator.rollback(steps=steps)
        log.info("rollback_done", extra={"steps": steps})

    if fresh:
        log.info("fresh_start")
        migrator.fresh(seed=seed)
        log.info("fresh_done")
    else:
        log.info("migrate_start")
        migrator.migrate(seed=seed)
        log.info("migrate_done")
