# prefiq/core/contracts/providers/settings_provider.py

import os
from dotenv import load_dotenv
from prefiq.core.contracts.base_provider import BaseProvider, register_provider


@register_provider
class SettingsProvider(BaseProvider):
    """
    Loads application settings from .env and environment variables,
    registers them globally under 'settings'.
    """

    def __init__(self, app, env_file: str = ".env"):
        super().__init__(app)
        self.env_file = env_file
        self.settings = {}

    def register(self) -> None:
        # Load .env (if present) + system env
        load_dotenv(self.env_file, override=False)

        # Store into dict
        self.settings = dict(os.environ)

        # Bind settings globally
        self.app.bind("settings", self.settings)

    def boot(self) -> None:
        print(f"[SettingsProvider] Booted with {len(self.settings)} variables")
