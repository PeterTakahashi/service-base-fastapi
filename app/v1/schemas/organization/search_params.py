from typing import Optional
from datetime import datetime
from app.v1.schemas.common.list.base_search_params import BaseSearchParams


class OrganizationSearchParams(BaseSearchParams):
    name__icontains: Optional[str] = None
    description__icontains: Optional[str] = None
    billing_email__icontains: Optional[str] = None
    created_at__gte: Optional[datetime] = None
    created_at__lte: Optional[datetime] = None
    updated_at__gte: Optional[datetime] = None
    updated_at__lte: Optional[datetime] = None
