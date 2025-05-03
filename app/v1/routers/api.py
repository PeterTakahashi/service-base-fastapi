from fastapi import APIRouter
from app.v1.routers import users, auth, products, characters

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(users.router, prefix="/users", tags=["auth"])
products.router.include_router(
    characters.router,
    prefix="/{product_id}/characters",
    tags=["characters"]
)
router.include_router(products.router, prefix="/products", tags=["products"])

api_router = router
