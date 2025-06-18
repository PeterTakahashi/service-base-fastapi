from fastapi_users.authentication import (
    CookieTransport,
)
from app.core.config import settings

cookie_transport = CookieTransport(
    cookie_name="access_token",
    cookie_max_age=settings.ACCESS_TOKEN_EXPIRED_SECONDS,
    cookie_secure=settings.SECURE_COOKIES,
    cookie_httponly=True,
)
