from app.models.user import User
from tests.factories.async_factory import AsyncSQLAlchemyModelFactory
import factory


class UserFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    hashed_password = "fakehashedpassword"
    is_active = True
    is_superuser = False
    is_verified = True
