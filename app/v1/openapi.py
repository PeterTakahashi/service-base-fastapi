from fastapi.openapi.utils import get_openapi

skip_adding_401 = {
    ("/auth/jwt/login", "post"),
    ("/auth/register/register", "post"),
    ("/auth/forgot-password", "post"),
    ("/auth/reset-password", "post"),
    ("/auth/cookie/google/authorize", "get"),
    ("/auth/cookie/github/authorize", "get"),
    ("/auth/cookie/google/callback", "get"),
    ("/auth/github/callback", "get"),
    ("/auth/cookie/login", "post"),
    ("/auth/cookie/logout", "post"),
}


def custom_openapi(app):
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["servers"] = [{"url": "/app/v1"}]

    accept_language_header = {
        "name": "Accept-Language",
        "in": "header",
        "description": "Language preference (e.g., en, ja)",
        "required": False,
        "schema": {
            "type": "string",
            "example": "en",
        },
    }
    for path, path_item in openapi_schema["paths"].items():
        for method, method_item in path_item.items():
            responses = method_item.setdefault("responses", {})
            parameters = method_item.setdefault("parameters", [])
            parameters.append(accept_language_header)

            if (path, method) not in skip_adding_401:
                authorization_language_header = {
                    "name": "Authorization",
                    "in": "header",
                    "description": "Bearer token for authentication",
                    "required": False,
                    "schema": {
                        "type": "string",
                        "example": "Bearer <token>",
                    },
                }
                parameters.append(authorization_language_header)

                responses.setdefault(
                    "401",
                    {
                        "description": "Unauthorized",
                        "content": {
                            "application/json": {
                                "example": {
                                    "errors": [
                                        {
                                            "status": "401",
                                            "code": "unauthorized",
                                            "title": "Unauthorized",
                                            "detail": "Authentication credentials were not provided or are invalid.",
                                        }
                                    ]
                                }
                            }
                        },
                    },
                )

            responses.setdefault(
                "500",
                {
                    "description": "Internal Server Error",
                    "content": {
                        "application/json": {
                            "example": {
                                "errors": [
                                    {
                                        "status": "500",
                                        "code": "internal_server_error",
                                        "title": "Internal Server Error",
                                        "detail": "An unexpected error occurred. Please try again later.",
                                    }
                                ]
                            }
                        }
                    },
                },
            )

            if "422" in responses:
                responses["422"] = {
                    "description": "Validation Error",
                    "content": {
                        "application/json": {
                            "example": {
                                "errors": [
                                    {
                                        "status": "422",
                                        "code": "validation_error",
                                        "title": "Validation Error",
                                        "detail": "The field 'title' is required.",
                                        "source": {"parameter": "title"},
                                    }
                                ]
                            }
                        }
                    },
                }

    app.openapi_schema = openapi_schema
    return app.openapi_schema
