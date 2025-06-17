from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


def bad_request_exception_handler(request: Request, exc: StarletteHTTPException):
    if isinstance(exc.detail, str):
        content = {"detail": exc.detail}
    elif isinstance(exc.detail, dict):
        content = exc.detail
    else:
        content = {"detail": "Bad Request"}
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=content,
    )
