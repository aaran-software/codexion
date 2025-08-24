# prefiq/core/application.py
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Type, Union, Iterable


__all__ = [
    "Application",
    "BaseProvider",
    "register_provider",
]


class Application:
    """
    Minimal application container (singleton).
    - Holds service bindings
    - Manages provider lifecycle (register → boot)
    - Supports booting callbacks
    - Supports decorator-based provider auto-registration
    """

    _instance: Optional["Application"] = None

    # Filled by @register_provider; import-time classes are queued here
    provider_registry: List[Type["BaseProvider"]] = []

    def __new__(cls) -> "Application":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        # guard against re-init for the singleton
        if getattr(self, "_initialized", False):
            return
        self._providers: List["BaseProvider"] = []
        self._booting_callbacks: List[Callable[[], None]] = []
        self._booted_callbacks: List[Callable[[], None]] = []
        self._published_paths: Dict[str, str] = {}
        self._services: Dict[str, Any] = {}
        self._booted: bool = False
        self._initialized = True

    # ---------- Provider management ----------

    def register(
        self,
        provider_cls_or_instance: Union[Type["BaseProvider"], "BaseProvider"],
    ) -> "BaseProvider":
        """
        Register a provider (class or instance) and call its register() hook.
        Returns the provider instance for chaining/testing.
        """
        if isinstance(provider_cls_or_instance, type):
            provider = provider_cls_or_instance(self)
        else:
            provider = provider_cls_or_instance

        provider.register()
        self._providers.append(provider)
        return provider

    def register_many(
        self,
        providers: Iterable[Union[Type["BaseProvider"], "BaseProvider"]],
    ) -> None:
        for p in providers:
            self.register(p)

    def register_decorated_providers(self) -> None:
        """
        Register all providers that were marked with @register_provider.
        Safe to call multiple times; duplicates are avoided by identity check.
        """
        queued = list(self.provider_registry)
        if not queued:
            return

        existing_ids = {id(p) for p in self._providers}
        for prov_cls in queued:
            # avoid re-adding an already-instantiated provider of the same class
            if any(isinstance(p, prov_cls) for p in self._providers):
                continue
            inst = prov_cls(self)
            inst.register()
            if id(inst) not in existing_ids:
                self._providers.append(inst)

    def boot(self) -> None:
        """
        Boot sequence:
          1) run booting callbacks
          2) auto-register any decorated providers
          3) call boot() on all registered providers
          4) run booted callbacks
        """
        if self._booted:
            return

        for cb in self._booting_callbacks:
            cb()

        # Ensure providers added via decorator are included before boot
        self.register_decorated_providers()

        for provider in self._providers:
            provider.boot()

        self._booted = True

        for cb in self._booted_callbacks:
            cb()

    # ---------- Lifecycle callbacks ----------

    def on_booting(self, callback: Callable[[], None]) -> None:
        self._booting_callbacks.append(callback)

    def on_booted(self, callback: Callable[[], None]) -> None:
        self._booted_callbacks.append(callback)

    # ---------- Services & resources ----------

    def publish(self, key: str, path: str) -> None:
        self._published_paths[key] = path

    def bind(self, key: str, service: Any) -> None:
        self._services[key] = service

    def resolve(self, key: str) -> Optional[Any]:
        return self._services.get(key)

    # ---------- Singleton access ----------

    @classmethod
    def get_app(cls) -> "Application":
        return cls()

    # Placeholder for future async runner (kept for compatibility)
    def run_async(self, _param: Any) -> None:  # noqa: D401 (intentional no-op)
        """No-op hook for frameworks that expect an async runner handle."""
        return


class BaseProvider(ABC):
    """
    Base class for service providers.

    Optional attributes for settings validation (if you use a config validator):
    - schema_namespace: Name under which a dict config may be nested on Settings
    - schema_model:     A Pydantic model (or similar) to validate config for this provider
    """
    schema_namespace: Optional[str] = None
    schema_model: Optional[Any] = None

    def __init__(self, app: Application) -> None:
        self.app = app

    @abstractmethod
    def register(self) -> None:
        """Bind services into the container."""

    @abstractmethod
    def boot(self) -> None:
        """Run startup logic after all providers have registered."""

    # Optional helpers to keep provider code tidy
    def load_routes(self, routes_file: str) -> None:
        # Intentionally no logging/printing; leave visibility to consumers.
        pass

    def load_translations(self, namespace: str, path: str) -> None:
        self.app.publish(namespace, path)


def register_provider(cls: Type[BaseProvider]) -> Type[BaseProvider]:
    """
    Decorator to opt a provider class into auto-registration.
    Importing a module that defines a decorated provider is enough;
    the Application will register these just before boot().
    """
    Application.provider_registry.append(cls)
    return cls
