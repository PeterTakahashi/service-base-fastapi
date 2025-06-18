from fastapi import Request
from fastapi.exceptions import HTTPException
from app.lib.exception.api_exception import APIException
from app.lib.exception_handlers.api_exception_handler import api_exception_handler
from app.lib.status_code_to_snake_case import status_code_to_snake_case
from fastapi.responses import JSONResponse


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    api_exception = APIException(
        status_code=exc.status_code,
        detail_code=status_code_to_snake_case(exc.status_code),
    )
    return await api_exception_handler(request, api_exception)
