from cortex.core.providers.base import ServiceProvider

class MigrationServiceProvider(ServiceProvider):
    def register(self):
        self.app.singleton("migrator", lambda: "Migrator ready")

    def boot(self):
        print("MigrationServiceProvider booted")
