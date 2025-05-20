from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
    CookieTransport,
)
from app.lib.fastapi_users.custom_cookie_transport import CustomCookieTransport
from app.core.config import settings
from httpx_oauth.clients.google import GoogleOAuth2
from httpx_oauth.clients.github import GitHubOAuth2

github_oauth_client = GitHubOAuth2(
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_CLIENT_SECRET
)

google_oauth_client = GoogleOAuth2(
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET
)

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
access_token_expires = 3600 * 24 * 7  # 1 week


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.JWT_SECRET, lifetime_seconds=access_token_expires
    )


jwt_auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

oauth_cookie_transport = CustomCookieTransport(
    cookie_name="access_token",
    cookie_max_age=access_token_expires,  # 1 week
    cookie_secure=settings.SECURE_COOKIES,
    cookie_httponly=True,
)

cookie_transport = CookieTransport(
    cookie_name="access_token",
    cookie_max_age=access_token_expires,  # 1 week
    cookie_secure=settings.SECURE_COOKIES,
    cookie_httponly=True,
)


cookie_auth_backend = AuthenticationBackend(
    name="cookie",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

cookie_auth_backend_oauth = AuthenticationBackend(
    name="cookie_oauth",
    transport=oauth_cookie_transport,
    get_strategy=get_jwt_strategy,
)