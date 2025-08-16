# cortex/core/providers/service_providers.py

from cortex.core.providers.settings_provider import SettingsProvider
from cortex.core.providers.profiles_provider import ProfilesProvider
from cortex.providers.database_provider import DatabaseProvider
# from cortex.core.providers.ui_provider import UiProvider

# Global registry of service providers
PROVIDERS = [
    SettingsProvider,
    ProfilesProvider,
    DatabaseProvider,
    # UiProvider,
]
