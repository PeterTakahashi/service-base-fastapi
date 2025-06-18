from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import NoResultFound

from app.lib.exception.api_exception import APIException
from app.lib.exception_handlers.api_exception_handler import api_exception_handler
from app.lib.error_code import ErrorCode


async def no_result_found_exception_handler(
    request: Request, exc: NoResultFound
) -> JSONResponse:
    api_exception = APIException.init_with_detail(
        status_code=status.HTTP_404_NOT_FOUND, detail_code=ErrorCode.NOT_FOUND
    )
    return await api_exception_handler(request, api_exception)
