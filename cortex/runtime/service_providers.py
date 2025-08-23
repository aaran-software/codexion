# cortex/runtime/service_providers.py
# from apps.devmeta.provider import DevMetaProvider
# from prefiq.providers.migration_provider import MigrationProvider
from prefiq.providers.settings_provider import SettingsProvider
from prefiq.providers.profiles_provider import ProfilesProvider
from prefiq.providers.database_provider import DatabaseProvider

# from cortex.core.providers.ui_provider import UiProvider

# Global registry of service providers
PROVIDERS = [
    SettingsProvider,
    ProfilesProvider,
    DatabaseProvider,
    # MigrationProvider,
    # DevMetaProvider
    # UiProvider,
]
