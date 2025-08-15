from cortex.core.providers.base import ServiceProvider

class ConfigServiceProvider(ServiceProvider):
    def register(self):
        self.app.singleton("config", lambda: self.config)

    def boot(self):
        print("ConfigServiceProvider booted")
