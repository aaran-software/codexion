from cortex.database.engines.mariadb.sync_engine import SyncMariaDBEngine


class MigrationTracker:
    def __init__(self, engine: SyncMariaDBEngine):
        self.engine = engine

    def ensure_table(self) -> None:
        self.engine.execute("""
            CREATE TABLE IF NOT EXISTS migrations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL UNIQUE,
                batch INT NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

    def get_applied_migrations(self) -> list[str]:
        rows = self.engine.fetchall("SELECT name FROM migrations")
        return [row[0] for row in rows]

    def get_latest_batch(self) -> int:
        row = self.engine.fetchone("SELECT MAX(batch) FROM migrations")
        return row[0] or 0

    def record_migration(self, name: str, batch: int) -> None:
        self.engine.execute("INSERT INTO migrations (name, batch) VALUES (%s, %s)", (name, batch))

    def remove_migration(self, name: str) -> None:
        self.engine.execute("DELETE FROM migrations WHERE name = %s", (name,))