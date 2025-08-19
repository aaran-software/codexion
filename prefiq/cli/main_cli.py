from __future__ import annotations
import typer

from prefiq.cli.core.server import server_app   # existing server group (prefiq server run)
from prefiq.cli.database.migrate import migrate     # function
from prefiq.cli.utils.tools import sanity, clear_cache  # functions
from prefiq.cli.checkup.manage_doctor import doctor_app      # <-- NEW

app = typer.Typer(help="Prefiq CLI")

# Keep server group as-is
app.add_typer(server_app, name="server")  # -> prefiq server run

# "run" group with function commands
run_app = typer.Typer(help="Operational commands (migrate, sanity, cache)")
run_app.command("migrate")(migrate)           # -> prefiq run migrate [--seed --fresh --steps]
run_app.command("sanity")(sanity)             # -> prefiq run sanity
run_app.command("clear-cache")(clear_cache)   # -> prefiq run clear-cache
app.add_typer(run_app, name="run")

# ---- Doctor group (new) ----
# Now: prefiq doctor boot
app.add_typer(doctor_app, name="doctor")

# ---- Optional: Mount DevMeta CLI if available ----
try:
    from apps.devmeta.cli.devmeta import app as devmeta_app  # type: ignore
    if isinstance(devmeta_app, typer.Typer):
        app.add_typer(devmeta_app, name="devmeta")
except Exception:
    pass

cli = app

def main():
    app()

if __name__ == "__main__":
    main()
