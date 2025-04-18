from fastapi import APIRouter
from app.v1.endpoints import users, auth, products

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(users.router, prefix="/users", tags=["auth"])
router.include_router(products.router, prefix="/products", tags=["products"])

api_router = router
