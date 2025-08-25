# prefiq/core/discovery.py
from __future__ import annotations

import importlib
import pkgutil
from typing import Dict, Iterable, List, Type

from prefiq.core.provider import Provider, all_providers
from prefiq.settings.get_settings import load_settings
from prefiq.apps.app_cfg import get_registered_apps  # ← NEW


def _iter_modules(pkg: str) -> Iterable[str]:
    """
    Yield immediate submodules and one level of subpackages' modules for 'pkg'.
    Safe to call even if the package does not exist.
    """
    try:
        p = importlib.import_module(pkg)
    except ModuleNotFoundError:
        return []
    path = getattr(p, "__path__", None) or []
    # direct children
    for _f, name, is_pkg in pkgutil.iter_modules(path):
        mod = f"{pkg}.{name}"
        yield mod
        if is_pkg:
            # one extra level in subpackages
            try:
                sp = importlib.import_module(mod)
                spath = getattr(sp, "__path__", None) or []
                for __f, sub, __is in pkgutil.iter_modules(spath):
                    yield f"{mod}.{sub}"
            except (ValueError, TypeError):
                # ignore subpackage scan errors
                pass


def _safe_import(module_name: str) -> None:
    try:
        importlib.import_module(module_name)
    except (ValueError, TypeError):
        # Swallow import failures — a missing providers package shouldn't kill discovery.
        pass


def _settings() -> tuple[list[str], list[str], set[str], set[str], Dict[str, int]]:
    """
    Merge discovery inputs from environment (.env) **and** config/apps.cfg.
    - apps: env REGISTERED_APPS + cfg apps (prefixed with 'apps.')
    - roots: env roots; if cfg has apps and 'apps' not present, add it
    """
    s = load_settings()
    apps_env = list(getattr(s, "REGISTERED_APPS", []) or [])
    roots = list(getattr(s, "PROVIDER_DISCOVERY_ROOTS", []) or [])
    include = set(getattr(s, "PROVIDERS_INCLUDE", []) or [])
    exclude = set(getattr(s, "PROVIDERS_EXCLUDE", []) or [])
    order = dict(getattr(s, "PROVIDERS_ORDER", {}) or {})

    # Load app names from config/apps.cfg and map to "apps.<name>"
    try:
        cfg_apps = get_registered_apps()  # preserves file order
    except (ValueError, TypeError):
        cfg_apps = []

    apps_cfg = [f"apps.{name}" for name in cfg_apps]

    # Merge (preserve first occurrence)
    merged_apps: list[str] = []
    for a in apps_env + apps_cfg:
        if a not in merged_apps:
            merged_apps.append(a)

    # If cfg lists apps but no explicit root, also scan the "apps" package
    if cfg_apps and "apps" not in roots:
        roots.append("apps")

    return merged_apps, roots, include, exclude, order


def discover_providers() -> List[Type[Provider]]:
    """
    Hybrid discovery (config‑driven):
      1) Import <app>.providers.* for each app in REGISTERED_APPS (+ apps.cfg)
      2) Import modules under each root in PROVIDER_DISCOVERY_ROOTS
      3) Apply INCLUDE/EXCLUDE/ORDER overrides from settings
      4) Return sorted Provider classes
    """
    apps, roots, include, exclude, ordermap = _settings()

    # 1) scan each app's providers/ package
    for app in apps:
        for mod in _iter_modules(f"{app}.providers"):
            _safe_import(mod)

    # 2) scan extra discovery roots
    for root in roots:
        for mod in _iter_modules(root):
            _safe_import(mod)

    # 3a) force‑include: import module so its Provider subclass registers via metaclass
    for fq in include:
        try:
            mod, _cls = fq.rsplit(".", 1)
            _safe_import(mod)
        except (ValueError, TypeError):
            pass

    # 3b) collect the currently known providers
    current = {f"{c.__module__}.{c.__name__}": c for c in all_providers()}

    # 3c) order overrides
    for fq, k in ordermap.items():
        if fq in current:
            setattr(current[fq], "order", int(k))

    # 3d) exclude
    result = [cls for fq, cls in current.items() if fq not in exclude]

    # 4) final sort (tolerate non‑ints/None)
    def _order_of(cls) -> int:
        v = getattr(cls, "order", 100)
        return v if isinstance(v, int) else 100

    result.sort(key=_order_of)
    return result
