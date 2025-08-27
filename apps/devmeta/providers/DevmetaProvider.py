# devmeta/providers/DevmetaProvider.py

from prefiq.core.provider import Provider
from prefiq.http.routing import include_routes

class DevmetaProvider(Provider):
    abstract = False
    enabled  = True
    name     = "devmeta"
    order    = 300

    def register(self) -> None:
        pass

    def boot(self) -> None:

        # 1) run migrations once on startup
        try:
            from apps.devmeta.devmeta.project.migrations import run_migrations
            run_migrations()
        except Exception as e:
            # don't kill the app on migration hiccups; surface in logs if you have a logger
            print(f"[devmeta] migrations skipped/failed: {e!r}")

        # 2) mount routes
        include_routes("apps.devmeta.devmeta.project.api", prefix="/api", tags=["projects"])
