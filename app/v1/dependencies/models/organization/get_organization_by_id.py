from fastapi import Depends
from app.models.organization import Organization
from app.v1.repositories.organization_repository import OrganizationRepository
from app.v1.dependencies.repositories.organization_repository import (
    get_organization_repository,
)


async def get_organization_by_id(
    id: int,
    organization_repository: OrganizationRepository = Depends(
        get_organization_repository
    ),
) -> Organization:
    return await organization_repository.find(id)
