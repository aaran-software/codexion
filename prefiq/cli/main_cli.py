from __future__ import annotations
import typer

from prefiq.cli.core.server import server_app   # existing server group (prefiq server run)
from prefiq.cli.database.migrate import migrate     # function
from prefiq.cli.utils.tools import sanity, clear_cache  # functions

app = typer.Typer(help="Prefiq CLI")

# Keep server group as-is
app.add_typer(server_app, name="server")  # -> prefiq server run

# "run" group with function commands
run_app = typer.Typer(help="Operational commands (migrate, sanity, cache)")
run_app.command("migrate")(migrate)           # -> prefiq run migrate [--seed --fresh --steps]
run_app.command("sanity")(sanity)             # -> prefiq run sanity
run_app.command("clear-cache")(clear_cache)   # -> prefiq run clear-cache
app.add_typer(run_app, name="run")

# ---- Optional: Mount DevMeta CLI if available ----
# This keeps your main CLI independent, but enables "prefiq devmeta ..." automatically
try:
    # Prefer the devmeta Typer app directly if the module is importable
    from apps.devmeta.cli.devmeta import app as devmeta_app  # type: ignore
    if isinstance(devmeta_app, typer.Typer):
        app.add_typer(devmeta_app, name="devmeta")
except Exception:
    # Silently ignore if DevMeta isn't present in this build
    pass

# Provide an alternative alias some containers look for
# (lets DI code resolve a CLI host by 'cli' if they don't import this module's 'app' name directly)
cli = app

def main():
    app()

if __name__ == "__main__":
    main()
