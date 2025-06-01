from fastapi import APIRouter
from app.v1.routers import users, auth, payment_intents, wallet_transactions

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(
    payment_intents.router, prefix="/payment-intents", tags=["payment_intents"]
)
router.include_router(
    wallet_transactions.router,
    prefix="/wallet-transactions",
    tags=["wallet_transactions"],
)

api_router = router
