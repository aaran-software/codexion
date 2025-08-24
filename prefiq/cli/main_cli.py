from __future__ import annotations
import sys
import typer

# ---- Doctor group: keep this lightweight and import eagerly ----
from prefiq.cli.checkup.manage_doctor import doctor_app

app = typer.Typer(help="Prefiq CLI")

# Doctor is safe to mount eagerly
app.add_typer(doctor_app, name="doctor")


def _mount_optional_groups() -> None:
    """
    Lazily mount CLI groups that pull heavy deps (server/run/app) *only if requested*.
    This prevents import-time side effects when running 'prefiq doctor boot' etc.
    """
    argv = set(sys.argv[1:])

    # 'server' group only if explicitly used
    if "server" in argv:
        from prefiq.cli.core.server import server_app  # heavy: imports bootstrap/providers
        app.add_typer(server_app, name="server")

    # 'app' group only if explicitly used
    if "app" in argv:
        # NOTE: import the Typer instance we exposed above
        from prefiq.cli.apps.builder import app_builder_cmd
        app.add_typer(app_builder_cmd, name="app")

    # 'run' group only if explicitly used
    if "run" in argv:
        from prefiq.cli.database.migrate import migrate
        from prefiq.cli.utils.tools import sanity, clear_cache

        run_app = typer.Typer(help="Operational commands (migrate, sanity, cache)")
        run_app.command("migrate")(migrate)           # -> prefiq run migrate [--seed --fresh --steps]
        run_app.command("sanity")(sanity)             # -> prefiq run sanity
        run_app.command("clear-cache")(clear_cache)   # -> prefiq run clear-cache

        app.add_typer(run_app, name="run")

    # Optional: DevMeta only if explicitly requested
    if "devmeta" in argv:
        try:
            from apps.devmeta.cli.devmeta import app as devmeta_app  # type: ignore
            if isinstance(devmeta_app, typer.Typer):
                app.add_typer(devmeta_app, name="devmeta")
        except Exception:
            # Silently ignore if DevMeta isn't present
            pass


# Provide an alternative alias some containers look for
cli = app

def main() -> None:
    _mount_optional_groups()
    app()


if __name__ == "__main__":
    main()
