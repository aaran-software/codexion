import sys
from pathlib import Path
from types import SimpleNamespace
import textwrap

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

def test_discover_sorts_by_order_index(tmp_path, monkeypatch):
    # sandbox layout: <tmp>/apps/demo/database/migration/*.py
    apps_dir = tmp_path / "apps" / "demo" / "database" / "migration"
    apps_dir.mkdir(parents=True, exist_ok=True)

    mod_b = _write_migration(apps_dir, "mig_b.py", "B", 2, "demo", "b")
    mod_a = _write_migration(apps_dir, "mig_a.py", "A", 1, "demo", "a")

    # patch discover to look into sandbox
    import prefiq.database.migrations.discover as discover
    monkeypatch.setattr(discover, "load_settings", lambda: SimpleNamespace(project_root=str(tmp_path)))
    monkeypatch.setattr(discover, "get_registered_apps", lambda: ["demo"])

    from prefiq.database.migrations.discover import discover_all
    classes = discover_all()

    assert [c.__name__ for c in classes] == ["A", "B"]
    assert mod_a in sys.modules and mod_b in sys.modules
