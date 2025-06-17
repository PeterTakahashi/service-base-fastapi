from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.i18n import get_locale, get_message


def unauthorized_exception_handler(request: Request, exc: StarletteHTTPException):
    locale = get_locale(request)
    code = exc.detail.get("code") if isinstance(exc.detail, dict) else "unauthorized"
    instance = str(request.url)
    return JSONResponse(
        status_code=401,
        content={
            "type": "about:blank",
            "title": "Unauthorized",
            "status": status.HTTP_401_UNAUTHORIZED,
            "instance": instance,
            "errors": [
                {
                    "status": "401",
                    "code": code,
                    "title": get_message(locale, code, "title"),
                    "detail": get_message(locale, code, "detail"),
                }
            ],
        },
    )
