import os

from prefiq.core.application import Application
from prefiq.core.service_providers import get_service_providers
from prefiq.settings.get_settings import load_settings
from prefiq.database.connection import get_engine

def main() -> None:
    app = Application.get_app()

    for provider_cls in get_service_providers():
        app.register(provider_cls)

    app.boot()

    # simple dev printout
    s = load_settings()
    engine_class = type(get_engine()).__name__
    if os.getenv("PREFIQ_BOOTSTRAP_VERBOSE", "0") == "1":
        print(f"ENGINE={s.DB_ENGINE} MODE={s.DB_MODE} -> {engine_class}")

if __name__ == "__main__":
    main()
