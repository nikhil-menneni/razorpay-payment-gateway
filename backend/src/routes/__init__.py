from fastapi import APIRouter

from src.routes.plans import planRouter 
from src.routes.payments import paymentRouter

router= APIRouter()

router.include_router(planRouter, prefix="/plans")
router.include_router(paymentRouter, prefix="/payments")