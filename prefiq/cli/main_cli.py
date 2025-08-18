# prefiq/cli/main_cli.py
from __future__ import annotations
import typer

from prefiq.cli.core.server import server_app   # your existing server group (prefiq server run)
from prefiq.cli.database.migrate import migrate     # function
from prefiq.cli.utils.tools import sanity, clear_cache  # functions

app = typer.Typer(help="Prefiq CLI")

# server group remains a Typer app on its own
app.add_typer(server_app, name="server")  # -> prefiq server run

# build a single "run" group and attach function commands to it
run_app = typer.Typer(help="Operational commands (migrate, sanity, cache)")
run_app.command("migrate")(migrate)           # -> prefiq run migrate [--seed --fresh --steps]
run_app.command("sanity")(sanity)             # -> prefiq run sanity
run_app.command("clear-cache")(clear_cache)   # -> prefiq run clear-cache
app.add_typer(run_app, name="run")

def main():
    app()

if __name__ == "__main__":
    main()
