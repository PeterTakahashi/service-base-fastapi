from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import NoResultFound

from app.core.i18n import get_locale, get_message


def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 401:
        return unauthorized_exception_handler(request, exc)
    elif exc.status_code == 400:
        return bad_request_exception_handler(request, exc)
    elif exc.status_code == 422:
        return unprocessable_entity_exception_handler(request, exc)
    else:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )


def unauthorized_exception_handler(request: Request, exc: StarletteHTTPException):
    locale = get_locale(request)
    code = exc.detail.get("code") if isinstance(exc.detail, dict) else "unauthorized"
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

def unprocessable_entity_exception_handler(request: Request, exc: StarletteHTTPException):
    locale = get_locale(request)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=exc.detail
    )


def bad_request_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.detail},
    )


async def server_exception_handler(request: Request, exc: Exception):
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
