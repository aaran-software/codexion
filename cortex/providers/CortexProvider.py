# providers/CortexProvider.py

from prefiq.core.application import register_provider
from prefiq.core.provider import Provider  # your base Provider

@register_provider
class CortexProvider(Provider):
    abstract = False
    enabled  = True
    name     = "cortex"
    order    = 2

    def register(self) -> None:
        # bind services, singletons, configs
        pass

    def boot(self) -> None:
        # run boot-time hooks after all providers are registered
        pass
