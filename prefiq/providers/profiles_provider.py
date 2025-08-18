# prefiq/core/contracts/providers/profiles_provider.py

from typing import Any, Dict, Optional
from prefiq.core.contracts.base_provider import BaseProvider, Application
from prefiq.log.logger import get_logger

log = get_logger("prefiq.settings")

class ProfilesProvider(BaseProvider):
    """
    ProfilesProvider
    ----------------
    Manages structured configuration profiles for different services.
    If no explicit profiles are passed, it will try to build a minimal default
    from the loaded settings; otherwise falls back to an empty dict.
    """

    def __init__(self, app: Application, profiles: Optional[Dict[str, Dict[str, Any]]] = None):
        super().__init__(app)

        # try to consume settings if already bound (SettingsProvider is first in PROVIDERS)
        settings = app.resolve("settings")
        if profiles is not None:
            self._profiles = profiles
        elif settings is not None:
            # keep this minimal; you can expand later with whatever you need
            # example: expose DB info in a neutral way (avoid secrets)
            db_name = getattr(settings, "DB_NAME", None)
            db_host = getattr(settings, "DB_HOST", None)
            db_engine = getattr(settings, "DB_ENGINE", None)
            self._profiles = {
                "database": {
                    "engine": db_engine,
                    "host": db_host,
                    "name": db_name,
                }
            }
        else:
            self._profiles = {}

    def register(self) -> None:
        self.app.bind("profiles", self._profiles)

    def boot(self) -> None:
        log.info("[ProfilesProvider]" " Profiles initialized.", extra={"profiles": self._profiles})
