from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


def unprocessable_entity_exception_handler(
    request: Request, exc: StarletteHTTPException
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=exc.detail
    )
