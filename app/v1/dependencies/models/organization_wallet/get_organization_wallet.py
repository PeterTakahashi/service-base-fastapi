from fastapi import Depends
from app.models.organization import Organization
from app.v1.repositories.organization_wallet_repository import (
    OrganizationWalletRepository,
)
from app.v1.dependencies.models.organization.get_organization_by_id import (
    get_not_assigned_organization_by_id,
)
from app.v1.dependencies.repositories.organization_wallet_repository import (
    get_organization_wallet_repository,
)


async def get_organization_wallet(
    organization: Organization = Depends(get_not_assigned_organization_by_id),
    organization_wallet_repository: OrganizationWalletRepository = Depends(
        get_organization_wallet_repository
    ),
):
    return await organization_wallet_repository.find_by_or_raise(
        organization_id=organization.id
    )
