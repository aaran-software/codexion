# cortex/providers/CortexProvider.py

from prefiq.core.application import register_provider
from prefiq.core.provider import Provider
from prefiq.http.routing import include_routes

@register_provider
class CortexProvider(Provider):
    abstract = False
    enabled  = True
    name     = "cortex"
    order    = 200

    def register(self) -> None:
        pass

    def boot(self) -> None:
        # Web -> /cortex
        include_routes("cortex.routes.web", prefix="/cortex", tags=["cortex:web"])
        # API -> /api/cortex
        include_routes("cortex.routes.api", prefix="/api/cortex", tags=["cortex:api"])
