# main.py

from __future__ import annotations
import sys
import typer

app = typer.Typer(help="Prefiq CLI")

from prefiq.cli.doctor import app as doctor_app
app.add_typer(doctor_app, name="doctor")


def _mount_optional_groups() -> None:

    argv = set(sys.argv[1:])

    if "server" in argv:
        # heavy: imports bootstrap/providers
        from prefiq.cli.core.server import server_app  # type: ignore
        app.add_typer(server_app, name="server")

    if "app" in argv:
        from prefiq.cli.apps import apps_app
        app.add_typer(apps_app, name="app")

    if "provider" in argv:
        from prefiq.cli.providers import providers_app
        app.add_typer(providers_app, name="provider")

    if "run" in argv:
        # operational commands (keep imports local)
        from prefiq.cli.database.migrate import migrate  # type: ignore
        from prefiq.cli.utils.tools import sanity, clear_cache  # type: ignore

        run_app = typer.Typer(help="Operational commands (migrate, sanity, cache)")
        run_app.command("migrate")(migrate)           # prefiq run migrate [--seed --fresh --steps N]
        run_app.command("sanity")(sanity)             # prefiq run sanity
        run_app.command("clear-cache")(clear_cache)   # prefiq run clear-cache
        app.add_typer(run_app, name="run")

    if "devmeta" in argv:
        # optional third-party/dev module
        try:
            from apps.devmeta.cli.devmeta import devmeta_app  # type: ignore
            if isinstance(devmeta_app, typer.Typer):
                app.add_typer(devmeta_app, name="devmeta")
        except (ValueError, TypeError):
            # silently ignore if missing
            pass


# Alias some containers look for
cli = app


def main() -> None:
    _mount_optional_groups()
    app()


if __name__ == "__main__":
    main()
