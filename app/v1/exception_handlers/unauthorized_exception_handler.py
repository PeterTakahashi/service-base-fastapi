from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.lib.i18n import get_message, get_locale


def unauthorized_json_content(code: str, instance: str, locale: str = "en"):
    return {
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
                "source": None,
            }
        ],
    }


def unauthorized_exception_handler(request: Request, exc: StarletteHTTPException):
    if isinstance(exc.detail, dict):
        content = exc.detail
    elif isinstance(exc.detail, str):
        code = exc.detail.lower() if exc.detail else "unauthorized"
        content = unauthorized_json_content(
            code=code, instance=str(request.url), locale=get_locale(request)
        )
    return JSONResponse(
        status_code=401,
        content=content,
    )
