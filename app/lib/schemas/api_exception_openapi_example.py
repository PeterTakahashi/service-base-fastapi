from pydantic import BaseModel
from typing import Optional


class APIExceptionOpenAPIExample(BaseModel):
    detail_code: str
    detail_title: Optional[str] = None
    detail_detail: Optional[str] = None
    parameter: Optional[str] = None
