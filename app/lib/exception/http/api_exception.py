from fastapi import HTTPException, Request
from app.lib.schemas.error import ErrorDetail, ErrorResponse, ErrorSource
from app.lib.i18n import get_message, get_locale
from http import HTTPStatus
from typing import Optional


class APIException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail_code: str,
        detail_title: str | None = None,
        detail_detail: str | None = None,
        parameter: str | None = None,
        locale: str = "en",
    ):
        http_status = HTTPStatus(status_code)
        self.title = http_status.phrase
        self.status_code = status_code
        self.detail_code = detail_code
        self.__set_detail_title_and_detail(
            detail_code=detail_code,
            detail_title=detail_title,
            detail_detail=detail_detail,
            locale=locale,
        )
        self.parameter = parameter
        self.locale = locale
        super().__init__(status_code=status_code)

    def to_error_response(self, request: Request) -> ErrorResponse:
        self.locale = get_locale(request)
        self.__set_detail()
        return ErrorResponse(
            type="about:blank",
            title=self.title,
            status=self.status_code,
            instance=str(request.url),
            errors=[self.error_detail],
        )

    @classmethod
    def openapi_example(
        cls,
        status_code: int,
        detail_code: str,
        instance: str,
        parameter: Optional[str] = None,
        locale: str = "en",
        detail_title: Optional[str] = None,
        detail_detail: Optional[str] = None,
    ) -> dict:
        exc = cls(
            status_code=status_code,
            detail_code=detail_code,
            detail_title=detail_title,
            detail_detail=detail_detail,
            parameter=parameter,
            locale=locale,
        )
        exc.__set_detail()
        return ErrorResponse(
            type="about:blank",
            title=exc.title,
            status=exc.status_code,
            instance=instance,
            errors=[exc.error_detail],
        ).model_dump()

    def __set_detail(self) -> None:
        self.__set_detail_title_and_detail(
            detail_code=self.detail_code,
            detail_title=self.detail_title,
            detail_detail=self.detail_detail,
            locale=self.locale,
        )
        self.error_detail = ErrorDetail(
            status=str(self.status_code),
            code=self.detail_code,
            title=self.detail_title,
            detail=self.detail_detail,
            source=ErrorSource(parameter=self.parameter) if self.parameter else None,
        )

    def __set_detail_title_and_detail(
        self,
        detail_code: str,
        detail_title: str | None = None,
        detail_detail: str | None = None,
        locale: str = "en",
    ) -> None:
        self.detail_title = detail_title or get_message(locale, detail_code, "title")
        self.detail_detail = detail_detail or get_message(locale, detail_code, "detail")
