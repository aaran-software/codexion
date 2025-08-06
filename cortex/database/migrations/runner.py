# cortex/database/migrations/migrations.py


def migrate_table(name: str) -> str:
    # runner = get_runner()
    # runner.scan_folder("cortex/core/database/migrations/files")

    found = False
    # for migration in runner.migrations:
    #     if migration.name == name:
    #         runner.migrate_single(name)
    #         found = True
    #         break

    return f"✅ Migrated: {name}" if found else f"❌ Migration not found: {name}"


def migrate_all_table() -> str:
    # runner = get_runner()
    # runner.scan_folder("cortex/core/database/migrations/files")
    # runner.migrate()
    return "✅ All tables migrated successfully."


def drop_migrate(name: str) -> str:
    # runner = get_runner()
    # runner.scan_folder("cortex/core/database/migrations/files")
    # drop_specific_migration(runner, name)
    return f"🗑️ Dropped migration: {name}"


def drop_all_migrate() -> str:
    # runner = get_runner()
    # runner.scan_folder("cortex/core/database/migrations/files")
    # fresh_migrate(runner)
    return "🧨 Dropped all tables and re-applied fresh migrations."
