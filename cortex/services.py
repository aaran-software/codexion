# services.py

from typing import List, Type

class ServiceProvider:
    def register(self):
        """Register bindings in the container."""
        pass

    def boot(self):
        """Bootstrapping logic after all providers are registered."""
        pass


def get_service_providers() -> List[Type[ServiceProvider]]:
    """
    Return a list of service provider classes to be registered.

    Add your custom providers here.
    """
    from cortex.providers.logger_provider import LoggerServiceProvider

    from cortex.providers.database_provider import DatabaseServiceProvider
    # Add more as needed

    return [
        LoggerServiceProvider,
        DatabaseServiceProvider,
    ]
