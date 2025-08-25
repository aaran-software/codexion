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
    _instance: Optional["Application"] = None
    provider_registry: List[Type["BaseProvider"]] = []

    def __new__(cls) -> "Application":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
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
            cls = provider_cls_or_instance
            # Support both ctor signatures:
            #   - BaseProvider(app)
            #   - Provider()
            try:
                provider = cls(self)  # BaseProvider style
            except TypeError:
                provider = cls()      # metaclass Provider (zero-arg)
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
        queued = list(self.provider_registry)
        if not queued:
            return

        filtered = []
        for q in queued:
            try:
                if isinstance(q, type) and issubclass(q, BaseProvider):
                    filtered.append(q)
            except Exception:
                pass
        type(self).provider_registry = filtered

        existing_classes = {p.__class__ for p in self._providers}
        for prov_cls in filtered:
            if prov_cls in existing_classes:
                continue
            try:
                inst = prov_cls(self)   # BaseProvider style
            except TypeError:
                inst = prov_cls()       # zero-arg
            inst.register()
            self._providers.append(inst)

    def boot(self) -> None:
        if self._booted:
            return

        for cb in self._booting_callbacks:
            cb()

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

    def run_async(self, _param: Any) -> None:
        return


class BaseProvider(ABC):
    schema_namespace: Optional[str] = None
    schema_model: Optional[Any] = None

    def __init__(self, app: Application) -> None:
        self.app = app

    @abstractmethod
    def register(self) -> None: ...
    @abstractmethod
    def boot(self) -> None: ...

    def load_routes(self, routes_file: str) -> None:
        pass

    def load_translations(self, namespace: str, path: str) -> None:
        self.app.publish(namespace, path)


def register_provider(cls: Type[BaseProvider]) -> Type[BaseProvider]:
    try:
        if not isinstance(cls, type) or not issubclass(cls, BaseProvider):
            return cls
    except Exception:
        return cls
    Application.provider_registry.append(cls)
    return cls
