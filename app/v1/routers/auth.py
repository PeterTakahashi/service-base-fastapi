from fastapi import APIRouter
from app.v1.schemas.user import UserRead
from app.lib.fastapi_users.user_setup import fastapi_users
from app.lib.fastapi_users.auth_backend import (
    jwt_auth_backend,
    cookie_auth_backend,
    cookie_oauth_auth_backend,
)
from app.lib.fastapi_users.oauth_client import (
    github_oauth_client,
    google_oauth_client,
)
from app.lib.fastapi_users.user_manager import get_user_manager

from app.core.config import settings
from app.v1.routers.fastapi_users.get_register_router import get_register_router
from app.v1.routers.fastapi_users.get_auth_router import get_auth_router
from app.v1.routers.fastapi_users.get_oauth_router import get_oauth_router
from app.v1.routers.fastapi_users.get_reset_password_router import (
    get_reset_password_router,
)
from app.v1.routers.fastapi_users.get_verify_router import get_verify_router

router = APIRouter(prefix="/auth", tags=["Auth"])

router.include_router(
    get_auth_router(jwt_auth_backend, get_user_manager, fastapi_users.authenticator),
    prefix="/jwt",
)

router.include_router(
    get_auth_router(cookie_auth_backend, get_user_manager, fastapi_users.authenticator),
    prefix="/cookie",
)

router.include_router(
    get_register_router(get_user_manager),
    prefix="/register",
)

router.include_router(
    get_reset_password_router(get_user_manager),
)

router.include_router(
    get_verify_router(get_user_manager, UserRead),
)

router.include_router(
    get_oauth_router(
        google_oauth_client,
        cookie_oauth_auth_backend,
        get_user_manager,
        settings.GOOGLE_CLIENT_SECRET,
        redirect_url=f"{settings.BACKEND_API_V1_URL}/auth/cookie/google/callback",
        is_verified_by_default=True,
    ),
    prefix="/cookie/google",
)

router.include_router(
    get_oauth_router(
        github_oauth_client,
        cookie_oauth_auth_backend,
        get_user_manager,
        settings.GITHUB_CLIENT_SECRET,
        redirect_url=f"{settings.BACKEND_API_V1_URL}/auth/cookie/github/callback",
        is_verified_by_default=True,
    ),
    prefix="/cookie/github",
)
