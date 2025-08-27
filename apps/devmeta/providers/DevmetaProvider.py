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

        include_routes("apps.devmeta.core.routes.api", prefix="/api", tags=["projects"])
        include_routes("apps.devmeta.core.routes.web", prefix="", tags=["projects"])
