from fastapi import APIRouter, Response, status
from prefiq.core.contracts.base_provider import Application
from prefiq.database.engines.mariadb.health import is_healthy

router = APIRouter()

@router.get("/healthz")
def healthz():
    app = Application.get_app()
    try:
        db = app.resolve("db")
    except Exception:
        return Response(
            content='{"status":"degraded","reason":"db_not_bound"}',
            media_type="application/json",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    ok = is_healthy(db)  # timeout built-in
    if ok:
        return {"status": "ok"}
    return Response(
        content='{"status":"degraded","reason":"db_unhealthy"}',
        media_type="application/json",
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    )
