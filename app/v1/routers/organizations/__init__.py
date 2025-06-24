from fastapi import APIRouter
from .crud import router as crud_router
from .users.router import router as users_router

router = APIRouter()
router.include_router(crud_router)
router.include_router(users_router)

__all__ = ["router"]
