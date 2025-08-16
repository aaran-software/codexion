# cortex/core/runtime/bootstrap.py

from cortex.core.contracts.base_provider import Application
from cortex.core.providers.service_providers import SERVICE_PROVIDERS

if __name__ == "__main__":
    app = Application.get_app()

    # Lifecycle hooks
    app.on_booting(lambda: print("[App] Booting started..."))
    app.on_booted(lambda: print("[App] Boot finished."))

    # Register all service providers from the global registry
    for provider in SERVICE_PROVIDERS:
        app.register(provider)

    # Boot application
    app.boot()

    # Example: resolve profiles
    profiles = app.resolve("profiles")
    print("[Profiles] Database URL →", profiles.get("database", {}).get("url"))
