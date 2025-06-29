from app.v1.repositories.user_repository import UserRepository
from app.v1.repositories.user_organization_assignment_repository import (
    UserOrganizationAssignmentRepository,
)

from app.v1.schemas.organization.users.search_params import (
    OrganizationUserSearchParams,
)
from app.v1.schemas.common.list.base_list_response import ListResponseMeta
from app.v1.schemas.organization.users.read_list import UserListRead
from app.v1.schemas.user.read import UserRead
from datetime import datetime, timezone
from app.lib.exception.api_exception import init_api_exception
from fastapi import status
from app.lib.error_code import ErrorCode


class OrganizationUserService:
    def __init__(
        self,
        user_repository: UserRepository,
        user_organization_assignment_repository: UserOrganizationAssignmentRepository,
    ):
        self.user_repository = user_repository
        self.user_organization_assignment_repository = (
            user_organization_assignment_repository
        )

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

    async def get(self, organization_id: int, user_id: str) -> UserRead:
        user = await self.user_repository.find_by_or_raise(
            id=user_id,
            user_organization_assignments__organization_id__exact=organization_id,
        )
        return UserRead.model_validate(user)

    async def delete(self, organization_id: int, user_id: str) -> None:
        user_organization_assignment = (
            await self.user_organization_assignment_repository.find_by_or_raise(
                user_id=user_id,
                organization_id=organization_id,
            )
        )
        # check if last one user in organization
        count = await self.user_organization_assignment_repository.count(
            organization_id=organization_id,
        )
        if count <= 1:
            raise init_api_exception(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail_code=ErrorCode.ORGANIZATION_LAST_USER_CANNOT_BE_DELETED,
            )
        await self.user_organization_assignment_repository.update(
            user_organization_assignment.id, deleted_at=datetime.now(timezone.utc)
        )
        return None
