# # tests/cortex/core/test_make_migration.py
#
# from pathlib import Path
# from cortex.config.apps.make_migration import (
#     create_migration_file,
#     delete_migration_file,
#     update_migration_filename
# )
# from cortex.config.apps.migration_order_json import (
#     read_migration_order
# )
#
#
# from pathlib import Path
# from cortex.core.settings import get_settings
# from cortex.config.apps.migration_order_json import read_migration_order
# from cortex.config.apps.make_migration import create_migration_file, delete_migration_file
#
# def test_create_and_delete_migration():
#     app = "crm"
#     table = "accounts"
#
#     # 1. Create migrations
#     filename = create_migration_file(app, table)  # just "003_accounts.py"
#     project_root = Path(get_settings().project_root)
#     path = project_root / "apps" / app / "database" / "migrations" / filename
#
#     print(f"🧪 File created at: {path}")
#
#     assert path.exists(), "❌ Migration file not created"
#
#     order = read_migration_order(app)
#     assert filename in order, f"❌ Migration '{filename}' not added to order"
#
#     # 2. Delete migration
#     delete_migration_file(app, filename)
#     assert not path.exists(), f"❌ Migration file '{filename}' not deleted"
#
#     order = read_migration_order(app)
#     assert filename not in order, f"❌ Migration '{filename}' still in order"
#
#
# # def test_update_migration_filename():
# #     app = "crm"
# #     table1 = "roles"
# #     table2 = "permissions"
# #
# #     # 1. Create old migration
# #     path = Path(create_migration_file(app, table1))
# #     old_filename = path.name
# #     assert path.exists(), "❌ Initial migration file not created"
# #
# #     # 2. Update migration
# #     new_path = update_migration_filename(app, old_filename, table2)
# #     new_filename = new_path.name
# #
# #     assert new_path.exists(), "❌ Updated migration file not created"
# #     assert not path.exists(), "❌ Old migration file not deleted"
# #
# #     order = read_migration_order(app)
# #     assert new_filename in order, "❌ New filename not added to order"
# #     assert old_filename not in order, "❌ Old filename still in order"
# #
# #     # Cleanup
# #     delete_migration_file(app, new_filename)
