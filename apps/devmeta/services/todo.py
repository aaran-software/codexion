# apps/devmeta/services/hooks.py
from __future__ import annotations

from typing import Optional, Callable, Any

from prefiq.log.logger import get_logger

from apps.devmeta.core.helper import connect_sqlite

LOG = get_logger("prefiq.devmeta.services.hooks")


def _bind_singleton(app, key: str, factory: Callable[[], Any]) -> None:
    """
    Bind a singleton instance to the container under `key` if not already bound.
    This is defensive and idempotent.
    """
    try:
        # If resolve succeeds, assume it's already bound.
        existing = app.resolve(key)
        if existing is not None:
            LOG.info("service_already_bound", extra={"key": key})
            return
    except Exception:
        # Not bound yet — proceed to bind.
        pass

    try:
        instance = factory()
        app.bind(key, instance)
        LOG.info("service_bound", extra={"key": key})
    except Exception as e:
        LOG.error("service_bind_failed", extra={"key": key, "error": repr(e)})


# ---------------------------- Todo Service ----------------------------

def bind_todo_service(app, db_path: str) -> None:
    """
    Bind TodoService as 'devmeta.todo_service' using the shared SQLite connector.
    Keeps provider resilient if the module isn't implemented yet.
    """
    try:
        from apps.devmeta.services.todo import TodoService  # local import
    except Exception as e:
        LOG.warning("todo_service_not_available", extra={"reason": repr(e)})
        return

    def factory():
        # Give the service a simple connector; service may open/close per op.
        return TodoService(db_path=db_path, connect_fn=connect_sqlite)

    _bind_singleton(app, "devmeta.todo_service", factory)


# -------------------------- Future service hooks ----------------------

def bind_note_service(app, db_path: str) -> None:
    """
    Placeholder for NoteService binding (future).
    """
    try:
        from apps.devmeta.services.note import NoteService  # type: ignore
    except Exception as e:
        LOG.info("note_service_not_available", extra={"reason": repr(e)})
        return

    def factory():
        return NoteService(db_path=db_path, connect_fn=connect_sqlite)  # type: ignore

    _bind_singleton(app, "devmeta.note_service", factory)


def bind_log_service(app, db_path: str) -> None:
    """
    Placeholder for LogService binding (future).
    """
    try:
        from apps.devmeta.services.log import LogService  # type: ignore
    except Exception as e:
        LOG.info("log_service_not_available", extra={"reason": repr(e)})
        return

    def factory():
        return LogService(db_path=db_path, connect_fn=connect_sqlite)  # type: ignore

    _bind_singleton(app, "devmeta.log_service", factory)
