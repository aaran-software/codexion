# prefiq/cli/checkup/migration_doctor.py
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from prefiq.core.contracts.base_provider import Application
from cortex.runtime.service_providers import PROVIDERS
from prefiq.log.logger import get_logger

log = get_logger("prefiq.doctor.migrate")

@dataclass
class CheckResult:
    name: str
    ok: bool
    detail: str = ""

def _fmt(ok: bool) -> str:
    return "✅" if ok else "❌"

def run_migration_diagnostics(verbose: bool = False) -> Tuple[bool, List[CheckResult]]:
    results: List[CheckResult] = []
    try:
        app = Application.get_app()
        for p in PROVIDERS:
            app.register(p)
        app.boot()
        results.append(CheckResult("Application booted", True, "Providers registered & booted"))
    except Exception as e:
        results.append(CheckResult("Application booted", False, str(e)))
        return False, results

    try:
        migrator = app.resolve("migrator")
        assert migrator is not None, "migrator not bound"
        # smoke: ensure migrations table is creatable at boot (MigrationProvider already tries this)
        results.append(CheckResult("Migrator bound", True, "Service key 'migrator' is available"))
    except Exception as e:
        results.append(CheckResult("Migrator bound", False, str(e)))
        return False, results

    overall = all(r.ok for r in results)
    return overall, results

def main(verbose: bool = False) -> int:
    ok, checks = run_migration_diagnostics(verbose=verbose)
    print("\nPrefiq Migration Doctor")
    print("-----------------------")
    for c in checks:
        line = f"{_fmt(c.ok)} {c.name}"
        if c.detail:
            line += f"  ·  {c.detail}"
        print(line)
    print("\nResult:", "ALL GOOD ✅" if ok else "ISSUES FOUND ❌")
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
