from typing import Optional

import jwt
from fastapi import APIRouter, Depends, Query, Request, status
from httpx_oauth.integrations.fastapi import OAuth2AuthorizeCallback
from httpx_oauth.oauth2 import BaseOAuth2, OAuth2Token

from app.lib.exception.api_exception import init_api_exception

from fastapi_users import models, schemas
from fastapi_users.authentication import AuthenticationBackend, Authenticator, Strategy
from fastapi_users.exceptions import UserAlreadyExists
from fastapi_users.jwt import SecretType, decode_jwt
from fastapi_users.manager import BaseUserManager, UserManagerDependency
from app.lib.error_code import ErrorCode
from app.lib.openapi_response_type import openapi_response_type
from app.schemas.api_exception_openapi_example import APIExceptionOpenAPIExample

from fastapi_users.router.oauth import (
    STATE_TOKEN_AUDIENCE,
    OAuth2AuthorizeResponse,
    generate_state_token,
)


def get_oauth_router(
    oauth_client: BaseOAuth2,
    backend: AuthenticationBackend[models.UP, models.ID],
    get_user_manager: UserManagerDependency[models.UP, models.ID],
    state_secret: SecretType,
    redirect_url: Optional[str] = None,
    associate_by_email: bool = False,
    is_verified_by_default: bool = False,
) -> APIRouter:
    """Generate a router with the OAuth routes."""
    router = APIRouter()
    callback_route_name = f"oauth:{oauth_client.name}.{backend.name}.callback"

    if redirect_url is not None:
        oauth2_authorize_callback = OAuth2AuthorizeCallback(
            oauth_client,
            redirect_url=redirect_url,
        )
    else:
        oauth2_authorize_callback = OAuth2AuthorizeCallback(
            oauth_client,
            route_name=callback_route_name,
        )

    @router.get(
        "/authorize",
        name=f"oauth:{oauth_client.name}.{backend.name}.authorize",
        response_model=OAuth2AuthorizeResponse,
    )
    async def authorize(
        request: Request, scopes: list[str] = Query(None)
    ) -> OAuth2AuthorizeResponse:
        if redirect_url is not None:
            authorize_redirect_url = redirect_url
        else:
            authorize_redirect_url = str(request.url_for(callback_route_name))

        state_data: dict[str, str] = {}
        state = generate_state_token(state_data, state_secret)
        authorization_url = await oauth_client.get_authorization_url(
            authorize_redirect_url,
            state,
            scopes,
        )

        return OAuth2AuthorizeResponse(authorization_url=authorization_url)

    @router.get(
        "/callback",
        name=callback_route_name,
        description="The response varies based on the authentication backend used.",
        responses={
            status.HTTP_400_BAD_REQUEST: openapi_response_type(
                status_code=status.HTTP_400_BAD_REQUEST,
                description="Invalid state token or missing email.",
                request_path=f"/auth/cookie/{oauth_client.name}/callback",
                api_exception_openapi_examples=[
                    APIExceptionOpenAPIExample(
                        detail_code=ErrorCode.INVALID_STATE_TOKEN
                    )
                ],
            ),
            status.HTTP_401_UNAUTHORIZED: openapi_response_type(
                status_code=status.HTTP_401_UNAUTHORIZED,
                description="Missing token or inactive user.",
                request_path=f"/auth/cookie/{oauth_client.name}/callback",
                api_exception_openapi_examples=[
                    APIExceptionOpenAPIExample(
                        detail_code=ErrorCode.LOGIN_BAD_CREDENTIALS
                    )
                ],
            ),
            status.HTTP_422_UNPROCESSABLE_ENTITY: openapi_response_type(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description="User already exists.",
                request_path=f"/auth/cookie/{oauth_client.name}/callback",
                api_exception_openapi_examples=[
                    APIExceptionOpenAPIExample(
                        detail_code=ErrorCode.OAUTH_USER_ALREADY_EXISTS
                    )
                ],
            ),
        },
    )
    async def callback(
        request: Request,
        access_token_state: tuple[OAuth2Token, str] = Depends(
            oauth2_authorize_callback
        ),
        user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
        strategy: Strategy[models.UP, models.ID] = Depends(backend.get_strategy),
    ):
        token, state = access_token_state
        account_id, account_email = await oauth_client.get_id_email(
            token["access_token"]
        )

        if account_email is None:
            raise init_api_exception(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail_code=ErrorCode.OAUTH_NOT_AVAILABLE_EMAIL,
            )

        try:
            decode_jwt(state, state_secret, [STATE_TOKEN_AUDIENCE])
        except jwt.DecodeError:
            raise init_api_exception(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail_code=ErrorCode.INVALID_PAYLOAD,
            )

        try:
            user = await user_manager.oauth_callback(
                oauth_client.name,
                token["access_token"],
                account_id,
                account_email,
                token.get("expires_at"),
                token.get("refresh_token"),
                request,
                associate_by_email=associate_by_email,
                is_verified_by_default=is_verified_by_default,
            )
        except UserAlreadyExists:
            raise init_api_exception(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail_code=ErrorCode.OAUTH_USER_ALREADY_EXISTS,
            )

        if not user.is_active:
            raise init_api_exception(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail_code=ErrorCode.LOGIN_BAD_CREDENTIALS,
            )

        # Authenticate
        response = await backend.login(strategy, user)
        await user_manager.on_after_login(user, request, response)
        return response

    return router


def get_oauth_associate_router(
    oauth_client: BaseOAuth2,
    authenticator: Authenticator[models.UP, models.ID],
    get_user_manager: UserManagerDependency[models.UP, models.ID],
    user_schema: type[schemas.U],
    state_secret: SecretType,
    redirect_url: Optional[str] = None,
    requires_verification: bool = False,
) -> APIRouter:
    """Generate a router with the OAuth routes to associate an authenticated user."""
    router = APIRouter()

    get_current_active_user = authenticator.current_user(
        active=True, verified=requires_verification
    )

    callback_route_name = f"oauth-associate:{oauth_client.name}.callback"

    if redirect_url is not None:
        oauth2_authorize_callback = OAuth2AuthorizeCallback(
            oauth_client,
            redirect_url=redirect_url,
        )
    else:
        oauth2_authorize_callback = OAuth2AuthorizeCallback(
            oauth_client,
            route_name=callback_route_name,
        )

    @router.get(
        "/authorize",
        name=f"oauth-associate:{oauth_client.name}.authorize",
        response_model=OAuth2AuthorizeResponse,
    )
    async def authorize(
        request: Request,
        scopes: list[str] = Query(None),
        user: models.UP = Depends(get_current_active_user),
    ) -> OAuth2AuthorizeResponse:
        if redirect_url is not None:
            authorize_redirect_url = redirect_url
        else:
            authorize_redirect_url = str(request.url_for(callback_route_name))

        state_data: dict[str, str] = {"sub": str(user.id)}
        state = generate_state_token(state_data, state_secret)
        authorization_url = await oauth_client.get_authorization_url(
            authorize_redirect_url,
            state,
            scopes,
        )

        return OAuth2AuthorizeResponse(authorization_url=authorization_url)

    @router.get(
        "/callback",
        response_model=user_schema,
        name=callback_route_name,
        description="The response varies based on the authentication backend used.",
        responses={
            status.HTTP_400_BAD_REQUEST: openapi_response_type(
                status_code=status.HTTP_400_BAD_REQUEST,
                description="Invalid state token or missing email.",
                request_path=f"/auth/cookie/{oauth_client.name}/callback",
                api_exception_openapi_examples=[
                    APIExceptionOpenAPIExample(
                        detail_code=ErrorCode.INVALID_STATE_TOKEN
                    )
                ],
            ),
        },
    )
    async def callback(
        request: Request,
        user: models.UP = Depends(get_current_active_user),
        access_token_state: tuple[OAuth2Token, str] = Depends(
            oauth2_authorize_callback
        ),
        user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
    ):
        token, state = access_token_state
        account_id, account_email = await oauth_client.get_id_email(
            token["access_token"]
        )

        if account_email is None:
            raise init_api_exception(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail_code=ErrorCode.OAUTH_NOT_AVAILABLE_EMAIL,
            )

        try:
            state_data = decode_jwt(state, state_secret, [STATE_TOKEN_AUDIENCE])
        except jwt.DecodeError:
            raise init_api_exception(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail_code=ErrorCode.INVALID_PAYLOAD,
            )

        if state_data["sub"] != str(user.id):
            raise init_api_exception(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail_code=ErrorCode.INVALID_PAYLOAD,
            )

        user = await user_manager.oauth_associate_callback(
            user,
            oauth_client.name,
            token["access_token"],
            account_id,
            account_email,
            token.get("expires_at"),
            token.get("refresh_token"),
            request,
        )

        return schemas.model_validate(user_schema, user)

    return router
