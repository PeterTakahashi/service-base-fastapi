from pydantic import BaseModel
from app.v1.schemas.list_response_meta import ListResponseMeta


class BaseListResponse(BaseModel):
    meta: ListResponseMeta
