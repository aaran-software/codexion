# prefiq/providers/config_provider.py
from __future__ import annotations

from typing import Any, Dict, Iterable, Optional

from pydantic import ValidationError

from prefiq.core.application import Application, BaseProvider, register_provider
from prefiq.settings.get_settings import load_settings, clear_settings_cache

try:
    from prefiq.core.provider import all_providers as _all_providers
except Exception:  # pragma: no cover
    _all_providers = None  # type: ignore[assignment]

@register_provider
class ConfigProvider(BaseProvider):
    """
    Binds:
      - 'settings'  -> Prefiq Settings (pydantic BaseSettings)
      - 'profiles'  -> minimal structured config derived from settings (overridable)

    Also performs schema validation for any providers that declare:
      - schema_model (a Pydantic model)
      - schema_namespace (optional string for namespaced dict on Settings)

    Supports BOTH provider systems:
      1) Decorator-based:  Application.provider_registry  (BaseProvider subclasses)
      2) Metaclass-based:  prefiq.core.provider.all_providers() (Provider subclasses)
    """

    def __init__(self, app: Application, profiles: Optional[Dict[str, Dict[str, Any]]] = None):
        super().__init__(app)
        self._profiles_override = profiles

    # ---------- public API ----------

    def register(self) -> None:
        # Bind settings (singleton cached in get_settings)
        settings = load_settings()
        self.app.bind("settings", settings)

        # Bind profiles: override > derived-from-settings > {}
        profiles = (
            self._profiles_override
            if self._profiles_override is not None
            else _derive_profiles_from_settings(settings)
        )
        self.app.bind("profiles", profiles)

        # Validate config against any declared provider schemas (best-effort)
        self._validate_declared_schemas(settings)

    def boot(self) -> None:
        # Intentionally no logging/printing here; keep boot clean.
        # If you need to act on settings after boot, add hooks/callbacks externally.
        return

    # Testing/ops helper to refresh settings without restarting the app
    def clear_settings_cache(self) -> None:
        clear_settings_cache()
        self.app.bind("settings", load_settings())

    # ---------- internals ----------

    def _validate_declared_schemas(self, settings: Any) -> None:
        """
        Aggregate schema declarations from both provider registries and validate them.
        Raises RuntimeError with all errors combined, if any.
        """
        provider_classes: list[type] = []

        # 1) Decorator-based BaseProvider registry (Application.provider_registry)
        provider_classes.extend(getattr(Application, "provider_registry", []) or [])

        # 2) Metaclass-based Provider registry (prefiq.core.provider)
        try:
            if callable(_all_providers):
                provider_classes.extend(_all_providers() or [])
        except Exception:
            # Ignore if provider base isn't available yet
            pass

        if not provider_classes:
            return

        errors: list[str] = []
        for provider_cls in provider_classes:
            model = getattr(provider_cls, "schema_model", None)
            namespace = getattr(provider_cls, "schema_namespace", None)
            if not model:
                continue  # nothing to validate

            payload: Dict[str, Any] = {}
            # Prefer building payload from model field names on Settings (flat env style)
            model_fields: Iterable[str] = []
            try:
                # pydantic v2
                model_fields = getattr(model, "model_fields", {}).keys()
            except Exception:
                # pydantic v1 fallback (names only if accessible)
                try:
                    model_fields = getattr(model, "__fields__", {}).keys()  # type: ignore[attr-defined]
                except Exception:
                    model_fields = []

            for key in model_fields:
                if hasattr(settings, key):
                    payload[key] = getattr(settings, key)

            # If still empty and a namespace is declared, try a dict under that attr on Settings
            if not payload and namespace and hasattr(settings, namespace):
                ns_val = getattr(settings, namespace)
                if isinstance(ns_val, dict):
                    payload = dict(ns_val)  # copy

            # Skip if we couldn't gather anything (no required fields met)
            if not payload:
                continue

            # Validate (pydantic v2 first; fallback to v1-style constructor)
            try:
                if hasattr(model, "model_validate"):
                    model.model_validate(payload)  # pydantic v2
                else:
                    model(**payload)               # pydantic v1
            except ValidationError as e:
                errors.append(f"[{getattr(provider_cls, '__name__', 'Provider')}] invalid config: {e}")

        if errors:
            raise RuntimeError("Settings validation failed:\n" + "\n".join(errors))


# ---------- helpers ----------

def _derive_profiles_from_settings(settings: Any) -> Dict[str, Dict[str, Any]]:
    """
    Construct a minimal, non-secret 'profiles' mapping derived from Settings.
    This is intentionally small; extend as your framework needs grow.
    """
    db_engine = getattr(settings, "DB_ENGINE", None)
    db_host   = getattr(settings, "DB_HOST", None)
    db_name   = getattr(settings, "DB_NAME", None)

    return {
        "database": {
            "engine": db_engine,
            "host": db_host,
            "name": db_name,
        }
    }
