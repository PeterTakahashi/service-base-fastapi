from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import NoResultFound

from app.core.i18n import get_locale, get_message


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    locale = get_locale(request)
    if exc.status_code == 401:
        code = (
            exc.detail.get("code") if isinstance(exc.detail, dict) else "unauthorized"
        )
        return JSONResponse(
            status_code=401,
            content={
                "errors": [
                    {
                        "status": "401",
                        "code": code,
                        "title": get_message(locale, "unauthorized", "title"),
                        "detail": get_message(locale, "unauthorized", "detail"),
                    }
                ]
            },
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def server_exception_handler(request: Request, exc: Exception):
    locale = get_locale(request)
    return JSONResponse(
        status_code=500,
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


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    locale = get_locale(request)
    errors = []

    for e in exc.errors():
        parameter = "/".join(str(loc) for loc in e["loc"] if loc != "body")

        errors.append(
            {
                "status": "422",
                "code": "validation_error",
                "title": get_message(locale, "validation_error", "title"),
                "detail": e["msg"],
                "source": {"parameter": parameter},
            }
        )

    return JSONResponse(status_code=422, content={"errors": errors})


async def no_result_found_exception_handler(request: Request, exc: NoResultFound):
    locale = get_locale(request)
    return JSONResponse(
        status_code=404,
        content={
            "errors": [
                {
                    "status": "404",
                    "code": "not_found",
                    "title": get_message(locale, "not_found", "title"),
                    "detail": get_message(locale, "not_found", "detail"),
                }
            ]
        },
    )
