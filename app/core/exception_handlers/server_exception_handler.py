from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.lib.exception.api_exception import init_api_exception
from app.core.exception_handlers.api_exception_handler import api_exception_handler
from app.lib.error_code import ErrorCode


async def server_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    api_exception = init_api_exception(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail_code=ErrorCode.INTERNAL_SERVER_ERROR,
    )
    return await api_exception_handler(request, api_exception)
