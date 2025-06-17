from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.v1.exception_handlers.responses.unprocessable_entity_json_response import (
    unprocessable_entity_json_content,
)
from app.core.i18n import get_locale


def unprocessable_entity_exception_handler(
    request: Request, exc: StarletteHTTPException
):
    if isinstance(exc.detail, dict):
        content = exc.detail
    elif isinstance(exc.detail, str):
        code = exc.detail.lower() if exc.detail else "unprocessable_entity"
        content = unprocessable_entity_json_content(
            code=code, instance=str(request.url), locale=get_locale(request)
        )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=content
    )
