from app.lib.i18n import get_message
from http import HTTPStatus


def check_api_exception_info(
    exc_info,
    status_code: int,
    detail_code: str,
    detail_title: str | None = None,
    detail_detail: str | None = None,
    parameter: str | None = None,
    locale: str = "en",
):
    http_status = HTTPStatus(status_code)
    assert exc_info.value.detail["status"] == status_code
    assert exc_info.value.detail["title"] == http_status.phrase
    error_detail = exc_info.value.detail["errors"][0]
    assert error_detail["status"] == status_code
    assert error_detail["code"] == detail_code
    assert error_detail["detail"] == (
        detail_detail or get_message(locale, detail_code, "detail")
    )
    assert error_detail["title"] == (
        detail_title or get_message(locale, detail_code, "title")
    )
    assert error_detail["source"] == (
        None if parameter is None else {"parameter": f"#/{parameter}"}
    )
