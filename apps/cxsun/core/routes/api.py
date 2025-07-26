# cortex/routes/api.py

from fastapi import APIRouter

from apps.cxsun.core.controllers import purchaseController
from apps.cxsun.core.controllers import TaskController
from apps.cxsun.core.config import invoiceController
from fastapi import APIRouter
router = APIRouter()

router.include_router(purchaseController.router, prefix="", tags=["purchases"])
router.include_router(TaskController.router, prefix="", tags=["tasks"])
router.include_router(invoiceController.router, prefix="", tags=["tasks"])
