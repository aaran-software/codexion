# cortex/routes/api.py


from fastapi import APIRouter
router = APIRouter()
from apps.dynamic.core.config import dynamic_json_controller

router.include_router(dynamic_json_controller.router, prefix="", tags=["json"])


