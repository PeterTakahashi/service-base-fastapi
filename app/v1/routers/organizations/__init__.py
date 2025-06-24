from fastapi import APIRouter
from .crud import router as crud_router

router = APIRouter()
router.include_router(crud_router)

__all__ = ["router"]
