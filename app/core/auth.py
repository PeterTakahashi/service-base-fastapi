from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
    CookieTransport,
)
from app.core.config import settings

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
access_token_expires = 3600 * 24 * 7  # 1 week

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.JWT_SECRET, lifetime_seconds=access_token_expires)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

cookie_transport = CookieTransport(
    cookie_name="access_token",
    cookie_max_age=access_token_expires,  # 1 week
    cookie_secure=settings.SECURE_COOKIES,
    cookie_httponly=True,
)

def get_cookie_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.JWT_SECRET, lifetime_seconds=access_token_expires)

cookie_auth_backend = AuthenticationBackend(
    name="cookie",
    transport=cookie_transport,
    get_strategy=get_cookie_jwt_strategy,
)