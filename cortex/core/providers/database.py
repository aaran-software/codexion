from cortex.core.providers.base import ServiceProvider


class DatabaseServiceProvider(ServiceProvider):
    def register(self):
        db_config = self.config.get("database", {})
        self.app.singleton("db", lambda: f"DB({db_config['driver']} @ {db_config['host']})")

    def boot(self):
        print("Booting DB provider:", self.app.make("db"))
