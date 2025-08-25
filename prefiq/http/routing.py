# prefiq/http/routing.py

from importlib import import_module
from typing import Optional, List
try:
    from fastapi import FastAPI  # runtime dep
except Exception as e:  # pragma: no cover
    FastAPI = None  # type: ignore[assignment]

from prefiq.core.application import Application

def get_http_app() -> "FastAPI":
    if FastAPI is None:
        raise RuntimeError("FastAPI not available. Install `fastapi` to use routing.")
    app = Application.get_app().resolve("http.app")
    if app is None:
        app = FastAPI(title="Prefiq")
        Application.get_app().bind("http.app", app)
    return app

def include_routes(import_path: str, *, prefix: str = "", tags: Optional[List[str]] = None) -> None:
    """
    Import a module that exposes `router: APIRouter` and mount it on the shared FastAPI app.
    """
    mod = import_module(import_path)
    router = getattr(mod, "router", None)
    if router is None:
        raise RuntimeError(f"{import_path!r} does not export a `router`")
    app = get_http_app()
    app.include_router(router, prefix=prefix, tags=tags or [])
