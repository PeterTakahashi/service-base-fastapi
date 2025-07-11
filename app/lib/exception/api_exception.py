from fastapi import HTTPException, Request
from app.schemas.error import ErrorDetail, ErrorResponse, ErrorSource
from app.lib.utils.i18n import get_message, get_locale
from http import HTTPStatus
from typing import Optional, List
from app.core.config import settings


class APIException(HTTPException):
    """
    Custom exception class for API errors following RFC 9457,
    which specifies a standardized error response format for HTTP APIs.
    See: https://www.rfc-editor.org/rfc/rfc9457.html
    """

    def __init__(
        self,
        status_code: int,
        error_details: List[ErrorDetail],
        locale: str = "en",
    ):
        http_status = HTTPStatus(status_code)
        self.title = http_status.phrase
        self.status_code = status_code
        self.error_details = error_details
        self.locale = locale

        # detailに渡した値はresponseの時には使わないが、testsでの検証のために必要
        super().__init__(
            status_code=status_code,
            detail={
                "type": "about:blank",
                "title": self.title,
                "status": status_code,
                "errors": error_details,
            },
        )

    def to_error_response(self, request: Request) -> ErrorResponse:
        self.locale = get_locale(request)
        return ErrorResponse(
            type="about:blank",
            title=self.title,
            status=self.status_code,
            instance=str(request.url),
            errors=self.error_details,
        )

    @classmethod
    def openapi_example(
        cls,
        status_code: int,
        detail_code: str,
        request_path: str,
        detail_title: Optional[str] = None,
        detail_detail: Optional[str] = None,
        pointer: Optional[str] = None,
        locale: str = "en",
    ) -> dict:
        instance = f"{settings.BACKEND_API_V1_URL}{request_path}"
        detail_title = detail_title or get_message(locale, detail_code, "title")
        detail_detail = detail_detail or get_message(locale, detail_code, "detail")
        source = ErrorSource(pointer=f"#/{pointer}") if pointer else None
        error_detail = ErrorDetail(
            status=str(status_code),
            code=detail_code,
            title=detail_title,
            detail=detail_detail,
            source=source,
        )
        exc = APIException(
            status_code=status_code, error_details=[error_detail], locale=locale
        )
        error_response = ErrorResponse(
            type="about:blank",
            title=exc.title,
            status=exc.status_code,
            instance=instance,
            errors=exc.error_details,
        ).model_dump()
        openapi_example_summary = get_message(
            locale, detail_code, "openapi_example_summary"
        )
        return {"summary": openapi_example_summary, "value": error_response}


def init_api_exception(
    status_code: int,
    detail_code: str,
    detail_title: Optional[str] = None,
    detail_detail: Optional[str] = None,
    pointer: Optional[str] = None,
    locale: str = "en",
) -> APIException:
    detail_title = detail_title or get_message(locale, detail_code, "title")
    detail_detail = detail_detail or get_message(locale, detail_code, "detail")
    source = ErrorSource(pointer=f"#/{pointer}") if pointer else None
    error_detail = ErrorDetail(
        status=str(status_code),
        code=detail_code,
        title=detail_title,
        detail=detail_detail,
        source=source,
    )
    return APIException(
        status_code=status_code, error_details=[error_detail], locale=locale
    )
