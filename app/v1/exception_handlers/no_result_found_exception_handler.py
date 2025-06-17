from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import NoResultFound

from app.lib.i18n import get_locale, get_message


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
