from fastapi import HTTPException, status, Request
from app.v1.exception_handlers.unauthorized_exception_handler import (
    unauthorized_json_content,
)
from app.core.i18n import get_locale


def HTTPExceptionUnauthorized(request: Request, code: str = "unauthorized"):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=unauthorized_json_content(
            code=code,
            instance=str(request.url),
            locale=get_locale(request),
        ),
    )
