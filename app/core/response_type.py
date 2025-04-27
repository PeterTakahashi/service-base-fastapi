from app.schemas.error import ErrorResponse
from app.lib.camel_to_snake import camel_to_snake

unauthorized_response = {
    401: {
        "description": "Unauthorized",
        "content": {"application/json": {"example": {"detail": "Unauthorized"}}},
    }
}


def not_found_response(model_name: str, pointer: str):
    return {
        404: {
            "description": f"{model_name} not found.",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": not_found_response_detail(
                        model_name, pointer, "123e4567-e89b-12d3-a456-426614174000"
                    ),
                }
            },
        }
    }


def not_found_response_detail(model_name: str, pointer: str, product_id: str):
    return {
        "errors": [
            {
                "status": "404",
                "code": f"{camel_to_snake(model_name)}_not_found",
                "title": "Not Found",
                "detail": f"{model_name} with id '{product_id}' not found.",
                "source": {"pointer": pointer},
            }
        ]
    }
