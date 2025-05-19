from fastapi_users.authentication import (
    CookieTransport
)
from fastapi import status
from fastapi.responses import RedirectResponse
from app.core.config import settings
from fastapi_users.openapi import OpenAPIResponseType

class CustomCookieTransport(CookieTransport):
    async def get_login_response(self, token: str) -> RedirectResponse:
        response = RedirectResponse(
            url=settings.FRONTEND_URL,
            status_code=302,
        )
        return self._set_login_cookie(response, token)

    def _set_login_cookie(self, response: RedirectResponse, token: str) -> RedirectResponse:
        response.set_cookie(
            self.cookie_name,
            token,
            max_age=self.cookie_max_age,
            path=self.cookie_path,
            domain=self.cookie_domain,
            secure=self.cookie_secure,
            httponly=self.cookie_httponly,
            samesite=self.cookie_samesite,
        )
        return response

    @staticmethod
    def get_openapi_login_responses_success() -> OpenAPIResponseType:
        return {
            status.HTTP_302_FOUND: {
                "description": "Redirect after successful login",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": "Redirecting to the frontend..."
                        }
                    }
                }
            }
        }
