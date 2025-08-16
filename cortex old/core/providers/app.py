import os
from cortex.core.providers.di import Container
from cortex.core.providers.registry import Registry
from cortex.core.providers.config_loader import load_env, load_config_modules

class Docs:
    def __init__(self, env_file=".env", config_folder="config"):
        load_env(env_file)
        self.env = os.getenv("APP_ENV", "local")
        self.config = load_config_modules(config_folder)
        self.container = Container()
        self.registry = Registry()
        self.providers = []

    def register(self, provider_cls):
        provider = provider_cls(self)
        provider.register()
        self.providers.append(provider)

    def boot(self):
        for provider in self.providers:
            provider.boot()

    def singleton(self, key, factory):
        self.container.singleton(key, factory)

    def bind(self, key, value):
        self.container.bind(key, value)

    def make(self, key):
        return self.container.make(key)

    def call(self, func):
        return self.container.resolve(func)

    def run_command(self, name):
        if name in self.registry.commands:
            return self.registry.commands[name]()
        raise ValueError(f"Command {name} not found")
