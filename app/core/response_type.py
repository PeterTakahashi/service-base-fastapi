from app.v1.schemas.error import ErrorResponse
from app.lib.camel_to_snake import camel_to_snake

unauthorized_response = {
    401: {
        "description": "Unauthorized",
        "content": {"application/json": {"example": {"detail": "Unauthorized"}}},
    }
}

unauthorized_detail = {
    "errors": [
        {
            "status": "401",
            "code": "unauthorized",
            "title": "Unauthorized",
            "detail": "Authentication credentials were not provided or are invalid.",
        }
    ]
}

internal_server_error_detail = {
    "errors": [
        {
            "status": "500",
            "code": "internal_server_error",
            "title": "Internal Server Error",
            "detail": "An unexpected error occurred. Please try again later.",
        }
    ]
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


def not_found_response_detail(model_name: str, pointer: str, target_id: str):
    return {
        "errors": [
            {
                "status": "404",
                "code": f"{camel_to_snake(model_name)}_not_found",
                "title": "Not Found",
                "detail": f"{model_name} with id '{target_id}' not found.",
                "source": {"pointer": pointer},
            }
        ]
    }
