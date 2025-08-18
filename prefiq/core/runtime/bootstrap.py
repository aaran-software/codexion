# prefiq/core/runtime/bootstrap.py

from __future__ import annotations

from prefiq.core.contracts.base_provider import Application
from cortex.runtime.service_providers import PROVIDERS

from prefiq.settings.get_settings import load_settings
from prefiq.log.logger import configure_logging, get_logger


def main() -> None:
    # 1) Configure logging once at process start
    settings = load_settings()
    configure_logging(
        level=getattr(settings, "LOG_LEVEL", "INFO"),
        fmt=getattr(settings, "LOG_FORMAT", "json"),
        base_logger=getattr(settings, "LOG_NAMESPACE", "prefiq"),
        color=getattr(settings, "LOG_COLOR", None),   # optional; "auto"/"true"/"false"
    )

    log = get_logger(f"{getattr(settings, 'LOG_NAMESPACE', 'prefiq')}.bootstrap")

    # 2) Build application + lifecycle hooks with structured logs
    app = Application.get_app()
    app.on_booting(lambda: log.info("boot_start"))
    app.on_booted(lambda: log.info("boot_finished"))

    # 3) Register providers from registry
    for provider in PROVIDERS:
        app.register(provider)

    # 4) Boot
    app.boot()

    # 5) Post-boot: verify bindings you care about
    try:
        db = app.resolve("db")
        log.debug("db_bound", extra={"bound": bool(db)})
    except Exception as e:
        log.error("db_bind_failed", extra={"error": str(e)})


if __name__ == "__main__":
    main()
