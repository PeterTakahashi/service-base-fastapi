from typing import List
from app.v1.schemas.common.list.base_list_response import BaseListResponse
from app.v1.schemas.user.read import UserRead


class UserListRead(BaseListResponse):
    data: List[UserRead]
