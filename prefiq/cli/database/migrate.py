# prefiq/cli/migrate.py
import typer
from typing import Optional
from prefiq.core.runtime.bootstrap import main as bootstrap_main
from prefiq.core.contracts.base_provider import Application

def migrate(
    seed: bool = typer.Option(False, "--seed", help="Run seeders after migrations"),
    fresh: bool = typer.Option(False, "--fresh", help="Drop all non-protected tables then migrate"),
    steps: Optional[int] = typer.Option(None, "--steps", help="Rollback N steps before migrating"),
    env: Optional[str] = typer.Option(None, "--env", help="dev|prod|stage|test"),
):
    from prefiq.cli.core.server import _apply_env  # reuse env normalization if you have it there
    _apply_env(env)

    bootstrap_main()  # bind providers
    appc = Application.get_app()
    migrator = appc.resolve("migrator")
    if not migrator:
        raise RuntimeError("Migrator service not available. Is MigrationProvider registered?")

    if steps:
        typer.echo(f"⏪ Rolling back {steps} step(s) before migrating...")
        migrator.rollback(steps=steps)

    if fresh:
        typer.echo("🧹 Dropping tables (fresh) and migrating...")
        migrator.fresh(seed=seed)
    else:
        typer.echo("📦 Applying migrations...")
        migrator.migrate(seed=seed)

    typer.echo("✅ Migrations complete.")
