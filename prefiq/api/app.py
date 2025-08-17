from fastapi import FastAPI
from prefiq.api.health import router as health_router
from prefiq.core.runtime.bootstrap import main as boot_main

app = FastAPI(title="Prefiq API")

# Boot your service providers once at startup
@app.on_event("startup")
def _startup():
    boot_main()

app.include_router(health_router)

# If you want to run directly:  uvicorn prefiq.api.app:app --reload
