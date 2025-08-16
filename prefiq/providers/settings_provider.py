# cortex/core/providers/settings_provider.py
from pydantic import ValidationError
from cortex.core.contracts.base_provider import Application, BaseProvider, register_provider

@register_provider
class SettingsProvider(BaseProvider):
    def register(self) -> None:
        merged = self._load_all_sources()
        self.app.bind("settings", merged)

        # Validation step: loop over providers with declared schema
        errors = []
        for provider_cls in Application.provider_registry:
            if getattr(provider_cls, "schema_namespace", None) and getattr(provider_cls, "schema_model", None):
                namespace = provider_cls.schema_namespace
                model = provider_cls.schema_model
                try:
                    model(**merged.get(namespace, {}))
                except ValidationError as e:
                    errors.append(f"[{provider_cls.__name__}] Invalid config for '{namespace}': {e}")

        if errors:
            raise RuntimeError("Settings validation failed:\n" + "\n".join(errors))

    def boot(self) -> None:
        print(f"[SettingsProvider] Loaded settings for ENV={self.env}")
