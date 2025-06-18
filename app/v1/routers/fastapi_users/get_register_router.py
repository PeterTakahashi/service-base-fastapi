from fastapi import APIRouter, Depends, Request, status

from fastapi_users import exceptions, models, schemas
from fastapi_users.manager import BaseUserManager, UserManagerDependency
from app.lib.error_code import ErrorCode

from app.v1.schemas.user import UserRead, UserCreate

from app.lib.exception.api_exception import APIException
from app.lib.openapi_response_type import openapi_response_type
from app.lib.schemas.api_exception_openapi_example import APIExceptionOpenAPIExample


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
            status.HTTP_422_UNPROCESSABLE_ENTITY: openapi_response_type(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description="",
                request_path="/app/v1/auth/register/register",
                api_exception_openapi_examples=[
                    APIExceptionOpenAPIExample(
                        detail_code=ErrorCode.REGISTER_USER_ALREADY_EXISTS,
                        parameter="email",
                    ),
                    APIExceptionOpenAPIExample(
                        detail_code=ErrorCode.REGISTER_INVALID_PASSWORD,
                        parameter="password",
                    ),
                ],
            )
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
            raise APIException.init_with_detail(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail_code=ErrorCode.REGISTER_USER_ALREADY_EXISTS,
                parameter="email",
            )
        except exceptions.InvalidPasswordException as e:
            raise APIException.init_with_detail(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail_code=ErrorCode.REGISTER_INVALID_PASSWORD,
                detail_detail=e.reason,
                parameter="password",
            )

        return schemas.model_validate(user_schema, created_user)

    return router
