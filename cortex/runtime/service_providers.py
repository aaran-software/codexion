# cortex/runtime/service_providers.py
# from apps.devmeta.provider import DevMetaProvider
from prefiq.providers.migration_provider import MigrationProvider
from prefiq.providers.config_provider import ConfigProvider
from prefiq.providers.database_provider import DatabaseProvider

# from cortex.core.providers.ui_provider import UiProvider

# Global registry of service providers
PROVIDERS = [
    ConfigProvider,
    DatabaseProvider,
    MigrationProvider,
    # DevMetaProvider
    # UiProvider,
]
