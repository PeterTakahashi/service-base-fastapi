import pytest
import pytest_asyncio
from httpx import AsyncClient
from faker import Faker
pytestmark = pytest.mark.asyncio
fake = Faker()

@pytest_asyncio.fixture(scope="function")
async def test_register_success(client: AsyncClient):
    """
    Test successful user registration.
    """
    unique_email = fake.unique.email()
    password = fake.password(length=12)

    registration_data = {
        "email": unique_email,
        "password": password
    }

    response = await client.post("/auth/register/register", json=registration_data)

    # Assertions
    assert response.status_code == 201, f"Expected 201, got {response.status_code}. Response: {response.text}"
    response_data = response.json()

    assert response_data["email"] == unique_email
    assert "id" in response_data
    assert response_data["is_active"] is True
    assert response_data["is_superuser"] is False
    assert response_data["is_verified"] is False
    assert "created_at" in response_data
    assert "updated_at" in response_data
    assert "hashed_password" not in response_data # Ensure password is not returned


async def test_register_duplicate_email(client: AsyncClient):
    """
    Test registration attempt with an email that already exists.
    """
    # 1. Register a user first
    email = fake.unique.email()
    password = fake.password(length=12)

    first_registration_data = {
        "email": email,
        "password": password,
    }
    reg_response = await client.post("/auth/register/register", json=first_registration_data)
    assert reg_response.status_code == 201, f"Setup failed: Could not register initial user. Response: {reg_response.text}"

    # 2. Attempt to register another user with the *same email*
    second_registration_data = {
        "email": email, # Same email
        "password": fake.password(length=12)
    }

    response = await client.post("/auth/register/register", json=second_registration_data)

    # Assertions
    assert response.status_code == 400, f"Expected 400, got {response.status_code}. Response: {response.text}"
    response_data = response.json()
    assert response_data["detail"] == "REGISTER_USER_ALREADY_EXISTS"

@pytest.mark.parametrize("password, expected_reason", [
    ("abcdefgh", "Password must contain at least one digit"),
    ("12345678", "Password must contain at least one letter"),
    ("abcd1234", "Password must contain at least one special character"),
])
async def test_register_invalid_password_rules(client: AsyncClient, password, expected_reason):
    """
    Test registration with various invalid passwords that fail specific rules.
    """
    registration_data = {
        "email": fake.unique.email(),
        "password": password
    }

    response = await client.post("/auth/register/register", json=registration_data)

    assert response.status_code == 400, f"Expected 400, got {response.status_code}. Response: {response.text}"
    response_data = response.json()
    assert response_data["detail"]["code"] == "REGISTER_INVALID_PASSWORD"
    assert expected_reason in response_data["detail"]["reason"]

async def test_register_too_short_password(client: AsyncClient):
    """
    Test registration with a password that is too short.
    """
    registration_data = {
        "email": fake.unique.email(),
        "password": "12"  # Too short
    }

    response = await client.post("/auth/register/register", json=registration_data)

    assert response.status_code == 422, f"Expected 422, got {response.status_code}. Response: {response.text}"
    response_data = response.json()
    assert response_data["detail"] == [{'type': 'string_too_short', 'loc': ['body', 'password'], 'msg': 'String should have at least 8 characters', 'input': '12', 'ctx': {'min_length': 8}}]

async def test_register_missing_field(client: AsyncClient):
    """
    Test registration with a missing required field (e.g., email).
    """
    registration_data = {
        # "email": fake.unique.email(), # Missing email
        "password": fake.password()
    }

    response = await client.post("/auth/register/register", json=registration_data)

    # Assertions for validation error
    assert response.status_code == 422, f"Expected 422, got {response.status_code}. Response: {response.text}"
    response_data = response.json()
    assert "detail" in response_data
    assert isinstance(response_data["detail"], list)
    assert len(response_data["detail"]) > 0
    # Check if the error message relates to the missing 'email' field
    email_error_found = any(err.get("loc") == ["body", "email"] and "field required" in err.get("msg", "").lower() for err in response_data["detail"])
    assert email_error_found, f"Validation error for missing email not found in {response_data['detail']}"