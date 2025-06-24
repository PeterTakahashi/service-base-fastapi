from fastapi import Depends
from app.v1.repositories.user_repository import UserRepository
from app.v1.services.organization_user_service import OrganizationUserService
from app.v1.dependencies.repositories.user_repository import get_user_repository


def get_organization_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> OrganizationUserService:
    return OrganizationUserService(
        user_repository=user_repository,
    )
