from app.v1.schemas.organization import (
    OrganizationRead,
    OrganizationListRead,
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationSearchParams,
)
from app.models.user import User
from app.v1.repositories.organization_repository import OrganizationRepository
from uuid import UUID
from app.v1.schemas.common.list.base_list_response import ListResponseMeta


class OrganizationService:
    def __init__(self, organization_repository: OrganizationRepository):
        self.organization_repository = organization_repository

    async def get_list(
        self, user_id: UUID, search_params: OrganizationSearchParams
    ) -> OrganizationListRead:
        """
        Retrieve a list of organizations with filtering, sorting, and pagination.
        """
        organizations = await self.organization_repository.where(
            **search_params.model_dump(exclude_none=True),
            created_by_user_id=user_id,
        )
        total_count = await self.organization_repository.count(
            **search_params.model_dump(
                exclude_none=True,
                exclude={"limit", "offset", "sorted_by", "sorted_order"},
            ),
            created_by_user_id=user_id,
        )
        return OrganizationListRead(
            meta=ListResponseMeta(
                total_count=total_count,
                **search_params.model_dump(exclude_none=True),
            ),
            data=[OrganizationRead.model_validate(tx) for tx in organizations],
        )

    async def get(self, id: int) -> OrganizationRead:
        organization = await self.organization_repository.find(id)
        return OrganizationRead.model_validate(organization)

    async def create(
        self,
        organization_params: OrganizationCreate,
        user: User,
    ) -> OrganizationRead:
        organization = await self.organization_repository.create(
            name=organization_params.name,
            description=organization_params.description,
            billing_email=organization_params.billing_email,
            profile_image_key=organization_params.profile_image_key,  # TODO: upload to storage
            created_by_user_id=user.id,
        )
        return OrganizationRead.model_validate(organization)

    async def update(
        self, id: int, organization_params: OrganizationUpdate
    ) -> OrganizationRead:
        organization = await self.organization_repository.update(
            id=id,
            name=organization_params.name,
            description=organization_params.description,
            billing_email=organization_params.billing_email,
            profile_image_key=organization_params.profile_image_key,  # TODO: upload to storage
        )
        return OrganizationRead.model_validate(organization)

    async def delete(self, id: int) -> None:
        await self.organization_repository.soft_delete(id)
