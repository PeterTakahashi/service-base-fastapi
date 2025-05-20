from fastapi_users.authentication import CookieTransport
from fastapi import status
from fastapi.responses import RedirectResponse, Response
from app.core.config import settings
from fastapi_users.openapi import OpenAPIResponseType


class OAuthCookieTransport(CookieTransport):
    async def get_login_response(self, token: str) -> Response:
        response = RedirectResponse(
            url=settings.FRONTEND_URL,
            status_code=302,
        )
        return self._set_login_cookie(response, token)

    @staticmethod
    def get_openapi_login_responses_success() -> OpenAPIResponseType:
        return {
            status.HTTP_302_FOUND: {
                "description": "Redirect after successful login",
                "content": {
                    "application/json": {
                        "example": {"detail": "Redirecting to the frontend..."}
                    }
                },
            }
        }


oauth_cookie_transport = OAuthCookieTransport(
    cookie_name="access_token",
    cookie_max_age=settings.ACCESS_TOKEN_EXPIRED_SECONDS,
    cookie_secure=settings.SECURE_COOKIES,
    cookie_httponly=True,
)
