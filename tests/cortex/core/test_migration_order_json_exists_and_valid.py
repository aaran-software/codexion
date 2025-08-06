# import json
# from pathlib import Path
# from cortex.config.apps.apps_cfg import (
#     create_apps_cfg,
#     delete_apps_cfg,
#     add_app,
#     remove_app,
#     get_registered_apps
# )
# from cortex.core.settings import get_settings
# from cortex.config.apps.migration_order_json import (
#     ensure_migration_folder_and_json,
#     ensure_all_apps_have_migration_order,
#     read_migration_order,
#     add_migration,
#     remove_migration,
#     update_migration_at,
#     delete_migration_json
# )
#
#
# def test_apps_cfg_lifecycle():
#     create_apps_cfg()
#     add_app("crm", "1.0.0")
#     add_app("inventory", "2.0.1")
#     apps = get_registered_apps()
#     assert "crm" in apps
#     assert "inventory" in apps
#
#     remove_app("inventory")
#     apps = get_registered_apps()
#     assert "inventory" not in apps
#
#     delete_apps_cfg()
#
#
# def test_ensure_all_apps_have_migration_json():
#     create_apps_cfg()
#     add_app("crm", "1.0.0")
#     add_app("cxsun", "1.2.3")
#
#     ensure_all_apps_have_migration_order()
#
#     project_root = Path(get_settings().project_root)
#     for app in ["crm", "cxsun"]:
#         json_path = project_root / "apps" / app / "database" / "migration_order.json"
#         assert json_path.exists(), f"{app}: migration_order.json not found"
#
#     delete_apps_cfg()
#
#
# def test_add_and_read_migrations():
#     app = "crm"
#     ensure_migration_folder_and_json(app, overwrite=True)
#     add_migration(app, "001_users.py")
#     add_migration(app, "002_roles.py")
#     order = read_migration_order(app)
#     assert "001_users.py" in order
#     assert "002_roles.py" in order
#
#
# def test_remove_migration():
#     app = "crm"
#     ensure_migration_folder_and_json(app, overwrite=True)
#     add_migration(app, "001_users.py")
#     add_migration(app, "002_roles.py")
#     remove_migration(app, "001_users.py")
#     order = read_migration_order(app)
#     assert "001_users.py" not in order
#     assert "002_roles.py" in order
#
#
# def test_update_migration_at():
#     app = "crm"
#     ensure_migration_folder_and_json(app, overwrite=True)
#     add_migration(app, "001_users.py")
#     add_migration(app, "002_roles.py")
#     update_migration_at(app, 1, "002_permissions.py")
#     order = read_migration_order(app)
#     assert order[1] == "002_permissions.py"
#
#
# def test_migration_order_json_valid_structure():
#     app = "crm"
#     ensure_migration_folder_and_json(app, overwrite=True)
#     add_migration(app, "001_users.py")
#
#     project_root = Path(get_settings().project_root)
#     json_path = project_root / "apps" / app / "database" / "migration_order.json"
#
#     with open(json_path) as f:
#         order = json.load(f)
#         assert isinstance(order, list), "❌ migration_order.json must be a list"
#         assert all(isinstance(m, str) for m in order), "❌ All entries must be strings"
#
#
# def test_delete_migration_json():
#     app = "crm"
#     ensure_migration_folder_and_json(app, overwrite=True)
#     delete_migration_json(app)
#     order = read_migration_order(app)
#     assert order == []