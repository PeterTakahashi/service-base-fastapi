from pydantic import BaseModel
from typing import List, Optional


class ErrorSource(BaseModel):
    pointer: Optional[str] = None  # e.g. "/title"


class ErrorDetail(BaseModel):
    status: str
    code: str
    title: str
    detail: str
    source: Optional[ErrorSource] = None


class ErrorResponse(BaseModel):
    errors: List[ErrorDetail]
