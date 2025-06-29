from fastapi import Depends, status

from app.v1.schemas.common.api_key.verify import ApiKeyVerifyResponse

from app.v1.dependencies.auth.api_key.get_user_or_organization_by_api_key import (
    get_user_or_organization_by_api_key,
)
from app.models.organization import Organization
from app.models.user import User

from app.core.routers.api_key_auth_api_router import ApiKeyAuthAPIRouter

router = ApiKeyAuthAPIRouter(prefix="/api-keys", tags=["API Keys"])


@router.post(
    "/verify",
    response_model=ApiKeyVerifyResponse,
    status_code=status.HTTP_200_OK,
    name="organization_api_keys:verify_organization_api_key",
)
async def verify_organization_api_key(
    user_or_organization: User | Organization = Depends(
        get_user_or_organization_by_api_key
    ),
):
    return ApiKeyVerifyResponse(
        is_valid=True, owner_type=user_or_organization.__class__.__name__.lower()
    )
