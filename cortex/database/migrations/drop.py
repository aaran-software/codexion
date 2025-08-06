from cortex.database.migrations.runner import BaseMigrationRunner


def drop_specific_migration(runner: BaseMigrationRunner, migration_name: str):
    for migration in runner.migrations:
        if migration.name == migration_name:
            print(f"️ Dropping migration: {migration.name}")
            migration.down()
            runner.tracker.remove_migration(migration.name)
            return
    print(f"️ Migration not found: {migration_name}")