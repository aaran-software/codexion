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
        include_routes("apps.devmeta.routes.web", prefix="/devmeta", tags=["devmeta:web"])
        include_routes("apps.devmeta.routes.api", prefix="/api/devmeta", tags=["devmeta:api"])
