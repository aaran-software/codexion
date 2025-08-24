# prefiq/core/provider.py
from __future__ import annotations

from abc import ABC, ABCMeta, abstractmethod
from typing import ClassVar, Dict, List, Set, Type

__all__ = ["Provider", "all_providers", "clear_provider_registry"]

# In‑memory registry populated at import time
_PROVIDER_REGISTRY: Dict[str, Type["Provider"]] = {}


class _ProviderMeta(ABCMeta):
    def __new__(mcls, name, bases, ns, **kw):
        cls = super().__new__(mcls, name, bases, ns, **kw)
        # Register any concrete subclass (direct or indirect), skip the base itself
        if name != "Provider":
            is_abstract = getattr(cls, "abstract", False)
            is_enabled  = getattr(cls, "enabled", True)
            if not is_abstract and is_enabled:
                _PROVIDER_REGISTRY[f"{cls.__module__}.{cls.__name__}"] = cls
        return cls


class Provider(ABC, metaclass=_ProviderMeta):
    """
    App/service provider base.
    Importing the module where your subclass lives is enough to get it registered.
    """
    # Flags / metadata
    abstract: ClassVar[bool] = True       # subclasses default to concrete unless they set True
    enabled:  ClassVar[bool] = True
    order:    ClassVar[int]  = 100        # lower = earlier

    # Optional diagnostics / future topo sort
    provides:   ClassVar[Set[str]] = set()
    depends_on: ClassVar[Set[str]] = set()

    def __init_subclass__(cls, **kw):
        # If subclass doesn't declare 'abstract', treat it as concrete by default
        if "abstract" not in cls.__dict__:
            cls.abstract = False

    # NOTE: Signature matches Application.register() which instantiates the class
    # and then calls .register()/.boot() with no args.
    @abstractmethod
    def register(self) -> None:
        """Bind services into the container (e.g., app.bind(...))."""

    def boot(self) -> None:
        """Optional post‑bind startup (routes, events, warmups)."""


def all_providers() -> List[Type["Provider"]]:
    """Return all registered provider classes sorted by .order (ascending)."""
    items = list(_PROVIDER_REGISTRY.values())
    items.sort(key=lambda c: getattr(c, "order", 100))
    return items


def clear_provider_registry() -> None:
    """Testing helper: empty the global provider registry."""
    _PROVIDER_REGISTRY.clear()
