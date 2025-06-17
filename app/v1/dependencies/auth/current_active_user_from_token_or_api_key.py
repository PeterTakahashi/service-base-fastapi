from typing import Optional

from fastapi import Depends, Header, Request

from app.models.user import User
from app.v1.dependencies.repositories.user_api_key_repository import (
    get_user_api_key_repository,
)
from app.v1.repositories.user_api_key_repository import UserApiKeyRepository
from app.v1.repositories.user_repository import UserRepository
from app.v1.dependencies.repositories.user_repository import get_user_repository

from app.lib.exception.http.unauthorized import HTTPExceptionUnauthorized
from app.lib.datetime import as_utc, now_utc

from app.lib.fastapi_users.user_setup import optional_current_active_user


async def current_active_user_from_token_or_api_key(
    request: Request,
    api_key: Optional[str] = Header(None, alias="X-API-KEY"),
    user_by_token: Optional[User] = Depends(optional_current_active_user),
    user_api_key_repository: UserApiKeyRepository = Depends(
        get_user_api_key_repository
    ),
    user_repository: UserRepository = Depends(get_user_repository),
) -> User:
    """
    Resolve the current active user by one of two methods:

    1. If the request already carries a valid JWT / cookie, return that user.
    2. Otherwise, fall back to the X‑API‑KEY header.
       The API‑key must be:
         * present
         * unexpired
         * coming from an allowed IP (if the key enforces it)
         * coming from an allowed Origin header (if the key enforces it)

    Failure in any of the above raises HTTP 401 with an appropriate error `code`.
    """

    # ------- 1. token/cookie authentication -------
    if user_by_token:
        return user_by_token

    # ------- 2. API‑Key authentication -------
    if api_key is None:
        raise HTTPExceptionUnauthorized(request)  # missing_api_key

    try:
        user_api_key = await user_api_key_repository.find_by_or_raise(api_key=api_key)
    except Exception:
        # Only "not found" should end up here; keep it broad but specific to invalid key
        raise HTTPExceptionUnauthorized(request, "invalid_api_key")

    # ---- IP restriction ----
    if user_api_key.allowed_ip:
        client_ip = request.client.host if request.client else None
        allowed_ips = [
            ip.strip() for ip in user_api_key.allowed_ip.split(",") if ip.strip()
        ]
        if len(allowed_ips) > 0 and (client_ip is None or client_ip not in allowed_ips):
            raise HTTPExceptionUnauthorized(request, "invalid_ip")

    # ---- Origin restriction ----
    if user_api_key.allowed_origin:
        origin = request.headers.get("origin")
        allowed_origins = [
            o.strip() for o in user_api_key.allowed_origin.split(",") if o.strip()
        ]
        if len(allowed_origins) > 0 and origin not in allowed_origins:
            raise HTTPExceptionUnauthorized(request, "invalid_origin")

    # ---- Expiry check ----
    expires_at_utc = as_utc(user_api_key.expires_at)
    if expires_at_utc and expires_at_utc < now_utc():
        raise HTTPExceptionUnauthorized(request, "expired_api_key")

    user = await user_repository.find(id=user_api_key.user_id)
    return user
