# from fastapi import Depends, status

# from app.v1.schemas.organization_api_key.verify import OrganizationApiKeyVerifyResponse
# from app.v1.dependencies.services.organization_api_key_service import get_organization_api_key_service
# from app.v1.services.organization_api_key_service import OrganizationApiKeyService

# from app.v1.dependencies.auth.current_active_organization_from_token_or_api_key import (
#     current_active_organization_from_token_or_api_key,
# )
# from app.models.organization import Organization

# from app.core.routers.api_key_auth_api_router import ApiKeyAuthAPIRouter

# router = ApiKeyAuthAPIRouter(prefix="/api-keys", tags=["Organization API Keys"])


# @router.post(
#     "/verify",
#     response_model=OrganizationApiKeyVerifyResponse,
#     status_code=status.HTTP_200_OK,
#     name="organization_api_keys:verify_organization_api_key",
# )
# async def verify_organization_api_key(
#     organization: Organization = Depends(current_active_organization_from_token_or_api_key),
#     service: OrganizationApiKeyService = Depends(get_organization_api_key_service),
# ):
#     return OrganizationApiKeyVerifyResponse(
#         is_valid=True,
#     )
