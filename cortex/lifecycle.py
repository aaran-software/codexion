# lifecycle.py

from cortex.services import get_service_providers
from cortex.config import load_config
from cortex.container import container


class AppLifecycle:
    def __init__(self):
        self.config = None
        self.providers = []

    def load_config(self):
        self.config = load_config()
        container.bind("config", self.config)

    def register_providers(self):
        for provider_class in get_service_providers():
            provider = provider_class()
            provider.register(container)
            self.providers.append(provider)

    def boot_providers(self):
        for provider in self.providers:
            provider.boot(container)

    def run(self):
        print("🚀 Starting application lifecycle...")
        self.load_config()
        self.register_providers()
        self.boot_providers()
        print("✅ Application booted successfully.")
