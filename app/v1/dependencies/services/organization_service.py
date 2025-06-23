from fastapi import Depends
from app.v1.services.organization_service import OrganizationService
from app.v1.repositories.organization_repository import OrganizationRepository
from app.v1.dependencies.repositories.organization_repository import (
    get_organization_repository,
)


def get_organization_service(
    organization_repository: OrganizationRepository = Depends(
        get_organization_repository
    ),
) -> OrganizationService:
    return OrganizationService(organization_repository=organization_repository)
