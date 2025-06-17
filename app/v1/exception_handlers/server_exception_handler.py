from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.lib.i18n import get_locale, get_message
from starlette.exceptions import HTTPException


async def server_exception_handler(request: Request, exc: Exception | HTTPException):
    locale = get_locale(request)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "errors": [
                {
                    "status": "500",
                    "code": "internal_server_error",
                    "title": get_message(locale, "internal_server_error", "title"),
                    "detail": get_message(locale, "internal_server_error", "detail"),
                }
            ]
        },
    )
