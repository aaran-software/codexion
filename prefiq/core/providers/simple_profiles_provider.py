# prefiq/core/contracts/providers/simple_profiles_provider.py

from typing import Any, Dict
from prefiq.core.contracts.base_provider import BaseProvider, Application


class ProfilesProvider(BaseProvider):
    """
    ProfilesProvider
    ----------------
    Manages structured configuration profiles for different services
    (e.g., database, AI, UI, integrations).
    """

    def __init__(self, app: Application, profiles: Dict[str, Dict[str, Any]]):
        super().__init__(app)
        self._profiles = profiles

    def register(self) -> None:
        """Register profiles in the application container."""
        self.app.bind("profiles", self._profiles)

    def boot(self) -> None:
        """Optional boot logic for profiles (e.g., validation)."""
        print("[ProfilesProvider] Profiles initialized.")
