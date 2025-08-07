from cortex.core.providers.database import DatabaseServiceProvider
from cortex.core.providers.config import ConfigServiceProvider
from cortex.core.providers.migration import MigrationServiceProvider
from cortex.core.providers.ui import UIServiceProvider

PROVIDERS = [
    DatabaseServiceProvider,
    ConfigServiceProvider,
    MigrationServiceProvider,
    UIServiceProvider,
]
