from app.v1.repositories.user_repository import UserRepository

from app.v1.schemas.organization.users.search_params import (
    OrganizationUserSearchParams,
)
from app.v1.schemas.common.list.base_list_response import ListResponseMeta
from app.v1.schemas.organization.users.read_list import UserListRead
from app.v1.schemas.user.read import UserRead


class OrganizationUserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_list(
        self, organization_id: int, search_params: OrganizationUserSearchParams
    ) -> UserListRead:
        users = await self.user_repository.where(
            **search_params.model_dump(exclude_none=True),
            user_organization_assignments__organization_id__exact=organization_id,
        )
        total_count = await self.user_repository.count(
            **search_params.model_dump(
                exclude_none=True,
                exclude={"limit", "offset", "sorted_by", "sorted_order"},
            ),
            user_organization_assignments__organization_id__exact=organization_id,
        )
        return UserListRead(
            meta=ListResponseMeta(
                total_count=total_count,
                **search_params.model_dump(exclude_none=True),
            ),
            data=[UserRead.model_validate(tx) for tx in users],
        )

    async def get(
        self, organization_id: int, user_id: str
    ) -> UserRead:
        user = await self.user_repository.find_by_or_raise(
            id=user_id,
            user_organization_assignments__organization_id__exact=organization_id,
        )
        return UserRead.model_validate(user)