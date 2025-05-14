from app.core.response_type import not_found_response_detail
from app.core.response_type import forbidden_detail


def check_unauthorized_response(response):
    assert response.status_code == 401
    assert response.json() == {
        "errors": [
            {
                "code": "unauthorized",
                "detail": (
                    "Authentication credentials were not provided or are invalid."
                ),
                "status": "401",
                "title": "Unauthorized",
            }
        ]
    }


def check_not_found_response(response, model_name: str, parameter: str, target_id: str):
    check_not_found_status_code_and_detail(
        status_code=response.status_code,
        detail=response.json()["detail"],
        model_name=model_name,
        parameter=parameter,
        target_id=target_id,
    )


def check_not_found_status_code_and_detail(
    status_code: int, detail: dict, model_name: str, parameter: str, target_id: str
):
    assert status_code == 404
    assert detail == not_found_response_detail(
        model_name=model_name, parameter=parameter, target_id=target_id
    )


def check_forbidden_response(response):
    assert response.status_code == 403
    assert response.json()["detail"] == forbidden_detail
