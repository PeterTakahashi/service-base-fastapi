from fastapi import status
from app.lib.schemas.error import ErrorResponse
from app.lib.camel_to_snake import camel_to_snake


forbidden_detail = {
    "errors": [
        {
            "status": "403",
            "code": "forbidden",
            "title": "Forbidden",
            "detail": "You do not have permission to perform this action.",
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


def not_found_response(model_name: str, parameter: str):
    return {
        status.HTTP_404_NOT_FOUND: {
            "description": f"{model_name} not found.",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": not_found_response_detail(
                        model_name, parameter, "123e4567e89b"
                    ),
                }
            },
        }
    }


def not_found_response_detail(model_name: str, parameter: str, target_id: str):
    return {
        "errors": [
            {
                "status": "404",
                "code": f"{camel_to_snake(model_name)}_not_found",
                "title": "Not Found",
                "detail": f"{model_name} with id '{target_id}' not found.",
                "source": {"parameter": parameter},
            }
        ]
    }


def invalid_request_response_detail(parameter: str, message: str):
    return {
        "errors": [
            {
                "status": "422",
                "code": "invalid_request",
                "title": "Unprocessable Entity",
                "detail": message,
                "source": {"parameter": parameter},
            }
        ]
    }


def conflict_response(model_name: str, parameter: str):
    return {
        status.HTTP_409_CONFLICT: {
            "description": f"{model_name} already exists.",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": conflict_response_detail(
                        model_name, parameter, "123e4567-e89b-12d3-a456-426614174000"
                    ),
                }
            },
        }
    }


def conflict_response_detail(model_name: str, parameter: str, value: str):
    return {
        "errors": [
            {
                "status": "409",
                "code": f"{camel_to_snake(model_name)}_already_exists",
                "title": "Conflict",
                "detail": f"{model_name} with {parameter} '{value}' already exists.",
                "source": {"parameter": parameter},
            }
        ]
    }
