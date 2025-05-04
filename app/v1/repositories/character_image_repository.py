from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.character_image import CharacterImage
from typing import Optional
from datetime import datetime


class CharacterImageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def character_image_create(
        self, character_id: int
    ) -> CharacterImage:
        character_image = CharacterImage(
            character_id=character_id,
        )
        self.session.add(character_image)
        await self.session.commit()
        await self.session.refresh(character_image)
        return character_image

    async def get_character_image(
        self, character_image_id: int
    ) -> Optional[CharacterImage]:
        stmt = select(CharacterImage).where(
            CharacterImage.id == character_image_id,
            CharacterImage.deleted_at == None,  # noqa: E711
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_character_image_storage_key(
        self, character_image: CharacterImage, storage_key: str
    ) -> CharacterImage:
        character_image.storage_key = storage_key
        await self.session.commit()
        await self.session.refresh(
            character_image
        )  # Refresh to ensure the instance is updated
        return character_image

    async def soft_delete_character_image(
        self, character_image: CharacterImage
    ) -> None:
        character_image.deleted_at = datetime.utcnow()
        await self.session.commit()
