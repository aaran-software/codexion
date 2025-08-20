from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple, Optional

from prefiq.settings.get_settings import load_settings


@dataclass
class CheckResult:
    name: str
    ok: bool
    detail: str = ""


def _fmt(ok: bool) -> str:
    return "✅" if ok else "❌"


def _try_import_engine():
    """
    Import DB engine resolution lazily so merely importing the doctor doesn't
    drag DB modules (keeps 'prefiq doctor boot' clean).
    """
    try:
        # Prefer the central resolver used by your stack
        from prefiq.database.connection import get_engine  # type: ignore
        return get_engine, None
    except Exception as e:
        return None, e


def _probe_connection(engine) -> Tuple[bool, str]:
    """
    Try a very safe connectivity probe.
    Supports engines that expose:
      - test_connection()
      - execute()/fetchone()
      - .connect() context manager that yields connection with execute()
    """
    # 1) Dedicated helper (if provided by your engine)
    if hasattr(engine, "test_connection"):
        try:
            ok = bool(engine.test_connection())
            return ok, "engine.test_connection()"
        except Exception as e:
            return False, f"engine.test_connection() failed: {e}"

    # 2) Direct lightweight SELECT 1
    sql = "SELECT 1"
    # a) engine.execute returns cursor/record?
    if hasattr(engine, "execute"):
        try:
            cur = engine.execute(sql)  # type: ignore[call-arg]
            _ = getattr(cur, "fetchone", lambda: (1,))()
            return True, sql
        except Exception as e:
            return False, f"{sql} via engine.execute failed: {e}"

    # b) context-managed connection (SQLAlchemy-ish or custom)
    if hasattr(engine, "connect"):
        try:
            with engine.connect() as conn:
                cur = conn.execute(sql)  # type: ignore[attr-defined]
                _ = getattr(cur, "fetchone", lambda: (1,))()
            return True, sql
        except Exception as e:
            return False, f"{sql} via engine.connect() failed: {e}"

    # c) Fallback: best effort attribute
    if hasattr(engine, "fetchone"):
        try:
            row = engine.fetchone(sql)
            return row is not None, sql
        except Exception as e:
            return False, f"{sql} via engine.fetchone failed: {e}"

    return False, "No known execution method on engine"


def _probe_metadata(engine) -> List[CheckResult]:
    checks: List[CheckResult] = []

    # Driver info
    try:
        name = type(engine).__name__
        checks.append(CheckResult("Engine type", True, name))
    except Exception as e:
        checks.append(CheckResult("Engine type", False, str(e)))

    # Version (best-effort)
    try:
        if hasattr(engine, "server_version"):
            ver = engine.server_version  # attr
        elif hasattr(engine, "version"):
            ver = engine.version
        else:
            # attempt a DB-specific query
            ver = None
            if hasattr(engine, "execute"):
                try:
                    cur = engine.execute("SELECT sqlite_version()")  # works on sqlite
                    row = getattr(cur, "fetchone", lambda: None)()
                    if row:
                        ver = row[0]
                except Exception:
                    pass
        if ver:
            checks.append(CheckResult("Server version", True, str(ver)))
        else:
            checks.append(CheckResult("Server version", True, "unknown (skipped)"))
    except Exception as e:
        checks.append(CheckResult("Server version", False, str(e)))

    return checks


def run_database_diagnostics(verbose: bool = False) -> Tuple[bool, List[CheckResult]]:
    results: List[CheckResult] = []

    # 0) Read settings first
    try:
        settings = load_settings()
        results.append(CheckResult("Settings loaded", True,
                                   f"ENGINE={settings.DB_ENGINE} MODE={settings.DB_MODE} HOST={getattr(settings, 'DB_HOST', '')}"))
    except Exception as e:
        results.append(CheckResult("Settings loaded", False, str(e)))
        return False, results

    # 1) Ensure sync mode for now (skip cleanly for async)
    if getattr(settings, "DB_MODE", "").lower() == "async":
        results.append(CheckResult("DB mode supported", False,
                                   "Async mode not yet supported by doctor (set DB_MODE=sync to test)"))
        overall = all(r.ok for r in results)
        return overall, results

    # 2) Resolve engine (lazy import)
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

    # 3) Connectivity probe
    ok, how = _probe_connection(engine)
    results.append(CheckResult("DB connectivity", ok, how))
    if not ok:
        # stop early if we can't even connect
        overall = all(r.ok for r in results)
        return overall, results

    # 4) Metadata checks (best effort)
    results.extend(_probe_metadata(engine))

    # 5) Permissions (non-destructive)
    # Only attempt in non-production + only if engine has execute()
    try:
        env = getattr(settings, "ENV", "development")
        if env != "production" and hasattr(engine, "execute"):
            # create a temp object where safe; SQLite supports temporary tables easily
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


def main(verbose: bool = False) -> int:
    overall, checks = run_database_diagnostics(verbose=verbose)

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
