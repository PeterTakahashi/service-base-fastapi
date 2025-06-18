from fastapi import APIRouter, Body, Depends, Request, status
from pydantic import EmailStr

from fastapi_users import exceptions, models, schemas
from fastapi_users.manager import BaseUserManager, UserManagerDependency
from app.lib.error_code import ErrorCode
from app.v1.schemas.user import UserRead

from app.lib.exception.http.api_exception import APIException
from app.lib.openapi_response_type import openapi_response_type
from app.lib.schemas.api_exception_openapi_example import APIExceptionOpenAPIExample
from app.lib.schemas.openapi import OpenAPIResponseType

VERIFY_RESPONSES: OpenAPIResponseType = {
    status.HTTP_400_BAD_REQUEST: openapi_response_type(
        status_code=status.HTTP_400_BAD_REQUEST,
        description="Bad token.",
        request_path="/auth/verify",
        api_exception_openapi_examples=[
            APIExceptionOpenAPIExample(detail_code=ErrorCode.VERIFY_USER_BAD_TOKEN),
            APIExceptionOpenAPIExample(
                detail_code=ErrorCode.VERIFY_USER_ALREADY_VERIFIED,
            ),
        ],
    ),
}


def get_verify_router(
    get_user_manager: UserManagerDependency[models.UP, models.ID],
    user_schema=UserRead,
):
    router = APIRouter()

    @router.post(
        "/request-verify-token",
        status_code=status.HTTP_202_ACCEPTED,
        name="verify:request-token",
    )
    async def request_verify_token(
        request: Request,
        email: EmailStr = Body(..., embed=True),
        user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
    ):
        try:
            user = await user_manager.get_by_email(email)
            await user_manager.request_verify(user, request)
        except (
            exceptions.UserNotExists,
            exceptions.UserInactive,
            exceptions.UserAlreadyVerified,
        ):
            pass

        return None

    @router.post(
        "/verify",
        response_model=user_schema,
        name="verify:verify",
        responses=VERIFY_RESPONSES,
    )
    async def verify(
        request: Request,
        token: str = Body(..., embed=True),
        user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
    ):
        try:
            user = await user_manager.verify(token, request)
            return schemas.model_validate(user_schema, user)
        except (exceptions.InvalidVerifyToken, exceptions.UserNotExists):
            raise APIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail_code=ErrorCode.VERIFY_USER_BAD_TOKEN,
            )
        except exceptions.UserAlreadyVerified:
            raise APIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail_code=ErrorCode.VERIFY_USER_ALREADY_VERIFIED,
            )

    return router
