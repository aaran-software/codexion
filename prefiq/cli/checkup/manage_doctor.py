from __future__ import annotations
import typer

from prefiq.cli.checkup.boot_doctor import main as boot_doctor_main

doctor_app = typer.Typer(help="Health checks and diagnostics")

@doctor_app.command("boot")
def boot(verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")):
    """Run boot sequence diagnostics (settings, providers, DB)."""
    code = boot_doctor_main(verbose=verbose)
    raise typer.Exit(code)

@doctor_app.command("database")
def database(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
    strict: bool = typer.Option(False, "--strict", help="Fail (exit 1) if DB provider is not configured"),
):
    """Run database diagnostics (provider → engine → connectivity)."""
    from prefiq.cli.checkup.database_doctor import main as db_doctor_main  # lazy import
    code = db_doctor_main(verbose=verbose, strict=strict)
    raise typer.Exit(code)