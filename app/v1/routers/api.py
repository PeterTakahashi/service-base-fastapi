from app.v1.routers import (
    users,
    auth,
    user_wallet_transactions,
    user_api_keys,
    organizations,
    payment_intents,
)
from app.core.routers.api_router import APIRouter
from app.v1.routers.users.user_payment_intents.router import (
    router as user_payment_intents_router,
)

router = APIRouter()

router.include_router(auth.router)
router.include_router(users.router)
router.include_router(payment_intents.router)
router.include_router(user_payment_intents_router)
router.include_router(user_wallet_transactions.router)
router.include_router(user_api_keys.router)
router.include_router(organizations.router)

api_router = router
