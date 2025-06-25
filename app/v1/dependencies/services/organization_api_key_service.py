from app.v1.services.organization_api_key_service import OrganizationApiKeyService
from fastapi import Depends
from app.v1.dependencies.repositories.organization_api_key_repository import (
    get_organization_api_key_repository,
)
from app.v1.repositories.organization_api_key_repository import (
    OrganizationApiKeyRepository,
)


def get_organization_api_key_service(
    repository: OrganizationApiKeyRepository = Depends(
        get_organization_api_key_repository
    ),
) -> OrganizationApiKeyService:
    return OrganizationApiKeyService(repository)
