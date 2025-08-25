# prefiq/http/app.py
from __future__ import annotations

import inspect
from pathlib import Path

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from fastapi import FastAPI

from prefiq.core.bootstrap import main as bootstrap_main
from prefiq.core.application import Application
from prefiq.database.connection_manager import connection_manager


def _prepare_http_app(app: FastAPI) -> FastAPI:
    """
    Idempotently attach global middleware, default routes and a centralized
    shutdown hook so both foreground and daemon paths behave the same.
    """
    if getattr(app, "_prefiq_prepared", False):
        return app

    # ---- global middleware ----
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ---- default routes ----
    @app.get("/favicon.ico", include_in_schema=False)
    def favicon():
        icon_path = Path(__file__).parent / "assets" / "images" / "favicon.svg"
        if icon_path.exists():
            return FileResponse(icon_path)
        # no favicon available — avoid raising at runtime
        return Response(status_code=204)

    @app.get("/")
    def root():
        return {"status": "running"}

    @app.get("/healthz", tags=["system"])
    def healthz():
        ok = False
        try:
            ok = connection_manager.test()
        except (ValueError, TypeError):
            ok = False
        return {"ok": ok}

    # ---- centralized shutdown (runs while event loop is alive) ----
    @app.on_event("shutdown")
    async def _close_services():
        # 1) close via connection manager
        try:
            eng = connection_manager.get_engine()
            if hasattr(eng, "close"):
                res = eng.close()
                if inspect.isawaitable(res):
                    await res
        except Exception:
            pass

        # 2) best-effort: close MariaDB pool if present (ignore if not installed)
        try:
            from prefiq.database.engines.mariadb.pool import close_pool  # type: ignore
            res = close_pool()
            if inspect.isawaitable(res):
                await res
        except (ModuleNotFoundError, ImportError, AttributeError, TypeError, ValueError):
            pass

    setattr(app, "_prefiq_prepared", True)
    return app


def build_http_app() -> FastAPI:
    """
    Uvicorn factory target: `uvicorn prefiq.http.app:build_http_app --factory`
    Ensures providers are bootstrapped, then returns prepared FastAPI app.
    """
    bootstrap_main()
    app = Application.get_app().resolve("http.app")
    if app is None or not isinstance(app, FastAPI):
        raise RuntimeError("No HTTP app bound. Did your Providers mount routes?")
    return _prepare_http_app(app)


__all__ = ["build_http_app"]
