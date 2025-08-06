from cortex.database.migrations.runner import BaseMigrationRunner


def fresh_migrate(runner: BaseMigrationRunner):
    runner.engine.connect()
    print(" Dropping all tables...")
    runner.engine.execute("SET FOREIGN_KEY_CHECKS = 0")
    tables = runner.engine.fetchall("SHOW TABLES")
    for (table_name,) in tables:
        runner.engine.execute(f"DROP TABLE IF EXISTS `{table_name}`")
    runner.engine.execute("SET FOREIGN_KEY_CHECKS = 1")
    print(" All tables dropped.")
    runner.migrate()