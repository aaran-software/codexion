from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import ClassVar, Dict, List, Set, Type

# Internal registry: filled automatically when Provider subclasses are imported
_PROVIDER_REGISTRY: Dict[str, Type["Provider"]] = {}


class _ProviderMeta(type):
    """
    Auto-register concrete Provider subclasses at import time.
    A class is 'concrete' when:
      - it's a subclass of Provider (but not Provider itself)
      - abstract == False
      - enabled == True
    """
    def __new__(mcls, name, bases, ns, **kw):
        cls = super().__new__(mcls, name, bases, ns, **kw)
        if any(b.__name__ == "Provider" for b in bases):
            is_abstract = ns.get("abstract", False)
            is_enabled = ns.get("enabled", True)
            if not is_abstract and is_enabled:
                fqname = f"{cls.__module__}.{cls.__name__}"
                _PROVIDER_REGISTRY[fqname] = cls
        return cls


class Provider(ABC, metaclass=_ProviderMeta):
    """
    Extend this in any <app>.providers.* module.
    Importing the module registers the class automatically.
    """
    # Class flags / metadata
    abstract: ClassVar[bool] = True        # subclasses become concrete by default
    enabled:  ClassVar[bool] = True
    order:    ClassVar[int]  = 100         # lower runs earlier (Laravel feel)

    # Optional diagnostics / future topo sort
    provides:   ClassVar[Set[str]] = set()
    depends_on: ClassVar[Set[str]] = set()

    def __init_subclass__(cls, **kw):
        # If subclass doesn't set 'abstract', treat it as concrete
        if "abstract" not in cls.__dict__:
            cls.abstract = False

    @abstractmethod
    def register(self, app) -> None:
        """Bind services into the container (app.bind/app.singleton/etc.)."""

    def boot(self, app) -> None:
        """Optional: post-bind startup (routes, events, migrations, warmups)."""


def all_providers() -> List[Type["Provider"]]:
    """Return all registered provider classes, sorted by .order."""
    items = list(_PROVIDER_REGISTRY.values())
    items.sort(key=lambda c: getattr(c, "order", 100))
    return items
