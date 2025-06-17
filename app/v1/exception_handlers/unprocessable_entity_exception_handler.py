from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.i18n import get_locale, get_message


def unprocessable_entity_json_content(instance: str, errors: list[dict]) -> dict:
    return {
        "type": "about:blank",
        "title": "Unprocessable Entity",
        "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
        "instance": instance,
        "errors": errors,
    }


def unprocessable_entity_json_content_with_code(
    code: str,
    instance: str,
    source_parameter: str | None = None,
    detail: str | None = None,
    locale: str = "en",
) -> dict:
    error_detail = detail or get_message(locale, code, "detail")
    if source_parameter is None:
        source = {}
    else:
        source = {"pointer": f"#/{source_parameter}"}
    return {
        "type": "about:blank",
        "title": "Unprocessable Entity",
        "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
        "instance": instance,
        "errors": [
            {
                "status": "422",
                "code": code,
                "title": get_message(locale, code, "title"),
                "detail": error_detail,
                "source": source,
            }
        ],
    }


def unprocessable_entity_exception_handler(
    request: Request, exc: StarletteHTTPException
):
    if isinstance(exc.detail, dict):
        content = exc.detail
    elif isinstance(exc.detail, str):
        code = exc.detail.lower() if exc.detail else "unprocessable_entity"
        content = unprocessable_entity_json_content_with_code(
            code=code, instance=str(request.url), locale=get_locale(request)
        )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=content
    )
