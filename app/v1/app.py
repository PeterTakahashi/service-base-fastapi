from fastapi import FastAPI
from app.v1.routers import api as api_router
from app.core.config import settings
from app.v1.openapi import custom_openapi
from app.v1.exception_handlers import (
    http_exception_handler,
    server_exception_handler,
    validation_exception_handler,
)
from app.core.i18n import load_messages
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

load_messages()

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

v1_app.openapi = lambda: custom_openapi(v1_app)  # type: ignore
