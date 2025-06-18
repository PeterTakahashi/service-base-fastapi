from fastapi import APIRouter, status
from app.lib.utils.openapi_response_type import openapi_response_type
from app.schemas.api_exception_openapi_example import APIExceptionOpenAPIExample
from app.lib.error_code import ErrorCode


class AuthAPIRouter(APIRouter):

    def get_full_path(self, path: str) -> str:
        if not self.prefix:
            return path
        return f"{self.prefix.rstrip('/')}{path}"

    def add_api_route(self, path: str, endpoint, *, responses=None, **kwargs):
        full_path = self.get_full_path(path)

        default_401 = {
            status.HTTP_401_UNAUTHORIZED: openapi_response_type(
                status_code=status.HTTP_401_UNAUTHORIZED,
                description="Unauthorized access.",
                request_path=full_path,
                api_exception_openapi_examples=[
                    APIExceptionOpenAPIExample(detail_code=ErrorCode.UNAUTHORIZED)
                ],
            )
        }

        merged = {**default_401, **(responses or {})}
        super().add_api_route(path, endpoint, responses=merged, **kwargs)
