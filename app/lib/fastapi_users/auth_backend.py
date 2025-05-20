from fastapi_users.authentication import (
    AuthenticationBackend,
    JWTStrategy,
)
from app.core.config import settings
from app.lib.fastapi_users.transport.bearer_transport import bearer_transport
from app.lib.fastapi_users.transport.cookie_transport import cookie_transport
from app.lib.fastapi_users.transport.oauth_cookie_transport import (
    oauth_cookie_transport,
)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.JWT_SECRET,
        lifetime_seconds=settings.ACCESS_TOKEN_EXPIRED_SECONDS,
    )


jwt_auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

cookie_auth_backend = AuthenticationBackend(
    name="cookie",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

cookie_oauth_auth_backend = AuthenticationBackend(
    name="cookie_oauth",
    transport=oauth_cookie_transport,
    get_strategy=get_jwt_strategy,
)
