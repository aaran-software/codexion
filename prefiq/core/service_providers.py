# prefiq/core/service_providers.py
from __future__ import annotations
from typing import List, Type, Iterable, Set

from prefiq.core.provider import Provider
from prefiq.core.discovery import discover_providers

# ---- Hardcoded core providers (optional if modules present) ----
try:
    from prefiq.providers.config_provider import ConfigProvider  # type: ignore
except (ValueError, TypeError):
    ConfigProvider = None  # type: ignore[misc]

try:
    from prefiq.providers.database_provider import DatabaseProvider  # type: ignore
except (ValueError, TypeError):
    DatabaseProvider = None  # type: ignore[misc]

try:
    from prefiq.providers.migration_provider import MigrationProvider  # type: ignore
except (ValueError, TypeError):
    MigrationProvider = None  # type: ignore[misc]

try:
    from cortex.providers.CortexProvider import CortexProvider  # type: ignore
except Exception:
    CortexProvider = None  # type: ignore[misc]


def _hardcoded_providers() -> List[Type[Provider]]:
    core: List[Type[Provider]] = []
    for cls in (ConfigProvider, DatabaseProvider, MigrationProvider):
        if cls is not None:
            core.append(cls)  # type: ignore[arg-type]
    return core


def _uniq_in_order(classes: Iterable[Type[Provider]]) -> List[Type[Provider]]:
    seen: Set[str] = set()
    out: List[Type[Provider]] = []
    for cls in classes:
        key = f"{cls.__module__}.{cls.__name__}"
        if key in seen:
            continue
        seen.add(key)
        out.append(cls)
    return out


def get_service_providers() -> List[Type[Provider]]:
    """
    1) Hardcoded core (config → database → migration)
    2) Discovered (apps, roots)
    3) Stable de-dupe (hardcoded precedence)
    """
    hardcoded = _hardcoded_providers()
    discovered = list(discover_providers())
    return _uniq_in_order([*hardcoded, *discovered])
