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
