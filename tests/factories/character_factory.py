from app.v1.models.character import Character
from tests.factories.async_factory import AsyncSQLAlchemyModelFactory
import factory
from tests.factories.product_factory import ProductFactory

class CharacterFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Character

    name = factory.Faker("name")
    product = factory.SubFactory(ProductFactory)
