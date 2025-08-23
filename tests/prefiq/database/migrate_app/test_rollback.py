import sys
import textwrap
from pathlib import Path
from types import SimpleNamespace

class _FakeEngine:
    def __init__(self, applied_rows, tables):
        self.applied_rows = applied_rows
        self.tables = tables
    def fetchone(self, sql, params):
        if "SELECT hash FROM migrations" in sql:
            app, name = params
            for r in self.applied_rows:
                if r["app"] == app and r["name"] == name:
                    return (r["hash"],)
        return None
    def fetchall(self, sql): return []
    def execute(self, sql, params=None): return None
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
    @classmethod
    def up(cls): CALLED.append("UP:{class_name}")
    @classmethod
    def down(cls): CALLED.append("DOWN:{class_name}")
"""
    path = apps_dir / filename
    path.write_text(textwrap.dedent(code), encoding="utf-8")
    return filename[:-3]

def test_rollback_last_step(tmp_path, monkeypatch):
    apps_dir = tmp_path / "apps" / "demo" / "database" / "migration"
    apps_dir.mkdir(parents=True, exist_ok=True)
    state = SimpleNamespace(applied=[], created_tables=set())

    mod_a = _write_migration(apps_dir, "mig_a.py", "A", 1, "demo", "a")
    mod_b = _write_migration(apps_dir, "mig_b.py", "B", 2, "demo", "b")

    import prefiq.database.migrations.discover as discover
    monkeypatch.setattr(discover, "load_settings", lambda: SimpleNamespace(project_root=str(tmp_path)))
    monkeypatch.setattr(discover, "get_registered_apps", lambda: ["demo"])

    fe = _FakeEngine(state.applied, state.created_tables)
    monkeypatch.setattr("prefiq.database.connection_manager.get_engine", lambda: fe, raising=False)
    monkeypatch.setattr("prefiq.database.schemas.builder.create",
                        lambda table, schema_fn: state.created_tables.add(table), raising=False)

    def _insert(table, payload):
        if table == "migrations":
            state.applied.append(dict(payload))
    def _select_all(table, columns="app, name, order_index"):
        if table != "migrations": return []
        cols = [c.strip() for c in columns.split(",")]
        return [tuple(r[c] for c in cols) for r in state.applied]
    def _delete(table, where, params):
        if table != "migrations": return
        app, name = params
        state.applied[:] = [r for r in state.applied if not (r["app"] == app and r["name"] == name)]

    monkeypatch.setattr("prefiq.database.schemas.queries.insert", _insert, raising=False)
    monkeypatch.setattr("prefiq.database.schemas.queries.select_all", _select_all, raising=False)
    monkeypatch.setattr("prefiq.database.schemas.queries.delete", _delete, raising=False)

    from prefiq.database.migrations.runner import migrate_all
    migrate_all()
    assert len(state.applied) == 2

    from prefiq.database.migrations.rollback import rollback
    rollback(step=1)

    # last migration (B) rolled back
    assert sys.modules[mod_b].CALLED[-1] == "DOWN:B"
    keys = {(r["app"], r["name"]) for r in state.applied}
    assert ("demo", "b") not in keys and ("demo", "a") in keys
