from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
from pydantic import EmailStr

from fastapi_users import exceptions, models
from fastapi_users.manager import BaseUserManager, UserManagerDependency
from fastapi_users.openapi import OpenAPIResponseType
from fastapi_users.router.common import ErrorCode, ErrorModel
from app.v1.exception_handlers.unprocessable_entity_exception_handler import (
    unprocessable_entity_json_content,
)
from app.v1.exception_handlers.bad_request_exception_handler import (
    bad_request_json_content,
)

RESET_PASSWORD_RESPONSES: OpenAPIResponseType = {
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.RESET_PASSWORD_BAD_TOKEN: {
                        "summary": "Bad or expired token.",
                        "value": bad_request_json_content(
                            code=ErrorCode.RESET_PASSWORD_BAD_TOKEN.lower(),
                            instance="http://127.0.0.1:8000/app/v1/auth/reset-password",
                        ),
                    },
                }
            }
        },
    },
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.RESET_PASSWORD_INVALID_PASSWORD: {
                        "summary": "Password validation failed.",
                        "value": unprocessable_entity_json_content(
                            instance="http://127.0.0.1:8000/app/v1/auth/reset-password",
                            errors=[
                                {
                                    "code": ErrorCode.RESET_PASSWORD_INVALID_PASSWORD.lower(),
                                    "title": "Invalid Password",
                                    "detail": "Password should be at least 3 characters",
                                    "source": {"pointer": "#/password"},
                                }
                            ],
                        ),
                    }
                }
            }
        },
    },
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
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.RESET_PASSWORD_BAD_TOKEN,
            )
        except exceptions.InvalidPasswordException as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=unprocessable_entity_json_content(
                    instance=str(request.url),
                    errors=[
                        {
                            "code": ErrorCode.RESET_PASSWORD_INVALID_PASSWORD.lower(),
                            "title": "Invalid Password",
                            "detail": e.reason,
                            "source": {"pointer": "#/password"},
                        }
                    ],
                ),
            )

    return router
