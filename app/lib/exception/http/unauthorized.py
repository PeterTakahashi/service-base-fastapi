from app.core.response_type import unauthorized_detail
from fastapi import HTTPException, status


def HTTPExceptionUnauthorized(code: str = "unauthorized"):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=unauthorized_detail(code=code),
    )
