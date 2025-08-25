# prefiq/providers/http_provider.py

from __future__ import annotations
import importlib
from fastapi import FastAPI

from prefiq.core.provider import Provider
from prefiq.apps.app_cfg import get_registered_apps
from prefiq.core.logger import get_logger

log = get_logger("http")

class HttpProvider(Provider):
    abstract = False
    enabled = True
    name = "http"
    order = 200  # after db/migrations

    def register(self) -> None:
        from prefiq.core.application import Application
        app = Application.get_app()

        fastapi_app = FastAPI(title="Prefiq Server")
        app.bind("http.app", fastapi_app)

        # Load routes from all apps
        for app_name in get_registered_apps():
            for kind in ("web", "api"):
                mod_name = f"apps.{app_name}.routes.{kind}"
                try:
                    mod = importlib.import_module(mod_name)
                    router = getattr(mod, "router", None)
                    if router:
                        prefix = f"/{app_name}/{kind}" if kind == "api" else f"/{app_name}"
                        fastapi_app.include_router(router, prefix=prefix)
                        log.info("Mounted %s routes from %s", kind, mod_name)
                except ModuleNotFoundError:
                    continue
                except Exception as e:
                    log.error("Failed to import %s: %s", mod_name, e)

    def boot(self) -> None:
        pass
