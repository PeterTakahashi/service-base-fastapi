from fastapi import status
from app.lib.error_code import ErrorCode

from app.lib.utils.openapi_response_type import openapi_response_type
from app.schemas.api_exception_openapi_example import APIExceptionOpenAPIExample

UPDATE_USER_RESPONSES = {
    status.HTTP_422_UNPROCESSABLE_ENTITY: openapi_response_type(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        request_path="/app/v1/users/me",
        api_exception_openapi_examples=[
            APIExceptionOpenAPIExample(
                detail_code=ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS,
                pointer="email",
            ),
            APIExceptionOpenAPIExample(
                detail_code=ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                pointer="password",
            ),
        ],
    ),
}
