from fastapi import status


def unprocessable_entity_json_content(instance: str, errors: list[dict]) -> dict:
    return {
        "type": "about:blank",
        "title": "Unprocessable Entity",
        "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
        "instance": instance,
        "errors": errors,
    }
