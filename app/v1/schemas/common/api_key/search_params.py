from typing import Optional
from datetime import datetime
from app.v1.schemas.common.list.base_search_params import BaseSearchParams


class ApiKeySearchParams(BaseSearchParams):
    name__icontains: Optional[str] = None
    api_key__icontains: Optional[str] = None
    expires_at__gte: Optional[datetime] = None
    expires_at__lte: Optional[datetime] = None
    allowed_origin__icontains: Optional[str] = None
    allowed_ip__icontains: Optional[str] = None
    created_at__gte: Optional[datetime] = None
    created_at__lte: Optional[datetime] = None
    updated_at__gte: Optional[datetime] = None
    updated_at__lte: Optional[datetime] = None
