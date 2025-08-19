from __future__ import annotations
import typer

from prefiq.cli.checkup.boot_doctor import main as boot_doctor_main

doctor_app = typer.Typer(help="Health checks and diagnostics")

@doctor_app.command("boot")
def boot(verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")):
    """Run boot sequence diagnostics (settings, providers, DB)."""
    code = boot_doctor_main(verbose=verbose)
    raise typer.Exit(code)
