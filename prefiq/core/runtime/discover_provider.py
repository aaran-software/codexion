from __future__ import annotations
import importlib
import pkgutil
from typing import Iterable, List, Type, Dict

from prefiq.core.provider import Provider, all_providers
from prefiq.settings.get_settings import load_settings

# If your logger is available, you can uncomment these lines.
# from prefiq.log.logger import get_logger
# _log = get_logger("prefiq.discovery")


def _iter_modules(pkg: str) -> Iterable[str]:
    """Yield pkg submodules and one level of subpackages' modules."""
    try:
        p = importlib.import_module(pkg)
    except ModuleNotFoundError:
        return []
    path = getattr(p, "__path__", None) or []
    # direct children
    for _f, name, ispkg in pkgutil.iter_modules(path):
        mod = f"{pkg}.{name}"
        yield mod
        if ispkg:
            try:
                sp = importlib.import_module(mod)
                spath = getattr(sp, "__path__", None) or []
                for __f, sub, __is in pkgutil.iter_modules(spath):
                    yield f"{mod}.{sub}"
            except Exception:
                # if logging: _log.debug("skip_subpkg_error", extra={"module": mod})
                pass


def _safe_import(mod: str) -> None:
    try:
        importlib.import_module(mod)
        # if logging: _log.debug("imported", extra={"module": mod})
    except Exception:
        # if logging: _log.warning("import_failed", extra={"module": mod, "error": str(e)})
        pass


def _settings_lists():
    s = load_settings()
    apps  = list(getattr(s, "REGISTERED_APPS", []) or [])
    roots = list(getattr(s, "PROVIDER_DISCOVERY_ROOTS", []) or [])
    include = set(getattr(s, "PROVIDERS_INCLUDE", []) or [])
    exclude = set(getattr(s, "PROVIDERS_EXCLUDE", []) or [])
    ordermap: Dict[str, int] = dict(getattr(s, "PROVIDERS_ORDER", {}) or {})
    return apps, roots, include, exclude, ordermap


def discover_providers() -> List[Type[Provider]]:
    """
    Config-driven discovery:
      1) Import <app>.providers.* for each app in REGISTERED_APPS
      2) Import modules under each root in PROVIDER_DISCOVERY_ROOTS
      3) Force-include / exclude / order overrides from settings
    """
    apps, roots, include, exclude, ordermap = _settings_lists()

    # 1) scan each app's providers/
    for app in apps:
        for mod in _iter_modules(f"{app}.providers"):
            _safe_import(mod)

    # 2) scan extra roots (built-ins, etc.)
    for root in roots:
        for mod in _iter_modules(root):
            _safe_import(mod)

    # 3) force include: import modules so metaclass can register classes
    for fq in include:
        try:
            mod, _cls = fq.rsplit(".", 1)
            _safe_import(mod)
        except Exception:
            pass

    # Collect current providers
    current = {f"{c.__module__}.{c.__name__}": c for c in all_providers()}

    # Apply order overrides
    for fq, k in ordermap.items():
        if fq in current:
            setattr(current[fq], "order", int(k))

    # Exclude
    result = [cls for fq, cls in current.items() if fq not in exclude]

    # Final sort
    result.sort(key=lambda c: getattr(c, "order", 100))
    return result
