from app.v1.models.character import Character
from app.v1.models.character_image import CharacterImage


async def create_character_image(
    session,
    character: Character,
) -> CharacterImage:
    character_image = CharacterImage(
        character_id=character.id,
    )
    session.add(character_image)
    await session.commit()
    await session.refresh(character_image)
    return character_image
