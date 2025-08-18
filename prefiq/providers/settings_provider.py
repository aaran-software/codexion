# prefiq/providers/settings_provider.py

from __future__ import annotations

import os
from typing import Any, Dict, Iterable

from pydantic import ValidationError
from prefiq.core.contracts.base_provider import Application, BaseProvider
from prefiq.settings.get_settings import load_settings, clear_settings_cache
from prefiq.log.logger import get_logger

log = get_logger("prefiq.settings")


class SettingsProvider(BaseProvider):
    """
    Loads global application settings (from env/.env) using prefiq.settings.
    Binds them into the Application container as 'settings'.
    Also validates config for providers that declare schema models.
    """

    def register(self) -> None:
        # Load from prefiq/settings (cached singleton) and bind
        settings = load_settings()
        self.app.bind("settings", settings)

        # Try to obtain the provider registry (support multiple shapes)
        provider_registry = (
            getattr(Application, "provider_registry", None)
            or getattr(self.app, "provider_registry", None)
            or []
        )

        errors: list[str] = []

        for provider_cls in provider_registry:
            # Provider may optionally declare schema_model and (optionally) schema_namespace
            model = getattr(provider_cls, "schema_model", None)
            namespace = getattr(provider_cls, "schema_namespace", None)

            if not model:
                continue  # nothing to validate

            # Prefer building payload from model field names on Settings (flat env style)
            # e.g., DatabaseSettings fields: DB_ENGINE, DB_MODE, DB_HOST, ...
            try:
                model_fields: Iterable[str] = getattr(model, "model_fields", {}).keys()  # pydantic v2
            except Exception:
                model_fields = []

            payload: Dict[str, Any] = {}

            # Fill from flat Settings attributes if present
            for key in model_fields:
                if hasattr(settings, key):
                    payload[key] = getattr(settings, key)

            # If nothing matched AND provider offered a namespace, try that as a dict on Settings
            if not payload and namespace and hasattr(settings, namespace):
                ns_val = getattr(settings, namespace)
                if isinstance(ns_val, dict):
                    payload = dict(ns_val)  # copy

            # Validate if we gathered anything; if model has required fields,
            # pydantic will complain if they’re missing (which is what we want).
            try:
                # pydantic v2
                if hasattr(model, "model_validate"):
                    model.model_validate(payload)
                else:
                    # pydantic v1 fallback, just in case
                    model(**payload)
            except ValidationError as e:
                errors.append(
                    f"[{provider_cls.__name__}] invalid config: {e}"
                )

        if errors:
            # Fail fast with a helpful, aggregated message
            raise RuntimeError("Settings validation failed:\n" + "\n".join(errors))

    def boot(self) -> None:
        settings = self.app.resolve("settings")
        # ENV may be provided via .env / OS; default to "development"
        env = getattr(settings, "ENV", os.getenv("ENV", "development"))
        log.info("settings_loaded", extra={"env": env})

    # Optional helper to clear cached settings (for tests)
    def clear(self) -> None:
        clear_settings_cache()
        self.app.bind("settings", load_settings())
