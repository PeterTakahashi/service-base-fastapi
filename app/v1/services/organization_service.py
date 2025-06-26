from app.v1.schemas.organization import (
    OrganizationRead,
    OrganizationListRead,
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationSearchParams,
)
from app.models.user import User
from app.models.organization import Organization
from app.v1.repositories.organization_repository import OrganizationRepository
from app.v1.repositories.user_organization_assignment_repository import (
    UserOrganizationAssignmentRepository,
)
from app.v1.repositories.organization_wallet_repository import (
    OrganizationWalletRepository,
)
from app.v1.repositories.organization_address_repository import (
    OrganizationAddressRepository,
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
        organization_address_repository: OrganizationAddressRepository,
    ):
        self.organization_repository = organization_repository
        self.organization_address_repository = organization_address_repository
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
            joinedload_models=[Organization.address],
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
            tax_type=organization_params.tax_type,
            tax_id=organization_params.tax_id,
        )
        organization.address = await self.organization_address_repository.create(
            organization_id=organization.id,
            city=organization_params.address.city,
            country=organization_params.address.country,
            line1=organization_params.address.line1,
            line2=organization_params.address.line2,
            postal_code=organization_params.address.postal_code,
            state=organization_params.address.state,
        )
        await self.user_organization_assignment_repository.create(
            user_id=user.id,
            organization_id=organization.id,
        )
        customer = stripe.Customer.create(
            name=organization.name,
            email=organization.billing_email,
            description=organization.description,
            address={
                "city": organization.address.city,
                "country": organization.address.country,
                "line1": organization.address.line1,
                "line2": organization.address.line2,
                "postal_code": organization.address.postal_code,
                "state": organization.address.state,
            },
        )
        await self.organization_wallet_repository.create(
            organization_id=organization.id,
            stripe_customer_id=customer.id,
        )
        return OrganizationRead.model_validate(organization)  # type: ignore

    async def update(
        self, id: int, organization_params: OrganizationUpdate
    ) -> OrganizationRead:
        organization = await self.organization_repository.update(
            id=id,
            name=organization_params.name,
            description=organization_params.description,
            billing_email=organization_params.billing_email,
            profile_image_key=organization_params.profile_image_key,  # TODO: upload to storage
            tax_type=organization_params.tax_type,
            tax_id=organization_params.tax_id,
        )
        address = await self.organization_address_repository.find_by(
            organization_id=id,
        )
        organization.address = await self.organization_address_repository.update(
            id=address.id,
            city=organization_params.address.city,
            country=organization_params.address.country,
            line1=organization_params.address.line1,
            line2=organization_params.address.line2,
            postal_code=organization_params.address.postal_code,
            state=organization_params.address.state,
        )
        organization_wallet = (
            await self.organization_wallet_repository.find_by_or_raise(
                organization_id=id,
            )
        )
        stripe.Customer.modify(
            organization_wallet.stripe_customer_id,
            metadata={
                "name": organization.name,
                "email": organization.billing_email,
                "description": organization.description,
                "address": {
                    "city": organization.address.city,
                    "country": organization.address.country,
                    "line1": organization.address.line1,
                    "line2": organization.address.line2,
                    "postal_code": organization.address.postal_code,
                    "state": organization.address.state,
                },
            },
        )
        return OrganizationRead.model_validate(organization)

    async def delete(self, id: int) -> None:
        await self.user_organization_assignment_repository.update_all(
            {"deleted_at": datetime.utcnow()},
            organization_id__exact=id,
            deleted_at__exact=None,
        )
        await self.organization_repository.soft_delete(id)
