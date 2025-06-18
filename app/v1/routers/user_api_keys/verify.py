from fastapi import Depends, status

from app.v1.schemas.user_api_key.verify import UserApiKeyVerifyResponse
from app.v1.dependencies.services.user_api_key_service import get_user_api_key_service
from app.v1.services.user_api_key_service import UserApiKeyService

from app.v1.dependencies.auth.current_active_user_from_token_or_api_key import (
    current_active_user_from_token_or_api_key,
)
from app.models.user import User

from app.core.routers.auth_api_router import AuthAPIRouter

router = AuthAPIRouter(prefix="/user-api-keys", tags=["User API Keys"])


@router.post(
    "/verify",
    response_model=UserApiKeyVerifyResponse,
    status_code=status.HTTP_200_OK,
    name="user_api_keys:verify_user_api_key",
)
async def verify_user_api_key(
    user: User = Depends(current_active_user_from_token_or_api_key),
    service: UserApiKeyService = Depends(get_user_api_key_service),
):
    return UserApiKeyVerifyResponse(
        is_valid=True,
    )
