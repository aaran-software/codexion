import os
import configparser
from cortex.config.apps.apps_cfg import (
    create_apps_cfg,
    # delete_apps_cfg,
    get_registered_apps,
    add_app,
    remove_app,
    update_app_version,
)
from cortex.config.apps.make_migration import create_migration_file
from cortex.config.apps.migration_order_json import ensure_all_apps_have_migration_order, read_migration_order
from cortex.core.settings import get_settings
from pathlib import Path

settings = get_settings()
CFG_PATH = Path(settings.project_root) / "config" / "apps.cfg"


def test_add_app():
    add_app("cxsun", "1.0.0")
    add_app("blog", "1.0.0")
    add_app("crm", "1.0.0")
    add_app("ecart", "1.0.0")
    add_app("erp", "1.0.0")
    add_app("mazsone", "1.0.0")
    apps = get_registered_apps()
    assert "cxsun" in apps
    assert "blog" in apps
    assert "crm" in apps
    assert "ecart" in apps
    assert "erp" in apps
    assert "mazsone" in apps
    print("✅ Apps added to apps.cfg")


def test_add_migration_json():
    ensure_all_apps_have_migration_order()
    project_root = Path(get_settings().project_root)
    apps = get_registered_apps()
    for app in apps:
        json_path = project_root / "apps" / app / "database" / "migration_order.json"
        assert json_path.exists(), f"{app}: migration_order.json not found"


def test_add_migration_schema():
    app = "cxsun"
    table = "dashboard"
    filename = create_migration_file(app, table)

    app = "blog"
    table = "blog_category"
    filename = create_migration_file(app, table)

    app = "blog"
    table = "blog_tag"
    filename = create_migration_file(app, table)

    app = "blog"
    table = "blog_post"
    filename = create_migration_file(app, table)

    app = "blog"
    table = "blog_like"
    filename = create_migration_file(app, table)

    app = "blog"
    table = "blog_comments"
    filename = create_migration_file(app, table)

    app = "blog"
    table = "blog_reply"
    filename = create_migration_file(app, table)

    app = "blog"
    table = "blog_media"
    filename = create_migration_file(app, table)

    project_root = Path(get_settings().project_root)
    path = project_root / "apps" / app / "database" / "migrations" / filename

    print(f"🧪 File created at: {path}")

    assert path.exists(), "❌ Migration file not created"

    order = read_migration_order(app)
    assert filename in order, f"❌ Migration '{filename}' not added to order"
