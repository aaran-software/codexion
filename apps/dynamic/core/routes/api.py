# cortex/routes/api.py

from apps.dynamic.core.controllers import blog_controller

from fastapi import APIRouter
router = APIRouter()

router.include_router(blog_controller.router, prefix="", tags=["blogs"])
