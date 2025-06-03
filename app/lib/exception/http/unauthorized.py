from fastapi import HTTPException, status


def HTTPExceptionUnauthorized(code: str = "unauthorized"):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "code": code,
        },
    )
