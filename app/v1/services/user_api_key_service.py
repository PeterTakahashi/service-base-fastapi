from app.v1.schemas.user_api_key import (
    UserApiKeyListRead,
    UserApiKeyRead,
    UserApiKeyCreate,
    UserApiKeyUpdate,
    UserApiKeySearchParams,
)
from app.v1.schemas.common.list.base_list_response import ListResponseMeta
from uuid import UUID
import secrets

from app.models.user_api_key import API_KEY_PREFIX


class UserApiKeyService:
    def __init__(self, user_api_key_repository):
        self.user_api_key_repository = user_api_key_repository

    async def get_list(
        self, user_id: UUID, search_params: UserApiKeySearchParams
    ) -> UserApiKeyListRead:
        """
        Retrieve a list of user API keys with filtering, sorting, and pagination.
        """
        user_api_keys = await self.user_api_key_repository.where(
            **search_params.model_dump(exclude_none=True),
            user_id=user_id,
        )
        total_count = await self.user_api_key_repository.count(
            **search_params.model_dump(
                exclude_none=True,
                exclude={"limit", "offset", "sorted_by", "sorted_order"},
            ),
            user_id=user_id,
        )
        return UserApiKeyListRead(
            meta=ListResponseMeta(
                total_count=total_count,
                **search_params.model_dump(exclude_none=True),
            ),
            data=[UserApiKeyRead.model_validate(tx) for tx in user_api_keys],
        )

    async def create(
        self, user_id: UUID, user_api_key_create: UserApiKeyCreate
    ) -> UserApiKeyRead:
        """
        Create a new user API key.
        """
        api_key = API_KEY_PREFIX + secrets.token_urlsafe(32)
        user_api_key = await self.user_api_key_repository.create(
            user_id=user_id, api_key=api_key, **user_api_key_create.model_dump()
        )
        return UserApiKeyRead.model_validate(user_api_key)

    async def update(
        self, user_api_key_id: int, user_api_key_update: UserApiKeyUpdate
    ) -> UserApiKeyRead:
        """
        Update an existing user API key.
        """
        user_api_key = await self.user_api_key_repository.update(
            id=user_api_key_id, **user_api_key_update.model_dump()
        )
        return UserApiKeyRead.model_validate(user_api_key)

    async def delete(self, user_api_key_id: int) -> None:
        """
        Delete a user API key.
        """
        await self.user_api_key_repository.soft_delete(id=user_api_key_id)
