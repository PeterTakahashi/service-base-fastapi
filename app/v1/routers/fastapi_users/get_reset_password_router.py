from fastapi import APIRouter, Body, Depends, Request, status
from pydantic import EmailStr

from fastapi_users import exceptions, models
from fastapi_users.manager import BaseUserManager, UserManagerDependency
from app.lib.schemas.openapi import OpenAPIResponseType
from app.lib.error_code import ErrorCode
from app.lib.exception.http.api_exception import APIException
from app.lib.openapi_response_type import openapi_response_type
from app.lib.schemas.api_exception_openapi_example import APIExceptionOpenAPIExample


RESET_PASSWORD_RESPONSES: OpenAPIResponseType = {
    status.HTTP_400_BAD_REQUEST: openapi_response_type(
        status_code=status.HTTP_400_BAD_REQUEST,
        description="Bad token.",
        request_path="/auth/reset-password",
        api_exception_openapi_examples=[
            APIExceptionOpenAPIExample(detail_code=ErrorCode.RESET_PASSWORD_BAD_TOKEN),
        ],
    ),
    status.HTTP_422_UNPROCESSABLE_ENTITY: openapi_response_type(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        description="",
        request_path="/auth/reset-password",
        api_exception_openapi_examples=[
            APIExceptionOpenAPIExample(
                detail_code=ErrorCode.RESET_PASSWORD_INVALID_PASSWORD,
                parameter="password",
            ),
        ],
    ),
}


def get_reset_password_router(
    get_user_manager: UserManagerDependency[models.UP, models.ID],
) -> APIRouter:
    """Generate a router with the reset password routes."""
    router = APIRouter()

    @router.post(
        "/forgot-password",
        status_code=status.HTTP_202_ACCEPTED,
        name="reset:forgot_password",
    )
    async def forgot_password(
        request: Request,
        email: EmailStr = Body(..., embed=True),
        user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
    ):
        try:
            user = await user_manager.get_by_email(email)
        except exceptions.UserNotExists:
            return None

        try:
            await user_manager.forgot_password(user, request)
        except exceptions.UserInactive:
            pass

        return None

    @router.post(
        "/reset-password",
        name="reset:reset_password",
        responses=RESET_PASSWORD_RESPONSES,
    )
    async def reset_password(
        request: Request,
        token: str = Body(...),
        password: str = Body(...),
        user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
    ):
        try:
            await user_manager.reset_password(token, password, request)
        except (
            exceptions.InvalidResetPasswordToken,
            exceptions.UserNotExists,
            exceptions.UserInactive,
        ):
            raise APIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail_code=ErrorCode.RESET_PASSWORD_BAD_TOKEN,
            )
        except exceptions.InvalidPasswordException as e:
            raise APIException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail_code=ErrorCode.RESET_PASSWORD_INVALID_PASSWORD,
                detail_detail=e.reason,
                parameter="password",
            )

    return router
