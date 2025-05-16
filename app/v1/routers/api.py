from fastapi import APIRouter
from app.v1.routers import users, auth

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(users.router, prefix="/users", tags=["users"])

api_router = router
