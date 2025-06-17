from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.v1.exception_handlers.unauthorized_exception_handler import (
    unauthorized_exception_handler,
)
from app.v1.exception_handlers.bad_request_exception_handler import (
    bad_request_exception_handler,
)
from app.v1.exception_handlers.unprocessable_entity_exception_handler import (
    unprocessable_entity_exception_handler,
)
from app.v1.exception_handlers.server_exception_handler import (
    server_exception_handler,
)


def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 401:
        return unauthorized_exception_handler(request, exc)
    elif exc.status_code == 400:
        return bad_request_exception_handler(request, exc)
    elif exc.status_code == 422:
        return unprocessable_entity_exception_handler(request, exc)
    elif exc.status_code == 500:
        return server_exception_handler(request, exc)
    else:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
