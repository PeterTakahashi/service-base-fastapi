from fastapi import APIRouter
from app.v1.schemas.user import UserRead, UserCreate
from app.core.user_setup import fastapi_users
from app.core.auth import jwt_auth_backend, cookie_auth_backend, github_oauth_client, google_oauth_client, cookie_auth_backend_oauth
from app.core.config import settings

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(jwt_auth_backend),
    prefix="/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_auth_router(cookie_auth_backend),
    prefix="/cookie",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),  # type: ignore
    prefix="/register",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_reset_password_router(),
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_verify_router(UserRead),  # type: ignore
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_oauth_router(
        google_oauth_client,
        cookie_auth_backend_oauth,
        settings.GOOGLE_CLIENT_SECRET,
        redirect_url=f"{settings.BACKEND_API_V1_URL}/auth/cookie/google/callback",
        is_verified_by_default=True,
    ),
    prefix="/cookie/google",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_oauth_router(
        github_oauth_client,
        cookie_auth_backend_oauth,
        settings.GITHUB_CLIENT_SECRET,
        redirect_url=f"{settings.BACKEND_API_V1_URL}/auth/cookie/github/callback",
        is_verified_by_default=True,
    ),
    prefix="/cookie/github",
    tags=["auth"],
)