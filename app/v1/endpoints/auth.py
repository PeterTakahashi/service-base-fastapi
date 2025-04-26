from fastapi import APIRouter
from app.schemas import UserRead, UserCreate
from app.core.user_setup import fastapi_users
from app.core.auth import auth_backend

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/register",
    tags=["auth"],
)
