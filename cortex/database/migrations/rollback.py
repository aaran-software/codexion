from cortex.database.migrations.runner import BaseMigrationRunner


def rollback_last_batch(runner: BaseMigrationRunner):
    runner.engine.connect()
    tracker = runner.tracker
    tracker.ensure_table()

    batch = tracker.get_latest_batch()
    applied = tracker.get_applied_migrations()

    for migration in reversed(runner.migrations):
        if migration.name in applied:
            print(f" Rolling back: {migration.name}")
            migration.down()
            tracker.remove_migration(migration.name)