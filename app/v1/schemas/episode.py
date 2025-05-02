from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import datetime


class EpisodeRead(BaseModel):
    id: UUID
    title: str
    created_at: datetime
    updated_at: datetime
    product_id: UUID

    model_config = ConfigDict(from_attributes=True)
