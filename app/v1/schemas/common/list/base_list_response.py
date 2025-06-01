from pydantic import BaseModel
from app.v1.schemas.common.list.list_response_meta import ListResponseMeta


class BaseListResponse(BaseModel):
    meta: ListResponseMeta
