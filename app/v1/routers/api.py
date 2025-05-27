from fastapi import APIRouter
from app.v1.routers import users, auth, payment_intents

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(
    payment_intents.router, prefix="/payment-intents", tags=["payment_intents"]
)

api_router = router
