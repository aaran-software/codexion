# prefiq/providers/settings_provider.py

from pydantic import ValidationError
from prefiq.core.contracts.base_provider import Application, BaseProvider
from prefiq.settings.get_settings import get_settings, clear_settings_cache
from prefiq.utils.logger import get_logger

log = get_logger("prefiq.settings")

class SettingsProvider(BaseProvider):
    """
    Loads global application settings (from env/.env) using prefiq.settings.
    Binds them into the Application container as 'settings'.
    Also validates config for providers that declare schema models.
    """

    def register(self) -> None:
        # Load from prefiq/settings.py (cached singleton)
        settings = get_settings()
        self.app.bind("settings", settings)

        # Validation step: loop over providers that declare schema
        errors = []
        for provider_cls in Application.provider_registry:  # <-- correct usage
            namespace = getattr(provider_cls, "schema_namespace", None)
            model = getattr(provider_cls, "schema_model", None)
            if namespace and model:
                try:
                    # Get namespace dict if available, otherwise pass empty dict
                    namespace_config = getattr(settings, namespace, {})
                    model(**namespace_config)
                except ValidationError as e:
                    errors.append(f"[{provider_cls.__name__}] Invalid config for '{namespace}': {e}")

        if errors:
            raise RuntimeError("Settings validation failed:\n" + "\n".join(errors))

    def boot(self) -> None:
        settings = self.app.resolve("settings")
        env = getattr(settings, "ENV", "development")
        log.info("settings_loaded", extra={"env": env})

    # Optional helper to clear cached settings (for tests)
    def clear(self) -> None:
        clear_settings_cache()
        self.app.bind("settings", get_settings())
