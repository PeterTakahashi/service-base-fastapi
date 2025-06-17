from fastapi.responses import JSONResponse
from fastapi import status


def unprocessable_entity_json_response(
    instance: str, errors: list[dict]
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=unprocessable_entity_json_content(
            instance=instance,
            errors=errors,
        ),
    )


def unprocessable_entity_json_content(instance: str, errors: list[dict]) -> dict:
    return {
        "type": "about:blank",
        "title": "Unprocessable Entity",
        "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
        "instance": instance,
        "errors": errors,
    }
