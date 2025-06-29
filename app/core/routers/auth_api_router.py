from fastapi import status
from app.lib.utils.openapi_response_type import openapi_response_type
from app.schemas.api_exception_openapi_example import APIExceptionOpenAPIExample
from app.lib.error_code import ErrorCode
from app.core.routers.base_router import BaseRouter


class AuthAPIRouter(BaseRouter):

    def get_default_responses(self, request_path: str) -> dict:
        return {
            status.HTTP_401_UNAUTHORIZED: openapi_response_type(
                status_code=status.HTTP_401_UNAUTHORIZED,
                request_path=request_path,
                description="Unauthorized access.",
                api_exception_openapi_examples=[
                    APIExceptionOpenAPIExample(detail_code=ErrorCode.UNAUTHORIZED)
                ],
            )
        }
