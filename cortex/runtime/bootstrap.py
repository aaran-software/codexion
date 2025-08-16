from prefiq.core.contracts.base_provider import Application
from prefiq.core.runtime.service_providers import PROVIDERS

def main():
    app = Application.get_app()

    # Register all providers
    for provider in PROVIDERS:
        app.register(provider)

    app.boot()

    # Now DB is available
    db = app.resolve("db")

    # Simple test
    users = db.fetchall("SELECT user()")
    print("[Cortex] Connected DB user:", users)

if __name__ == "__main__":
    main()
