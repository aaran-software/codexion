# providers/DevmetaProvider.py
# Auto-registered Provider for devmeta
from prefiq.core.provider import Provider  # your base Provider

class DevmetaProvider(Provider):
    abstract = False
    enabled  = True
    name     = "devmeta"
    order    = None  # will be injected/overridden by config during boot if needed

    def register(self) -> None:
        # bind services, singletons, configs
        pass

    def boot(self) -> None:
        # run boot-time hooks after all providers are registered
        pass
