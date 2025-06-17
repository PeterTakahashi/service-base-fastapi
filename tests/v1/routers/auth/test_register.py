import pytest
from httpx import AsyncClient
from tests.common.check_error_response import check_validation_error_response


async def test_register_success(client: AsyncClient, faker):
    """
    Test successful user registration.
    """
    unique_email = faker.unique.email()
    password = faker.password(length=12)

    registration_data = {"email": unique_email, "password": password}

    response = await client.post("/auth/register/register", json=registration_data)

    # Assertions
    assert (
        response.status_code == 201
    ), f"Expected 201, got {response.status_code}. Response: {response.text}"
    response_data = response.json()

    assert response_data["email"] == unique_email
    assert "id" in response_data


async def test_register_duplicate_email(client: AsyncClient, faker):
    """
    Test registration attempt with an email that already exists.
    """
    # 1. Register a user first
    email = faker.unique.email()
    password = faker.password(length=12)

    first_registration_data = {
        "email": email,
        "password": password,
    }
    reg_response = await client.post(
        "/auth/register/register", json=first_registration_data
    )
    assert (
        reg_response.status_code == 201
    ), f"Setup failed: Could not register initial user. Response: {reg_response.text}"

    # 2. Attempt to register another user with the *same email*
    second_registration_data = {
        "email": email,  # Same email
        "password": faker.password(length=12),
    }

    response = await client.post(
        "/auth/register/register", json=second_registration_data
    )
    check_validation_error_response(
        response,
        path="/auth/register/register",
        errors=[
            {
                "code": "REGISTER_USER_ALREADY_EXISTS",
                "title": "User Already Exists",
                "detail": "A user with this email already exists.",
                "source": {"pointer": "#/email"},
            }
        ],
    )


@pytest.mark.parametrize(
    "password, expected_reason",
    [
        ("abcdefgh", "Password must contain at least one digit"),
        ("12345678", "Password must contain at least one letter"),
        ("abcd1234", "Password must contain at least one special character"),
    ],
)
async def test_register_invalid_password_rules(
    client: AsyncClient, password, expected_reason, faker
):
    """
    Test registration with various invalid passwords that fail specific rules.
    """
    registration_data = {"email": faker.unique.email(), "password": password}

    response = await client.post("/auth/register/register", json=registration_data)

    check_validation_error_response(
        response,
        path="/auth/register/register",
        errors=[
            {
                "code": "REGISTER_INVALID_PASSWORD",
                "title": "Invalid Password",
                "detail": expected_reason,
                "source": {"pointer": "#/password"},
            }
        ],
    )


async def test_register_too_short_password(client: AsyncClient, faker):
    """
    Test registration with a password that is too short.
    """
    registration_data = {
        "email": faker.unique.email(),
        "password": "12",  # Too short
    }

    response = await client.post("/auth/register/register", json=registration_data)

    check_validation_error_response(
        response,
        path="/auth/register/register",
        errors=[
            {
                "code": "REGISTER_INVALID_PASSWORD",
                "title": "Invalid Password",
                "detail": "Password must be at least 8 characters long",
                "source": {"pointer": "#/password"},
            }
        ],
    )


async def test_register_missing_field(client: AsyncClient, faker):
    """
    Test registration with a missing required field (e.g., email).
    """
    registration_data = {
        # "email": faker.unique.email(), # Missing email
        "password": faker.password()
    }

    response = await client.post("/auth/register/register", json=registration_data)
    check_validation_error_response(
        response,
        path="/auth/register/register",
        errors=[
            {
                "code": "validation_error",
                "title": "Validation Error",
                "detail": "Field required",
                "source": {"pointer": "#/email"},
            }
        ],
    )
