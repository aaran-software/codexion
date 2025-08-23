from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple, Optional

from prefiq.settings.get_settings import load_settings
from cortex.runtime.service_providers import PROVIDERS


@dataclass
class CheckResult:
    name: str
    ok: bool
    detail: str = ""


def _fmt(ok: bool) -> str:
    return "✅" if ok else "❌"


def _db_provider_configured() -> tuple[bool, str]:
    """
    Detect whether a DatabaseProvider-like class is present in PROVIDERS,
    without importing the provider module directly.
    """
    seen = []
    for p in PROVIDERS:
        name = getattr(p, "__name__", "")
        module = getattr(p, "__module__", "")
        qual = f"{module}.{name}" if module and name else name or module
        seen.append(name or qual)
        # accept common names/modules without importing heavy deps
        if name == "DatabaseProvider" or "database_provider" in module:
            return True, qual or name
    return False, ", ".join(seen) if seen else "none"


def _try_import_engine():
    # Import lazily only if provider is configured
    try:
        from prefiq.database.connection import get_engine  # type: ignore
        return get_engine, None
    except Exception as e:
        return None, e


def _probe_connection(engine) -> tuple[bool, str]:
    if hasattr(engine, "test_connection"):
        try:
            return bool(engine.test_connection()), "engine.test_connection()"
        except Exception as e:
            return False, f"engine.test_connection() failed: {e}"

    sql = "SELECT 1"
    if hasattr(engine, "execute"):
        try:
            cur = engine.execute(sql)  # type: ignore[call-arg]
            _ = getattr(cur, "fetchone", lambda: (1,))()
            return True, sql
        except Exception as e:
            return False, f"{sql} via engine.execute failed: {e}"

    if hasattr(engine, "connect"):
        try:
            with engine.connect() as conn:
                cur = conn.execute(sql)  # type: ignore[attr-defined]
                _ = getattr(cur, "fetchone", lambda: (1,))()
            return True, sql
        except Exception as e:
            return False, f"{sql} via engine.connect() failed: {e}"

    if hasattr(engine, "fetchone"):
        try:
            row = engine.fetchone(sql)
            return row is not None, sql
        except Exception as e:
            return False, f"{sql} via engine.fetchone failed: {e}"

    return False, "No known execution method on engine"


def _probe_metadata(engine) -> List[CheckResult]:
    checks: List[CheckResult] = []
    try:
        checks.append(CheckResult("Engine type", True, type(engine).__name__))
    except Exception as e:
        checks.append(CheckResult("Engine type", False, str(e)))

    try:
        ver = None
        if hasattr(engine, "server_version"):
            ver = engine.server_version
        elif hasattr(engine, "version"):
            ver = engine.version
        elif hasattr(engine, "execute"):
            try:
                cur = engine.execute("SELECT sqlite_version()")
                row = getattr(cur, "fetchone", lambda: None)()
                if row:
                    ver = row[0]
            except Exception:
                pass
        checks.append(CheckResult("Server version", True, str(ver) if ver else "unknown (skipped)"))
    except Exception as e:
        checks.append(CheckResult("Server version", False, str(e)))

    return checks


def run_database_diagnostics(*, verbose: bool = False, strict: bool = False) -> tuple[bool, List[CheckResult]]:
    results: List[CheckResult] = []

    # 0) Settings
    try:
        settings = load_settings()
        results.append(CheckResult("Settings loaded", True,
                                   f"ENGINE={settings.DB_ENGINE} MODE={settings.DB_MODE} HOST={getattr(settings, 'DB_HOST', '')}"))
    except Exception as e:
        results.append(CheckResult("Settings loaded", False, str(e)))
        return False, results

    # 1) Is DatabaseProvider configured?
    has_db_provider, prov_detail = _db_provider_configured()
    if not has_db_provider:
        results.append(CheckResult("Database provider configured", False,
                                   f"Not found in PROVIDERS (seen: {prov_detail})."))
        results.append(CheckResult("Database checks", True, "skipped (no provider)"))
        # In non-strict mode, missing provider is informative, not fatal.
        return (False if strict else True), results
    else:
        results.append(CheckResult("Database provider configured", True, prov_detail))

    # 2) (Optional) Sync mode guard — skip async for now
    if getattr(settings, "DB_MODE", "").lower() == "async":
        results.append(CheckResult("DB mode supported", False,
                                   "Async mode not yet supported by doctor (set DB_MODE=sync to test)"))
        overall = all(r.ok for r in results)
        return overall, results

    # 3) Resolve engine (lazy import)
    get_engine, import_err = _try_import_engine()
    if import_err or get_engine is None:
        results.append(CheckResult("Engine resolver import", False, f"{import_err}"))
        return False, results

    try:
        engine = get_engine()
        results.append(CheckResult("Engine resolved", True, type(engine).__name__))
    except Exception as e:
        results.append(CheckResult("Engine resolved", False, str(e)))
        return False, results

    # 4) Connectivity
    ok, how = _probe_connection(engine)
    results.append(CheckResult("DB connectivity", ok, how))
    if not ok:
        overall = all(r.ok for r in results)
        return overall, results

    # 5) Metadata + non-destructive perms
    results.extend(_probe_metadata(engine))
    try:
        env = getattr(settings, "ENV", "development")
        if env != "production" and hasattr(engine, "execute"):
            try:
                engine.execute("CREATE TEMP TABLE __prefiq_probe__(id INTEGER)")
                engine.execute("DROP TABLE __prefiq_probe__")
                results.append(CheckResult("DDL permission (temp)", True, "CREATE TEMP TABLE"))
            except Exception as e:
                results.append(CheckResult("DDL permission (temp)", False, str(e)))
        else:
            results.append(CheckResult("DDL permission (temp)", True, "skipped"))
    except Exception as e:
        results.append(CheckResult("DDL permission (temp)", False, str(e)))

    overall = all(r.ok for r in results)
    return overall, results


def main(verbose: bool = False, strict: bool = False) -> int:
    overall, checks = run_database_diagnostics(verbose=verbose, strict=strict)

    print("\nPrefiq Database Doctor")
    print("----------------------")
    for c in checks:
        line = f"{_fmt(c.ok)} {c.name}"
        if c.detail:
            line += f"  ·  {c.detail}"
        print(line)
    print("\nResult:", "ALL GOOD ✅" if overall else "ISSUES FOUND ❌")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
