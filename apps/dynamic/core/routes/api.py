# cortex/routes/api.py


from fastapi import APIRouter
router = APIRouter()
from apps.dynamic.core.controllers import BlogController,CityController
from apps.dynamic.core.config import dynamic_json_controller

router.include_router(dynamic_json_controller.router, prefix="", tags=["json"])

router.include_router(BlogController.router, prefix="", tags=["blog"])
router.include_router(CityController.router, prefix="", tags=["city"])
