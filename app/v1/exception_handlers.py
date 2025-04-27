
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 401:
        return JSONResponse(
            status_code=401,
            content={
                "errors": [
                    {
                        "status": "401",
                        "code": "unauthorized",
                        "title": "Unauthorized",
                        "detail": "Authentication credentials were not provided or are invalid.",
                    }
                ]
            },
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

async def server_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "errors": [
                {
                    "status": "500",
                    "code": "internal_server_error",
                    "title": "Internal Server Error",
                    "detail": "An unexpected error occurred. Please try again later.",
                }
            ]
        },
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for e in exc.errors():
        pointer = ""
        if e["loc"]:
            # ["body", "field_name"] -> /field_name
            pointer = "/" + "/".join(str(loc) for loc in e["loc"] if loc != "body")

        errors.append({
            "status": "422",
            "code": "validation_error",
            "title": "Validation Error",
            "detail": e["msg"],
            "source": {
                "pointer": pointer or None
            }
        })

    return JSONResponse(
        status_code=422,
        content={"errors": errors},
    )
