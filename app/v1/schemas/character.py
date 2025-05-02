from pydantic import BaseModel, ConfigDict
from datetime import datetime


class CharacterRead(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    product_id: int

    model_config = ConfigDict(from_attributes=True)
