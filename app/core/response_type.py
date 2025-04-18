from app.db.schemas.error import ErrorResponse

unauthorized_response = {
    401: {
        "description": "Unauthorized",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Unauthorized"
                }
            }
        }
    }
}

def not_found_response(model_name: str, pointer: str):
    return {
        404: {
            "description": f"{model_name} not found.",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {
                        "errors": [
                            {
                                "status": "404",
                                "code": f"{model_name}_not_found",
                                "title": "Not Found",
                                "detail": f"{model_name} with id '123e4567-e89b-12d3-a456-426614174000' not found.",
                                "source": { "pointer": pointer }
                            }
                        ]
                    }
                }
            }
        }
    }
