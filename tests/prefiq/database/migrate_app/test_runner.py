# tests/prefiq/migrations/test_runner_apply.py
import sys
import textwrap
from pathlib import Path
from types import SimpleNamespace


# ---------------------------
# local helpers (no conftest)
# ---------------------------
class _FakeEngine:
    def __init__(self, applied_rows, tables):
        self.applied_rows = applied_rows   # list[dict]
        self.tables = tables               # set[str]

    def fetchone(self, sql, params):
        # not used by current runner, kept for compatibility
        if "SELECT hash FROM migrations" in sql:
            app, name = params
            for r in self.applied_rows:
                if r["app"] == app and r["name"] == name:
                    return (r["hash"],)
        return None

    def fetchall(self, sql):  # not used here
        return []

    def execute(self, sql, params=None):  # builder.create & inserts call through patched fns
        return None

    def begin(self): pass
    def commit(self): pass
    def rollback(self): pass


def _write_migration(apps_dir: Path, filename: str, class_name: str, order_index: int,
                     app_name: str, table_name: str) -> str:
    code = f"""
from prefiq.database.migrations.base import Migrations
CALLED = []
class {class_name}(Migrations):
    APP_NAME = {app_name!r}
    TABLE_NAME = {table_name!r}
    ORDER_INDEX = {order_index}
    def up(self): CALLED.append("UP:{class_name}")
    def down(self): CALLED.append("DOWN:{class_name}")
"""
    path = apps_dir / filename
    path.write_text(textwrap.dedent(code), encoding="utf-8")
    return filename[:-3]


def test_migrate_runs_in_order_and_records(tmp_path, monkeypatch):
    # sandbox
    apps_dir = tmp_path / "apps" / "demo" / "database" / "migration"
    apps_dir.mkdir(parents=True, exist_ok=True)
    state = SimpleNamespace(applied=[], created_tables=set())

    mod_b = _write_migration(apps_dir, "mig_b.py", "B", 2, "demo", "b")
    mod_a = _write_migration(apps_dir, "mig_a.py", "A", 1, "demo", "a")

    # patch discover roots
    import prefiq.database.migrations.discover as discover
    monkeypatch.setattr(discover, "load_settings", lambda: SimpleNamespace(project_root=str(tmp_path)))
    monkeypatch.setattr(discover, "get_registered_apps", lambda: ["demo"])

    # patch engine
    fake_engine = _FakeEngine(state.applied, state.created_tables)
    monkeypatch.setattr("prefiq.database.connection_manager.get_engine", lambda: fake_engine, raising=False)

    # patch schema/queries to pure in-memory
    # ensure_migrations_table() calls create("migrations", ...)
    monkeypatch.setattr("prefiq.database.schemas.builder.create",
                        lambda table, schema_fn: state.created_tables.add(table), raising=False)

    def _insert(table, payload):
        if table == "migrations":
            state.applied.append(dict(payload))

    def _select_all(table, columns="app, name, hash"):
        if table != "migrations":
            return []
        cols = [c.strip() for c in columns.split(",")]
        out = []
        for row in state.applied:
            out.append(tuple(row[c] for c in cols))
        return out

    monkeypatch.setattr("prefiq.database.schemas.queries.insert", _insert, raising=False)
    monkeypatch.setattr("prefiq.database.schemas.queries.select_all", _select_all, raising=False)

    from prefiq.database.migrations.runner import migrate_all
    migrate_all()

    # ensured table
    assert "migrations" in state.created_tables

    # ran in order (A then B)
    assert sys.modules[mod_a].CALLED == ["UP:A"]
    assert sys.modules[mod_b].CALLED == ["UP:B"]

    # recorded rows
    by_key = {(r["app"], r["name"]): r for r in state.applied}
    assert ("demo", "a") in by_key and ("demo", "b") in by_key
    assert by_key[("demo", "a")]["order_index"] == 1
    assert by_key[("demo", "b")]["order_index"] == 2
    assert by_key[("demo", "a")]["hash"] and by_key[("demo", "b")]["hash"]


def test_migrate_is_idempotent(tmp_path, monkeypatch):
    apps_dir = tmp_path / "apps" / "demo" / "database" / "migration"
    apps_dir.mkdir(parents=True, exist_ok=True)
    state = SimpleNamespace(applied=[], created_tables=set())

    mod_a = _write_migration(apps_dir, "mig_a.py", "A", 1, "demo", "a")

    import prefiq.database.migrations.discover as discover
    monkeypatch.setattr(discover, "load_settings", lambda: SimpleNamespace(project_root=str(tmp_path)))
    monkeypatch.setattr(discover, "get_registered_apps", lambda: ["demo"])

    fake_engine = _FakeEngine(state.applied, state.created_tables)
    monkeypatch.setattr("prefiq.database.connection_manager.get_engine", lambda: fake_engine, raising=False)

    monkeypatch.setattr("prefiq.database.schemas.builder.create",
                        lambda table, schema_fn: state.created_tables.add(table), raising=False)

    def _insert(table, payload):
        if table == "migrations":
            state.applied.append(dict(payload))

    def _select_all(table, columns="app, name, hash"):
        if table != "migrations":
            return []
        cols = [c.strip() for c in columns.split(",")]
        return [tuple(row[c] for c in cols) for row in state.applied]

    monkeypatch.setattr("prefiq.database.schemas.queries.insert", _insert, raising=False)
    monkeypatch.setattr("prefiq.database.schemas.queries.select_all", _select_all, raising=False)

    from prefiq.database.migrations.runner import migrate_all
    migrate_all()
    first = len(state.applied)
    # run again — should skip based on hash equality
    migrate_all()
    assert len(state.applied) == first
