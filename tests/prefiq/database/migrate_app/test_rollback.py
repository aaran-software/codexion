# tests/prefiq/database/migrate_app/test_rollback.py

from __future__ import annotations

import sys
import textwrap
from pathlib import Path
from types import SimpleNamespace


class _FakeEngine:
    """
    Minimal engine stub. Real SQL isn't executed because we monkeypatch the
    queries module to operate purely on in-memory state.
    """
    def __init__(self, applied_rows, tables):
        self.applied_rows = applied_rows
        self.tables = tables

    # Keep signatures flexible; some code may call with (sql) or (sql, params)
    def fetchone(self, sql, params=None):
        if params is None:
            params = ()
        if "SELECT hash FROM migrations" in sql:
            app, name = params
            for r in self.applied_rows:
                if r["app"] == app and r["name"] == name:
                    return (r.get("hash", ""),)
        return None

    def fetchall(self, sql, *args):
        return []

    def execute(self, sql, params=None):
        return None

    def begin(self): ...
    def commit(self): ...
    def rollback(self): ...


def _write_migration(apps_dir: Path, filename: str, class_name: str,
                     order_index: int, app_name: str, table_name: str) -> str:
    """
    Writes a tiny Migration class with UP/DOWN tracking to a temp apps tree.
    Returns the module name so we can inspect CALLED later.
    """
    code = f"""
from prefiq.database.migrations.base import Migrations
CALLED = []
class {class_name}(Migrations):
    APP_NAME = {app_name!r}
    TABLE_NAME = {table_name!r}
    ORDER_INDEX = {order_index}
    @classmethod
    def up(cls): CALLED.append("UP:{class_name}")
    @classmethod
    def down(cls): CALLED.append("DOWN:{class_name}")
"""
    path = apps_dir / filename
    path.write_text(textwrap.dedent(code), encoding="utf-8")
    # Return the module name string so callers can look up sys.modules[name]
    return filename[:-3]


def test_rollback_last_step(tmp_path, monkeypatch):
    """
    Create two migrations A(1) and B(2).
    - Run migrate_all() -> both apply
    - Run rollback(step=1) -> only B rolls back (DOWN:B)
    - Migrations table retains only A
    """
    apps_dir = tmp_path / "apps" / "demo" / "database" / "migration"
    apps_dir.mkdir(parents=True, exist_ok=True)

    state = SimpleNamespace(applied=[], created_tables=set())

    mod_a = _write_migration(apps_dir, "mig_a.py", "A", 1, "demo", "a")
    mod_b = _write_migration(apps_dir, "mig_b.py", "B", 2, "demo", "b")

    # Patch discovery roots to the temp "apps" dir
    import prefiq.database.migrations.discover as discover
    monkeypatch.setattr(discover, "load_settings",
                        lambda: SimpleNamespace(project_root=str(tmp_path)))
    monkeypatch.setattr(discover, "get_registered_apps", lambda: ["demo"])

    # Engine and builder.create (ensure_migrations_table)
    fe = _FakeEngine(state.applied, state.created_tables)
    monkeypatch.setattr("prefiq.database.connection_manager.get_engine", lambda: fe, raising=False)
    monkeypatch.setattr("prefiq.database.schemas.builder.create",
                        lambda table, schema_fn: state.created_tables.add(table), raising=False)

    # In-memory queries shims (only for 'migrations' table)
    def _insert(table, payload):
        if table == "migrations":
            state.applied.append(dict(payload))

    def _select_all(table, columns="app, name, order_index"):
        if table != "migrations":
            return []
        cols = [c.strip() for c in columns.split(",")]
        return [tuple(r[c] for c in cols) for r in state.applied]

    def _delete(table, where, params):
        if table != "migrations":
            return
        app, name = params
        state.applied[:] = [r for r in state.applied if not (r["app"] == app and r["name"] == name)]

    monkeypatch.setattr("prefiq.database.schemas.queries.insert", _insert, raising=False)
    monkeypatch.setattr("prefiq.database.schemas.queries.select_all", _select_all, raising=False)
    monkeypatch.setattr("prefiq.database.schemas.queries.delete", _delete, raising=False)

    # Run migrations
    from prefiq.database.migrations.runner import migrate_all
    migrate_all()
    assert len(state.applied) == 2

    # Roll back the last step (B)
    from prefiq.database.migrations.rollback import rollback
    rollback(step=1)

    # Validate DOWN:B and record removal
    assert sys.modules[mod_b].CALLED[-1] == "DOWN:B"
    keys = {(r["app"], r["name"]) for r in state.applied}
    assert ("demo", "b") not in keys and ("demo", "a") in keys


def test_rollback_two_steps(tmp_path, monkeypatch):
    """
    Create three migrations A(1), B(2), C(3).
    - Run migrate_all() -> A,B,C apply
    - Run rollback(step=2) -> C then B roll back
    - Only A remains in migrations table; order of DOWN calls respected.
    """
    apps_dir = tmp_path / "apps" / "demo" / "database" / "migration"
    apps_dir.mkdir(parents=True, exist_ok=True)

    state = SimpleNamespace(applied=[], created_tables=set())

    mod_a = _write_migration(apps_dir, "mig_a.py", "A", 1, "demo", "a")
    mod_b = _write_migration(apps_dir, "mig_b.py", "B", 2, "demo", "b")
    mod_c = _write_migration(apps_dir, "mig_c.py", "C", 3, "demo", "c")

    import prefiq.database.migrations.discover as discover
    monkeypatch.setattr(discover, "load_settings",
                        lambda: SimpleNamespace(project_root=str(tmp_path)))
    monkeypatch.setattr(discover, "get_registered_apps", lambda: ["demo"])

    fe = _FakeEngine(state.applied, state.created_tables)
    monkeypatch.setattr("prefiq.database.connection_manager.get_engine", lambda: fe, raising=False)
    monkeypatch.setattr("prefiq.database.schemas.builder.create",
                        lambda table, schema_fn: state.created_tables.add(table), raising=False)

    def _insert(table, payload):
        if table == "migrations":
            state.applied.append(dict(payload))

    def _select_all(table, columns="app, name, order_index"):
        if table != "migrations":
            return []
        cols = [c.strip() for c in columns.split(",")]
        return [tuple(r[c] for c in cols) for r in state.applied]

    def _delete(table, where, params):
        if table != "migrations":
            return
        app, name = params
        state.applied[:] = [r for r in state.applied if not (r["app"] == app and r["name"] == name)]

    monkeypatch.setattr("prefiq.database.schemas.queries.insert", _insert, raising=False)
    monkeypatch.setattr("prefiq.database.schemas.queries.select_all", _select_all, raising=False)
    monkeypatch.setattr("prefiq.database.schemas.queries.delete", _delete, raising=False)

    from prefiq.database.migrations.runner import migrate_all
    migrate_all()
    assert len(state.applied) == 3

    from prefiq.database.migrations.rollback import rollback
    rollback(step=2)

    # Validate DOWN order: C then B
    assert sys.modules[mod_c].CALLED[-1] == "DOWN:C"
    assert sys.modules[mod_b].CALLED[-1] == "DOWN:B"

    # Only A remains
    keys = {(r["app"], r["name"]) for r in state.applied}
    assert keys == {("demo", "a")}
