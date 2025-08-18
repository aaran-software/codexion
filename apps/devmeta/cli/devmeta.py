# apps/devmeta/cli/devmeta.py

from __future__ import annotations

from typing import Any, Optional
import typer

from prefiq.log.logger import get_logger

LOG = get_logger("prefiq.devmeta.cli.devmeta")

# The actual Typer subapp for DevMeta.
# We'll attach commands later (migrate, todo add/list/done, etc.)
app = typer.Typer(help="DevMeta: developer metadata (todos, notes, logs).")

# Internal flag key used to ensure we mount only once.
_MOUNT_FLAG_KEY = "devmeta.cli.mounted"


def _resolve_cli_host(container) -> Optional[Any]:
    """
    Try to locate the main Typer CLI host from the DI container.

    Expected keys (in order):
      - "cli.app"  -> a Typer() instance
      - "cli"      -> either a Typer() instance or an object exposing add_typer()
    """
    for key in ("cli.app", "cli"):
        try:
            cli_app = container.resolve(key)
            if cli_app:
                return cli_app
        except Exception:
            continue
    return None


def mount_devmeta_cli(container) -> bool:
    """
    Mount the DevMeta Typer subapp under the main CLI host as `devmeta`.

    - If the CLI host isn't present, this is a no-op (logs a breadcrumb).
    - Idempotent: won't mount twice if provider.boot() runs multiple times.

    Returns:
        True if mounted (or already mounted), False if skipped.
    """
    # Already mounted?
    try:
        if container.resolve(_MOUNT_FLAG_KEY):
            LOG.info("cli_mount_skipped", extra={"reason": "already mounted"})
            return True
    except Exception:
        pass

    cli_host = _resolve_cli_host(container)
    if cli_host is None:
        LOG.info("cli_mount_skipped", extra={"reason": "no cli host found"})
        return False

    try:
        mounted = False

        # Prefer Typer's API
        add_typer = getattr(cli_host, "add_typer", None)
        if callable(add_typer):
            add_typer(app, name="devmeta")
            LOG.info("cli_mounted", extra={"name": "devmeta", "method": "add_typer"})
            mounted = True
        else:
            # Optional custom host API
            mount = getattr(cli_host, "mount_subapp", None)
            if callable(mount):
                mount("devmeta", app)
                LOG.info("cli_mounted", extra={"name": "devmeta", "method": "mount_subapp"})
                mounted = True

        if not mounted:
            LOG.info(
                "cli_mount_skipped",
                extra={"reason": "host lacks add_typer/mount_subapp"},
            )
            return False

        # mark as mounted for idempotency
        try:
            container.bind(_MOUNT_FLAG_KEY, True)
        except Exception:
            pass

        return True

    except Exception as e:
        LOG.error("cli_mount_failed", extra={"error": f"{type(e).__name__}: {e}"})
        return False
