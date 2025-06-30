from typing import List
from app.v1.schemas.common.list.base_list_response import BaseListResponse
from app.v1.schemas.common.api_key.read import ApiKeyRead


class ApiKeyListRead(BaseListResponse):
    data: List[ApiKeyRead]
