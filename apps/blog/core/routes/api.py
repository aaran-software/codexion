# cortex/routes/api.py

from apps.blog.core.config import BlogJsonController
from apps.blog.core.controllers import BlogController

from fastapi import APIRouter
router = APIRouter()

router.include_router(BlogJsonController.router, prefix="", tags=["blogsJson"])

router.include_router(BlogController.router, prefix="", tags=["blogs"])
