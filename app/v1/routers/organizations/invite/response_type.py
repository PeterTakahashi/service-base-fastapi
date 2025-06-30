from fastapi import status
from app.lib.utils.openapi_response_type import openapi_response_type
from app.schemas.api_exception_openapi_example import APIExceptionOpenAPIExample
from app.lib.error_code import ErrorCode
from app.schemas.openapi import OpenAPIResponseType

INVITE_RESPONSES: OpenAPIResponseType = {
    status.HTTP_400_BAD_REQUEST: openapi_response_type(
        status_code=status.HTTP_400_BAD_REQUEST,
        description="Bad Request",
        request_path="/organizations/{organization_id}/invite",
        api_exception_openapi_examples=[
            APIExceptionOpenAPIExample(
                detail_code=ErrorCode.USER_ORGANIZATION_INVITATION_NOT_FOUND
            ),
            APIExceptionOpenAPIExample(
                detail_code=ErrorCode.USER_ORGANIZATION_INVITATION_EXPIRED
            ),
            APIExceptionOpenAPIExample(
                detail_code=ErrorCode.USER_ORGANIZATION_INVITATION_ALREADY_ASSIGNED
            ),
        ],
    ),
}
