from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.lib.exception.api_exception import APIException
from app.lib.exception_handlers.api_exception_handler import api_exception_handler
from app.lib.error_code import ErrorCode


async def server_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    api_exception = APIException.init_with_detail(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail_code=ErrorCode.INTERNAL_SERVER_ERROR,
    )
    return await api_exception_handler(request, api_exception)
