# cortex/core/contracts/base_provider.py

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Type, Union


class Application:
    """
    Core application container (singleton).
    Manages service providers, lifecycle callbacks, and shared services.
    """

    _instance: Optional["Application"] = None
    provider_registry: List[Type["BaseProvider"]] = []  # public registry for decorated providers

    def __new__(cls) -> "Application":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):
            self._providers: List["BaseProvider"] = []
            self._booting_callbacks: List[Callable[[], None]] = []
            self._booted_callbacks: List[Callable[[], None]] = []
            self._published_paths: Dict[str, str] = {}
            self._services: Dict[str, Any] = {}
            self._booted: bool = False
            self._initialized = True

    # --- Provider Management ---

    def register(self, provider_cls_or_instance: Union[Type["BaseProvider"], "BaseProvider"]) -> "BaseProvider":
        """Register a provider (class or instance)."""
        if isinstance(provider_cls_or_instance, type):
            provider_instance = provider_cls_or_instance(self)
        else:
            provider_instance = provider_cls_or_instance
        provider_instance.register()
        self._providers.append(provider_instance)
        return provider_instance

    def register_decorated_providers(self) -> None:
        """Register all providers added via @register_provider decorator."""
        for provider_cls in self.provider_registry:
            self.register(provider_cls)

    def boot(self) -> None:
        """Boot all registered providers and trigger lifecycle callbacks."""
        for cb in self._booting_callbacks:
            cb()

        # auto-register decorator providers before boot
        self.register_decorated_providers()

        for provider in self._providers:
            provider.boot()

        self._booted = True

        for cb in self._booted_callbacks:
            cb()

    # --- Lifecycle Callbacks ---

    def on_booting(self, callback: Callable[[], None]) -> None:
        self._booting_callbacks.append(callback)

    def on_booted(self, callback: Callable[[], None]) -> None:
        self._booted_callbacks.append(callback)

    # --- Services & Resources ---

    def publish(self, key: str, path: str) -> None:
        self._published_paths[key] = path

    def bind(self, key: str, service: Any) -> None:
        self._services[key] = service

    def resolve(self, key: str) -> Optional[Any]:
        return self._services.get(key)

    # --- Singleton Access ---

    @classmethod
    def get_app(cls) -> "Application":
        """Return the global singleton application instance."""
        return cls()


class BaseProvider(ABC):
    """Abstract base class for service providers."""
    schema_namespace: Optional[str] = None   # e.g. "database"
    schema_model: Optional[Any] = None       # e.g. Pydantic model

    def __init__(self, app: Application) -> None:
        self.app = app

    @abstractmethod
    def register(self) -> None:
        ...

    @abstractmethod
    def boot(self) -> None:
        ...

    # --- Optional helpers ---
    def load_routes(self, routes_file: str) -> None:
        print(f"[{self.__class__.__name__}] Loading routes from {routes_file}")

    def load_translations(self, namespace: str, path: str) -> None:
        self.app.publish(namespace, path)


# --- Decorator for auto-registration ---

def register_provider(cls: Type[BaseProvider]) -> Type[BaseProvider]:
    """
    Decorator to mark a class as a provider that should be auto-registered
    when the application boots.
    """
    Application.provider_registry.append(cls)
    return cls
