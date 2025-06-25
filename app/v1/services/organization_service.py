from app.v1.schemas.organization import (
    OrganizationRead,
    OrganizationListRead,
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationSearchParams,
)
from app.models.user import User
from app.v1.repositories.organization_repository import OrganizationRepository
from app.v1.repositories.user_organization_assignment_repository import (
    UserOrganizationAssignmentRepository,
)
from app.v1.repositories.organization_wallet_repository import (
    OrganizationWalletRepository,
)

from uuid import UUID
from app.v1.schemas.common.list.base_list_response import ListResponseMeta
from datetime import datetime

from app.lib.utils.stripe import stripe


class OrganizationService:
    def __init__(
        self,
        organization_repository: OrganizationRepository,
        user_organization_assignment_repository: UserOrganizationAssignmentRepository,
        organization_wallet_repository: OrganizationWalletRepository,
    ):
        self.organization_repository = organization_repository
        self.user_organization_assignment_repository = (
            user_organization_assignment_repository
        )
        self.organization_wallet_repository = organization_wallet_repository

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
        await self.user_organization_assignment_repository.create(
            user_id=user.id,
            organization_id=organization.id,
        )
        customer = stripe.Customer.create(
            name=organization.name,
            email=organization.billing_email,
            description=organization.description,
        )
        await self.organization_wallet_repository.create(
            organization_id=organization.id,
            stripe_customer_id=customer.id,
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
        await self.user_organization_assignment_repository.update_all(
            {"deleted_at": datetime.utcnow()},
            organization_id__exact=id,
            deleted_at__exact=None,
        )
        await self.organization_repository.soft_delete(id)
