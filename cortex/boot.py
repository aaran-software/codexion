# boot.py

from cortex.services import get_service_providers
from cortex.container import container

def boot_providers():
    providers = []

    # First register all services
    for provider_cls in get_service_providers():
        provider = provider_cls()
        provider.register()
        providers.append(provider)

    # Then call boot method on all
    for provider in providers:
        provider.boot()
