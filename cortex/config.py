# config.py

import os
from cortex.core.settings import get_settings, clear_settings_cache


def load_config():
    """
    Loads environment config (via Pydantic settings or custom logic).
    Called once during application bootstrap.
    """
    clear_settings_cache()  # Ensure fresh load (important during testing/dev)
    settings = get_settings()

    # Optionally bind config to container here
    from cortex.container import container
    container.bind("config", settings)

    print("⚙️  Config loaded from .env and environment variables.")
