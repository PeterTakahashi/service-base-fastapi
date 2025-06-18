from fastapi import APIRouter, Depends, Request, status, HTTPException

from fastapi_users import exceptions, models, schemas
from fastapi_users.manager import BaseUserManager, UserManagerDependency
from app.lib.error_code import ErrorCode
from app.lib.schemas.error import ErrorResponse

from app.v1.schemas.user import UserRead, UserCreate

from app.v1.exception_handlers.unprocessable_entity_exception_handler import (
    unprocessable_entity_json_content,
)


def get_register_router(
    get_user_manager: UserManagerDependency[models.UP, models.ID],
    user_schema=UserRead,
    user_create_schema=UserCreate,
) -> APIRouter:
    """Generate a router with the register route."""
    router = APIRouter()

    @router.post(
        "/register",
        response_model=user_schema,
        status_code=status.HTTP_201_CREATED,
        name="register:register",
        responses={
            status.HTTP_422_UNPROCESSABLE_ENTITY: {
                "model": ErrorResponse,
                "content": {
                    "application/json": {
                        "examples": {
                            ErrorCode.REGISTER_USER_ALREADY_EXISTS: {
                                "summary": "A user with this email already exists.",
                                "value": unprocessable_entity_json_content(
                                    instance="http://127.0.0.1:8000/app/v1/auth/register/register",
                                    errors=[
                                        {
                                            "code": ErrorCode.REGISTER_USER_ALREADY_EXISTS,
                                            "title": "User Already Exists",
                                            "detail": "A user with this email already exists.",
                                            "source": {"pointer": "#/email"},
                                        }
                                    ],
                                ),
                            },
                            ErrorCode.REGISTER_INVALID_PASSWORD: {
                                "summary": "Password validation failed.",
                                "value": unprocessable_entity_json_content(
                                    instance="http://127.0.0.1:8000/app/v1/auth/register/register",
                                    errors=[
                                        {
                                            "code": ErrorCode.REGISTER_INVALID_PASSWORD,
                                            "title": "Invalid Password",
                                            "detail": "Password must be at least 8 characters long",
                                            "source": {"pointer": "#/password"},
                                        }
                                    ],
                                ),
                            },
                        }
                    }
                },
            },
        },
    )
    async def register(
        request: Request,
        user_create: user_create_schema,  # type: ignore
        user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
    ):
        try:
            created_user = await user_manager.create(
                user_create, safe=True, request=request
            )
        except exceptions.UserAlreadyExists:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=unprocessable_entity_json_content(
                    instance=str(request.url),
                    errors=[
                        {
                            "code": ErrorCode.REGISTER_USER_ALREADY_EXISTS,
                            "title": "User Already Exists",
                            "detail": "A user with this email already exists.",
                            "source": {"pointer": "#/email"},
                        }
                    ],
                ),
            )
        except exceptions.InvalidPasswordException as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=unprocessable_entity_json_content(
                    instance=str(request.url),
                    errors=[
                        {
                            "code": ErrorCode.REGISTER_INVALID_PASSWORD,
                            "title": "Invalid Password",
                            "detail": e.reason,
                            "source": {"pointer": "#/password"},
                        }
                    ],
                ),
            )

        return schemas.model_validate(user_schema, created_user)

    return router
