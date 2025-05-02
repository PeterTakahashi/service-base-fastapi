from app.models.character_image import CharacterImage
from tests.factories.async_factory import AsyncSQLAlchemyModelFactory
import factory
from tests.factories.character_factory import CharacterFactory

class CharacterImageFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = CharacterImage

    character = factory.SubFactory(CharacterFactory)
