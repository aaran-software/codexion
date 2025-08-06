# cortex/routes/api.py

from fastapi import APIRouter

from apps.cxsun.core.controllers import PurchaseController,SalesController, PaymentController ,ReceiptController
from apps.cxsun.core.controllers import TaskController
from apps.cxsun.core.config import invoiceController
from fastapi import APIRouter
router = APIRouter()

router.include_router(PurchaseController.router, prefix="", tags=["purchases"])

router.include_router(TaskController.router, prefix="", tags=["tasks"])
router.include_router(invoiceController.router, prefix="", tags=["tasks"])

router.include_router(SalesController.router, prefix="", tags=["sales"])

router.include_router(PaymentController.router, prefix="", tags=["payment"])

router.include_router(ReceiptController.router, prefix="", tags=["receipt"])

