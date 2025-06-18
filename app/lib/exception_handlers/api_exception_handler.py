from fastapi import Request
from fastapi.responses import JSONResponse
from app.lib.exception.api_exception import APIException


async def api_exception_handler(request: Request, exc: APIException) -> JSONResponse:
    content = exc.to_error_response(request).model_dump()
    return JSONResponse(status_code=exc.status_code, content=content)
