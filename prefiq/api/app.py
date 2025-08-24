from fastapi import FastAPI
from prefiq.api.health import router as health_router
from prefiq.core.runtime.bootstrap import main as boot_main
from prefiq.core.contracts.base_provider import Application
from prefiq.log.logger import get_logger
from prefiq.settings.get_settings import load_settings

app = FastAPI(title="Prefiq API")

@app.on_event("startup")
def _startup():
    boot_main()

@app.on_event("shutdown")
def _shutdown():
    s = load_settings()
    log = get_logger(f"{s.LOG_NAMESPACE}.bootstrap")
    appc = Application.get_app()
    try:
        db = appc.resolve("db")
        # close can be sync or async
        if hasattr(db, "close"):
            maybe = db.close()
            # if async, run to completion
            import inspect, asyncio
            if inspect.isawaitable(maybe):
                asyncio.run(maybe)
        log.info("db_closed_on_shutdown")
    except Exception as e:
        log.error("db_close_failed_on_shutdown", extra={"error": str(e)})

app.include_router(health_router)
