from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import datetime

class EpisodeRead(BaseModel):
    id: UUID = Field(..., validation_alias='display_id')
    title: str
    created_at: datetime
    updated_at: datetime
    product_id: UUID = Field(..., validation_alias='product_display_id')

    model_config = ConfigDict(from_attributes=True)
