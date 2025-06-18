from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []

    for error in exc.errors():
        parameter = ""
        if error["loc"][0] == "body":
            parameter = "#/" + "/".join(str(loc) for loc in error["loc"][1:])
        elif error["loc"][0] == "query":
            parameter = "#/" + "/".join(str(loc) for loc in error["loc"][1:])
        elif error["loc"][0] == "path":
            parameter = "#/" + "/".join(str(loc) for loc in error["loc"][1:])
        else:
            parameter = "#/" + "/".join(str(loc) for loc in error["loc"])

        errors.append(
            {
                "code": "validation_error",
                "title": "Validation Error",
                "detail": error["msg"],
                "source": {"parameter": parameter},
            }
        )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "type": "about:blank",
            "title": "Unprocessable Entity",
            "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "instance": str(request.url),
            "errors": errors,
        },
    )
