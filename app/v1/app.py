from fastapi import FastAPI
from app.v1.routers import api as api_router
from app.core.config import settings
from app.v1.exception_handlers.http_exception_handler import http_exception_handler
from app.v1.exception_handlers.server_exception_handler import server_exception_handler
from app.v1.exception_handlers.no_result_found_exception_handler import (
    no_result_found_exception_handler,
)
from app.v1.exception_handlers.validation_exception_handler import (
    validation_exception_handler,
)

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import NoResultFound

from app.lib.exception.http.api_exception import APIException
from app.lib.exception_handlers.api_exception_handler import api_exception_handler

v1_app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Version 1 of the  FastAPI Applicatoin",
    version="1.0.0",
)

v1_app.include_router(api_router.api_router)

v1_app.add_exception_handler(
    StarletteHTTPException, http_exception_handler  # type: ignore
)
v1_app.add_exception_handler(Exception, server_exception_handler)  # type: ignore
v1_app.add_exception_handler(
    RequestValidationError, validation_exception_handler  # type: ignore
)

v1_app.add_exception_handler(NoResultFound, no_result_found_exception_handler)  # type: ignore

v1_app.add_exception_handler(APIException, api_exception_handler)  # type: ignore
