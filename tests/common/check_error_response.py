from app.lib.i18n import get_message
from http import HTTPStatus


def check_api_exception_response(
    response,
    status_code: int,
    detail_code: str,
    detail_title: str | None = None,
    detail_detail: str | None = None,
    parameter: str | None = None,
    locale: str = "en",
):
    http_status = HTTPStatus(status_code)
    assert response.status_code == status_code
    assert response.json() == {
        "type": "about:blank",
        "title": http_status.phrase,
        "status": status_code,
        "instance": str(response.url),
        "errors": [
            {
                "status": str(status_code),
                "code": detail_code,
                "title": detail_title or get_message(locale, detail_code, "title"),
                "detail": detail_detail or get_message(locale, detail_code, "detail"),
                "source": {"parameter": f"#/{parameter}"} if parameter else None,
            }
        ],
    }
