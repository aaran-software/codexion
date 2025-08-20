from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from prefiq.settings.get_settings import load_settings
from prefiq.core.contracts.base_provider import Application
from cortex.runtime.service_providers import PROVIDERS
# IMPORTANT: no DB imports here

@dataclass
class CheckResult:
    name: str
    ok: bool
    detail: str = ""

def _fmt(ok: bool) -> str:
    return "✅" if ok else "❌"

def run_boot_diagnostics(verbose: bool = False) -> Tuple[bool, List[CheckResult]]:
    results: List[CheckResult] = []

    # 1) Settings load
    try:
        settings = load_settings()
        results.append(CheckResult("Settings loaded", True, f"ENV={getattr(settings, 'ENV', 'development')}"))
    except Exception as e:
        results.append(CheckResult("Settings loaded", False, str(e)))
        return False, results

    # 2) Providers discover
    try:
        prov_names = [getattr(p, "__name__", str(p)) for p in PROVIDERS]
        results.append(CheckResult("Providers discovered", True, ", ".join(prov_names)))
    except Exception as e:
        results.append(CheckResult("Providers discovered", False, str(e)))
        return False, results

    # 3) Boot sequence (register + boot) – no DB engine resolution here
    try:
        app = Application.get_app()
        for p in PROVIDERS:
            app.register(p)
        app.boot()
        results.append(CheckResult("Application booted", True, "Lifecycle callbacks executed"))
    except Exception as e:
        results.append(CheckResult("Application booted", False, str(e)))
        return False, results

    # ALWAYS return on the success path
    overall = all(r.ok for r in results)
    return overall, results

def main(verbose: bool = False) -> int:
    overall, checks = run_boot_diagnostics(verbose=verbose)
    print("\nPrefiq Boot Doctor")
    print("------------------")
    for c in checks:
        line = f"{_fmt(c.ok)} {c.name}"
        if c.detail:
            line += f"  ·  {c.detail}"
        print(line)
    print("\nResult:", "ALL GOOD ✅" if overall else "ISSUES FOUND ❌")
    return 0 if overall else 1

if __name__ == "__main__":
    raise SystemExit(main())
