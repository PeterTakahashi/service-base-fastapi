from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists
from app.models.character_image import CharacterImage
from typing import Optional, List
from datetime import datetime

class CharacterImageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_character_images_by_character(
        self,
        character_id: int,
        limit: int = 10,
        offset: int = 0,
        sort_by: Optional[str] = "id",
        sort_order: Optional[str] = "asc",
    ) -> List[CharacterImage]:
        stmt = select(CharacterImage).where(
            CharacterImage.character_id == character_id,
            CharacterImage.deleted_at.is_(None),
        ).limit(limit).offset(offset)

        if sort_order.lower() == "desc":
            stmt = stmt.order_by(getattr(CharacterImage, sort_by).desc())
        else:
            stmt = stmt.order_by(getattr(CharacterImage, sort_by).asc())

        result = await self.session.execute(stmt)
        return result.scalars().all()

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

    async def character_image_exists(
        self, character_id: int
    ) -> bool:
        stmt = select(
            exists().where(
                CharacterImage.character_id == character_id,
                CharacterImage.deleted_at.is_(None),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar()

    async def get_character_image(self, character_image_id: int) -> Optional[CharacterImage]:
        stmt = select(CharacterImage).where(
            CharacterImage.id == character_image_id,
            CharacterImage.deleted_at.is_(None),
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_character_image_storage_key(
        self, character_image: CharacterImage, storage_key: str
    ) -> CharacterImage:
        character_image.storage_key = storage_key
        await self.session.commit()
        return character_image

    async def soft_delete_character_image(self, character_image: CharacterImage) -> None:
        character_image.deleted_at = datetime.utcnow()
        await self.session.commit()
