from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class BaseSearchParams(BaseModel):
    limit: int = Field(100, ge=1, description="Maximum number of items to retrieve")
    offset: int = Field(0, ge=0, description="Starting position for retrieval")
    sorted_by: Optional[str] = Field(None, description="Field name to sort by")
    sorted_order: str = Field("asc", description="Sort order: asc or desc")

    model_config = ConfigDict(from_attributes=True)
