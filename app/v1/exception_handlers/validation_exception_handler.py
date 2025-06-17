from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []

    for e in exc.errors():
        print(e)  # Debugging line to print the error details
        pointer = ""
        if e["loc"][0] == "body":
            pointer = "#/" + "/".join(str(loc) for loc in e["loc"][1:])
        elif e["loc"][0] == "query":
            pointer = "#/" + "/".join(str(loc) for loc in e["loc"][1:])
        elif e["loc"][0] == "path":
            pointer = "#/" + "/".join(str(loc) for loc in e["loc"][1:])
        else:
            pointer = "#/" + "/".join(str(loc) for loc in e["loc"])

        errors.append(
            {
                "code": "validation_error",
                "title": "Validation Error",
                "detail": e["msg"],
                "source": {"pointer": pointer},
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
