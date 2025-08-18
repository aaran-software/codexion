from __future__ import annotations

from typing import Any, Optional
import typer
from datetime import datetime

from prefiq.log.logger import get_logger

LOG = get_logger("prefiq.devmeta.cli.devmeta")
def _ensure_devmeta_bound():
    from prefiq.core.contracts.base_provider import Application
    appc = _ensure_devmeta_bound()
    try:
        mig = appc.resolve("devmeta.migrator")
        if mig:
            return appc
    except Exception:
        pass
    # Try registering the provider on the fly
    try:
        from apps.devmeta.core.provider import DevMetaProvider  # type: ignore
    except Exception:
        try:
            # Fallback import path if layout differs
            from apps.devmeta.provider import DevMetaProvider  # type: ignore
        except Exception:
            DevMetaProvider = None  # type: ignore
    if DevMetaProvider is not None:
        prov = DevMetaProvider()
        try:
            prov.register(appc)
        except Exception:
            pass
        try:
            prov.boot(appc)
        except Exception:
            pass
    return appc


# The actual Typer subapp for DevMeta.
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


# ------------- Commands -------------

@app.command("migrate")
def cmd_migrate():
    """Apply all pending migrations for DevMeta."""
    from prefiq.core.contracts.base_provider import Application
    appc = _ensure_devmeta_bound()
    migrator = appc.resolve("devmeta.migrator")
    applied = migrator.migrate()
    typer.echo(f"✅ Applied {applied} migration(s).")


@app.command("rollback")
def cmd_rollback(steps: int = typer.Option(1, "--steps", help="Number of migrations to roll back")):
    from prefiq.core.contracts.base_provider import Application
    appc = _ensure_devmeta_bound()
    migrator = appc.resolve("devmeta.migrator")
    done = migrator.rollback(steps=steps)
    typer.echo(f"⏪ Rolled back {done} migration(s).")


# --- Todo commands ---

def _resolve_todo_service():
    from prefiq.core.contracts.base_provider import Application
    appc = _ensure_devmeta_bound()
    try:
        return appc.resolve("devmeta.todo")
    except Exception:
        return None


@app.command("todo-add")
def todo_add(
    title: str = typer.Argument(..., help="Title of the todo"),
    priority: int = typer.Option(3, "--priority", "-p"),
    project: Optional[str] = typer.Option(None, "--project"),
    due_at: Optional[str] = typer.Option(None, "--due-at", help="ISO datetime, e.g. 2025-08-18T15:00:00"),
    tags: Optional[str] = typer.Option(None, "--tags", help="Comma-separated"),
):
    """Add a new todo."""
    svc = _resolve_todo_service()
    if not svc:
        typer.echo("⚠️ TodoService not bound. (Provider will bind if apps.devmeta.services.todo.bind_todo_service is present.)")
        raise typer.Exit(code=1)

    parsed_due = None
    if due_at:
        try:
            parsed_due = datetime.fromisoformat(due_at)
        except Exception:
            typer.echo("Invalid --due-at; expected ISO format like 2025-08-18T15:00:00")
            raise typer.Exit(code=2)

    todo = svc.add(title=title, priority=priority, project=project, due_at=parsed_due, tags=tags)
    typer.echo(f"➕ Added todo #{todo.id}: {todo.title}")


@app.command("todo-list")
def todo_list(
    status: Optional[str] = typer.Option(None, "--status", "-s", help="Filter by status (open, done, etc.)"),
    limit: int = typer.Option(50, "--limit", help="Max rows"),
):
    """List todos."""
    svc = _resolve_todo_service()
    if not svc:
        typer.echo("⚠️ TodoService not bound. (Provider will bind if apps.devmeta.services.todo.bind_todo_service is present.)")
        raise typer.Exit(code=1)

    rows = svc.list(status=status, limit=limit)
    if not rows:
        typer.echo("No todos.")
        raise typer.Exit()

    for t in rows:
        due = t.due_at.isoformat() if getattr(t, "due_at", None) else "-"
        comp = t.completed_at.isoformat() if getattr(t, "completed_at", None) else "-"
        typer.echo(f"[#{t.id}] {t.title} | status={t.status} | p={t.priority} | project={t.project or '-'} | due={due} | done={comp}")


@app.command("todo-done")
def todo_done(todo_id: int = typer.Argument(..., help="ID of the todo")):
    """Mark a todo as done."""
    svc = _resolve_todo_service()
    if not svc:
        typer.echo("⚠️ TodoService not bound. (Provider will bind if apps.devmeta.services.todo.bind_todo_service is present.)")
        raise typer.Exit(code=1)

    ok = svc.done(todo_id)
    if not ok:
        typer.echo(f"Todo #{todo_id} not found.")
        raise typer.Exit(code=1)
    typer.echo(f"✅ Done: #{todo_id}")
