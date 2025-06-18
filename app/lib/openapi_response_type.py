from app.lib.schemas.error import ErrorResponse
from app.lib.exception.api_exception import APIException
from app.lib.schemas.api_exception_openapi_example import APIExceptionOpenAPIExample
from typing import List, Optional


def openapi_response_type(
    status_code: int,
    request_path: str,
    api_exception_openapi_examples: List[APIExceptionOpenAPIExample],
    description: Optional[str] = None,
):
    examples = {}
    for api_exception_openapi_example in api_exception_openapi_examples:
        example = APIException.openapi_example(
            status_code=status_code,
            request_path=request_path,
            detail_code=api_exception_openapi_example.detail_code,
            detail_title=api_exception_openapi_example.detail_title,
            detail_detail=api_exception_openapi_example.detail_detail,
            parameter=api_exception_openapi_example.parameter,
        )
        examples[api_exception_openapi_example.detail_code] = example

    return {
        "description": description,
        "model": ErrorResponse,
        "content": {"application/json": {"examples": examples}},
    }
