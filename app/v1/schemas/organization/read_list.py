from typing import List
from app.v1.schemas.common.list.base_list_response import BaseListResponse
from app.v1.schemas.organization.read import OrganizationRead

class OrganizationListRead(BaseListResponse):
    data: List[OrganizationRead]
