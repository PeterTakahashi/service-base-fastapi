from app.v1.schemas.common.list.base_search_params import BaseSearchParams
from pydantic import Field


class ListResponseMeta(BaseSearchParams):
    total_count: int = Field(
        ...,
        description="Total number of items matching the search criteria.",
        json_schema_extra={"example": 100},
    )
