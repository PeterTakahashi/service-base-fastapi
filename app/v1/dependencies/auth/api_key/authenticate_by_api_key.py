from typing import Optional, Literal

from fastapi import Request, status

from app.models.organization_api_key import OrganizationApiKey
from app.models.user_api_key import UserApiKey

from app.v1.repositories.organization_api_key_repository import (
    OrganizationApiKeyRepository,
)
from app.v1.repositories.user_api_key_repository import UserApiKeyRepository


from app.lib.exception.api_exception import init_api_exception
from app.lib.utils.datetime import as_utc, now_utc
from app.lib.error_code import ErrorCode


async def _authenticate_by_api_key(
    request: Request,
    api_key_str: Optional[str],
    api_key_repository: OrganizationApiKeyRepository | UserApiKeyRepository,
    prefix: Literal["organization_", "user_"] = "organization_",
) -> OrganizationApiKey | UserApiKey | None:
    """
    Resolve the current active organization by one of two methods:

    1. If the request already carries a valid JWT / cookie, return that organization.
    2. Otherwise, fall back to the X‑API‑KEY header.
       The API‑key must be:
         * present
         * unexpired
         * coming from an allowed IP (if the key enforces it)
         * coming from an allowed Origin header (if the key enforces it)

    Failure in any of the above raises HTTP 401 with an appropriate error `code`.
    """
    # ------- 1. API‑Key authentication -------
    if api_key_str is None or api_key_str == "":
        raise init_api_exception(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail_code=ErrorCode.UNAUTHORIZED_API_KEY,
        )

    if not api_key_str.startswith(prefix):
        return None

    api_key = await api_key_repository.find_by(api_key=api_key_str)

    if api_key is None:
        return None

    # ---- IP restriction ----
    if api_key.allowed_ip:
        client_ip = request.client.host if request.client else None
        allowed_ips = [ip.strip() for ip in api_key.allowed_ip.split(",") if ip.strip()]
        if len(allowed_ips) > 0 and (client_ip is None or client_ip not in allowed_ips):
            raise init_api_exception(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail_code=ErrorCode.INVALID_IP,
            )

    # ---- Origin restriction ----
    if api_key.allowed_origin:
        origin = request.headers.get("origin")
        allowed_origins = [
            o.strip() for o in api_key.allowed_origin.split(",") if o.strip()
        ]
        if len(allowed_origins) > 0 and origin not in allowed_origins:
            raise init_api_exception(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail_code=ErrorCode.INVALID_ORIGIN,
            )

    # ---- Expiry check ----
    expires_at_utc = as_utc(api_key.expires_at)
    if expires_at_utc and expires_at_utc < now_utc():
        raise init_api_exception(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail_code=ErrorCode.EXPIRED_API_KEY,
        )

    return api_key
