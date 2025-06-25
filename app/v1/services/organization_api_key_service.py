from app.v1.schemas.organization_api_key import (
    OrganizationApiKeyListRead,
    OrganizationApiKeyRead,
    OrganizationApiKeyCreate,
    OrganizationApiKeyUpdate,
    OrganizationApiKeySearchParams,
)
from app.v1.schemas.common.list.base_list_response import ListResponseMeta
import secrets
from uuid import UUID


class OrganizationApiKeyService:
    def __init__(self, organization_api_key_repository):
        self.organization_api_key_repository = organization_api_key_repository

    async def get_list(
        self, organization_id: int, search_params: OrganizationApiKeySearchParams
    ) -> OrganizationApiKeyListRead:
        """
        Retrieve a list of organization API keys with filtering, sorting, and pagination.
        """
        organization_api_keys = await self.organization_api_key_repository.where(
            **search_params.model_dump(exclude_none=True),
            organization_id=organization_id,
        )
        total_count = await self.organization_api_key_repository.count(
            **search_params.model_dump(
                exclude_none=True,
                exclude={"limit", "offset", "sorted_by", "sorted_order"},
            ),
            organization_id=organization_id,
        )
        return OrganizationApiKeyListRead(
            meta=ListResponseMeta(
                total_count=total_count,
                **search_params.model_dump(exclude_none=True),
            ),
            data=[
                OrganizationApiKeyRead.model_validate(tx)
                for tx in organization_api_keys
            ],
        )

    async def create(
        self,
        user_id: UUID,
        organization_id: int,
        organization_api_key_create: OrganizationApiKeyCreate,
    ) -> OrganizationApiKeyRead:
        """
        Create a new organization API key.
        """
        api_key = secrets.token_urlsafe(32)
        organization_api_key = await self.organization_api_key_repository.create(
            organization_id=organization_id,
            api_key=api_key,
            created_by_user_id=user_id,
            **organization_api_key_create.model_dump(),
        )
        return OrganizationApiKeyRead.model_validate(organization_api_key)

    async def update(
        self,
        organization_api_key_id: int,
        organization_api_key_update: OrganizationApiKeyUpdate,
    ) -> OrganizationApiKeyRead:
        """
        Update an existing organization API key.
        """
        organization_api_key = await self.organization_api_key_repository.update(
            id=organization_api_key_id, **organization_api_key_update.model_dump()
        )
        return OrganizationApiKeyRead.model_validate(organization_api_key)

    async def delete(self, organization_api_key_id: int) -> None:
        """
        Delete a organization API key.
        """
        await self.organization_api_key_repository.soft_delete(
            id=organization_api_key_id
        )
