from fastapi import APIRouter as FastAPIRouter, status
from app.lib.utils.openapi_response_type import openapi_response_type
from app.schemas.api_exception_openapi_example import APIExceptionOpenAPIExample
from app.lib.error_code import ErrorCode


class APIRouter(FastAPIRouter):

    def get_full_path(self, path: str) -> str:
        if not self.prefix:
            return path
        return f"{self.prefix.rstrip('/')}{path}"

    def add_api_route(self, path: str, endpoint, *, responses=None, **kwargs):
        full_path = self.get_full_path(path)

        default_responses = {
            status.HTTP_422_UNPROCESSABLE_ENTITY: openapi_response_type(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                request_path=full_path,
                description="Validation error.",
                api_exception_openapi_examples=[
                    APIExceptionOpenAPIExample(
                        detail_code=ErrorCode.VALIDATION_ERROR,
                        pointer="body",
                    ),
                ],
            )
        }

        merged = {**default_responses, **(responses or {})}
        super().add_api_route(path, endpoint, responses=merged, **kwargs)
