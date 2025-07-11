from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from app.schemas.error import ErrorDetail, ErrorSource

from app.lib.exception.api_exception import APIException
from app.core.exception_handlers.api_exception_handler import api_exception_handler
from app.lib.error_code import ErrorCode
from app.lib.utils.i18n import get_message, get_locale
from typing import List


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_details: List[ErrorDetail] = []
    locale = get_locale(request)

    for error in exc.errors():
        pointer = None
        detail_code = ErrorCode.VALIDATION_ERROR
        if error["loc"][0] == "body":
            pointer = "#/" + "/".join(str(loc) for loc in error["loc"][1:])
        elif error["loc"][0] == "query":
            pointer = "#/" + "/".join(str(loc) for loc in error["loc"][1:])
        elif error["loc"][0] == "path":
            pointer = "#/" + "/".join(str(loc) for loc in error["loc"][1:])
        else:
            pointer = "#/" + "/".join(str(loc) for loc in error["loc"])

        detail = error.get("ctx", {}).get("reason")
        if detail is None:
            detail = error.get("msg", "")

        error_details.append(
            ErrorDetail(
                status=str(status.HTTP_422_UNPROCESSABLE_ENTITY),
                code=detail_code,
                title=get_message(locale, detail_code, "title"),
                detail=detail,
                source=ErrorSource(pointer=pointer) if pointer else None,
            )
        )
    api_exception = APIException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error_details=error_details,
    )
    return await api_exception_handler(request, api_exception)
