from app.v1.routers import (
    users,
    auth,
    payment_intents,
    user_wallet_transactions,
    user_api_keys,
)
from app.core.routers.api_router import APIRouter

router = APIRouter()

router.include_router(auth.router)
router.include_router(users.router)
router.include_router(payment_intents.router)
router.include_router(user_wallet_transactions.router)
router.include_router(user_api_keys.router)

api_router = router
