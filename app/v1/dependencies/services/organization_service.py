from fastapi import Depends
from app.v1.services.organization_service import OrganizationService
from app.v1.repositories.organization_repository import OrganizationRepository
from app.v1.dependencies.repositories.organization_repository import (
    get_organization_repository,
)
from app.v1.repositories.user_organization_assignment_repository import (
    UserOrganizationAssignmentRepository,
)
from app.v1.dependencies.repositories.user_organization_assignment_repository import (
    get_user_organization_assignment_repository,
)
from app.v1.dependencies.repositories.organization_wallet_repository import (
    get_organization_wallet_repository,
)
from app.v1.repositories.organization_wallet_repository import (
    OrganizationWalletRepository,
)
from app.v1.dependencies.repositories.organization_address_repository import (
    get_organization_address_repository,
)


def get_organization_service(
    organization_repository: OrganizationRepository = Depends(
        get_organization_repository
    ),
    user_organization_assignment_repository: UserOrganizationAssignmentRepository = Depends(
        get_user_organization_assignment_repository
    ),
    organization_wallet_repository: OrganizationWalletRepository = Depends(
        get_organization_wallet_repository
    ),
    organization_address_repository = Depends(get_organization_address_repository),
) -> OrganizationService:
    return OrganizationService(
        organization_repository=organization_repository,
        user_organization_assignment_repository=user_organization_assignment_repository,
        organization_wallet_repository=organization_wallet_repository,
        organization_address_repository=organization_address_repository,
    )
