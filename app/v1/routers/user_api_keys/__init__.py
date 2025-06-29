from fastapi import APIRouter
from .crud import router as crud_router
from .verify import router as verify_router

router = APIRouter()
router.include_router(crud_router)
router.include_router(verify_router)

__all__ = ["router"]
