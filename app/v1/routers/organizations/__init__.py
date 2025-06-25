from fastapi import APIRouter
from .crud import router as crud_router
from .invite.router import router as invite_router
from .users.router import router as users_router
from .wallet_transactions.router import router as wallet_transactions_router

router = APIRouter()
router.include_router(crud_router)
router.include_router(invite_router)
router.include_router(users_router)
router.include_router(wallet_transactions_router)

__all__ = ["router"]
