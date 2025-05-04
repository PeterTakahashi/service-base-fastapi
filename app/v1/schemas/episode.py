from datetime import datetime
from app.v1.schemas.base import HasEncodedID


class EpisodeRead(HasEncodedID):
    title: str
    created_at: datetime
    updated_at: datetime
    product_id: int
