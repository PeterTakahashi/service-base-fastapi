from fastapi import Depends
from app.models.organization import Organization
from app.v1.dependencies.repositories.organization_api_key_repository import (
    get_organization_api_key_repository,
)
from app.v1.repositories.organization_api_key_repository import (
    OrganizationApiKeyRepository,
)
from app.v1.dependencies.models.organization.get_organization_by_id import (
    get_organization_by_id,
)
from app.lib.utils.convert_id import decode_id


async def get_organization_api_key(
    organization_api_key_id: str,
    organization: Organization = Depends(get_organization_by_id),
    organization_api_key_repository: OrganizationApiKeyRepository = Depends(
        get_organization_api_key_repository
    ),
):
    return await organization_api_key_repository.find_by_or_raise(
        organization_id=organization.id, id=decode_id(organization_api_key_id)
    )
