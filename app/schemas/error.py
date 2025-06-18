from pydantic import BaseModel
from typing import List, Optional


class ErrorSource(BaseModel):
    parameter: Optional[str] = None  # e.g. "#/title"


class ErrorDetail(BaseModel):
    status: str
    code: str
    title: str
    detail: str
    source: Optional[ErrorSource] = None


class ErrorResponse(BaseModel):
    type: str = "about:blank"
    title: str
    status: int
    instance: str
    errors: List[ErrorDetail]
