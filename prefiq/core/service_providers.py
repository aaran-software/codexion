# prefiq/core/service_providers.py

from prefiq.core.providers.settings_provider import SettingsProvider
from prefiq.core.providers.profiles_provider import ProfilesProvider
from prefiq.providers.database_provider import DatabaseProvider
# from cortex.core.providers.ui_provider import UiProvider

# Global registry of service providers
PROVIDERS = [
    SettingsProvider,
    ProfilesProvider,
    DatabaseProvider,
    # UiProvider,
]
