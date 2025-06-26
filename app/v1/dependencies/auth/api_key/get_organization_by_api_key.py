from fastapi import Depends, Header, Request

from app.models.organization import Organization
from app.v1.dependencies.repositories.organization_api_key_repository import (
    get_organization_api_key_repository,
)
from app.v1.repositories.organization_api_key_repository import (
    OrganizationApiKeyRepository,
)
from app.v1.repositories.organization_repository import OrganizationRepository
from app.v1.dependencies.repositories.organization_repository import (
    get_organization_repository,
)


from .authenticate_by_api_key import _authenticate_by_api_key


async def get_organization_by_api_key(
    request: Request,
    api_key_str: str = Header(..., alias="X-API-KEY"),
    api_key_repository: OrganizationApiKeyRepository = Depends(
        get_organization_api_key_repository
    ),
    organization_repository: OrganizationRepository = Depends(
        get_organization_repository
    ),
) -> Organization | None:
    api_key = await _authenticate_by_api_key(
        request=request,
        api_key_str=api_key_str,
        api_key_repository=api_key_repository,
        prefix="organization_",
    )
    if api_key is None:
        return None

    organization = await organization_repository.find(id=api_key.organization_id)
    return organization
