from app.models.product import Product
from tests.factories.async_factory import AsyncSQLAlchemyModelFactory
from tests.factories.user_factory import UserFactory
import factory

class ProductFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Product

    title = factory.Faker("sentence", nb_words=3)
    user = factory.SubFactory(UserFactory)
