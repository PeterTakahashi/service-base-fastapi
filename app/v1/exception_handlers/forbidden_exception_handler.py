from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.lib.i18n import get_locale, get_message


def forbidden_json_content(code: str, instance: str, locale: str = "en"):
    return {
        "type": "about:blank",
        "title": "Forbidden",
        "status": status.HTTP_403_FORBIDDEN,
        "instance": instance,
        "errors": [
            {
                "status": "403",
                "code": code,
                "title": get_message(locale, code, "title"),
                "detail": get_message(locale, code, "detail"),
            }
        ],
    }


def forbidden_exception_handler(request: Request, exc: StarletteHTTPException):
    if isinstance(exc.detail, dict):
        content = exc.detail
    elif isinstance(exc.detail, str):
        code = exc.detail.lower() if exc.detail else "forbidden"
        content = forbidden_json_content(
            code=code, instance=str(request.url), locale=get_locale(request)
        )
    return JSONResponse(
        status_code=403,
        content=content,
    )
