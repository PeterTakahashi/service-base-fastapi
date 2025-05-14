from fastapi import APIRouter
from app.v1.routers import users, auth, products, characters, character_images

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(users.router, prefix="/users", tags=["auth"])
products.router.include_router(
    characters.router, prefix="/{product_id}/characters", tags=["characters"]
)
router.include_router(products.router, prefix="/products", tags=["products"])
router.include_router(
    character_images.router, prefix="/character-images", tags=["character_images"]
)

api_router = router
