from cortex.core.providers.base import ServiceProvider

class UIServiceProvider(ServiceProvider):
    def register(self):
        self.app.singleton("ui", lambda: "UI ready")

    def boot(self):
        print("UIServiceProvider booted")
