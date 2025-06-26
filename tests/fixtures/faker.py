from faker import Faker
import pytest_asyncio
from fastapi_users.password import PasswordHelper
from app.lib.utils.convert_id import encode_id
from app.v1.schemas.common.address.read import AddressRead

@pytest_asyncio.fixture
def faker():
    return Faker()


@pytest_asyncio.fixture
async def fake_id() -> str:
    return encode_id(0)


@pytest_asyncio.fixture
def fake_email(faker) -> str:
    """
    Generate a fake email address.
    """
    return faker.unique.email()


@pytest_asyncio.fixture
def fake_password(faker) -> str:
    """
    Generate a fake password.
    """
    return faker.password(
        length=12, special_chars=True, digits=True, upper_case=True, lower_case=True
    )


@pytest_asyncio.fixture
def fake_hashed_password(fake_password) -> str:
    """
    Generate a hashed password using the Faker library.
    """
    return PasswordHelper().hash(password=fake_password)

@pytest_asyncio.fixture
def fake_address(faker) -> AddressRead:
    """
    Generate a fake address.
    """
    return AddressRead(
            line1=faker.street_address(),
            line2=faker.secondary_address(),
            city=faker.city(),
            state=faker.state_abbr(),
            postal_code=faker.postcode(),
            country="US"
    )
