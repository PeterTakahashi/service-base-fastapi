from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists
from app.models.character import Character
from typing import Optional, List, cast
from datetime import datetime
from sqlalchemy.orm import selectinload


class CharacterRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_characters_by_product(
        self,
        product_id: int,
        limit: int = 10,
        offset: int = 0,
        name: Optional[str] = None,
        sort_by: str = "id",
        sort_order: str = "asc",
    ) -> List[Character]:
        stmt = (
            select(Character)
            .where(
                Character.product_id == product_id,
                Character.deleted_at == None,  # noqa: E711,
            )
            .limit(limit)
            .offset(offset)
        )

        if name:
            stmt = stmt.where(Character.name.ilike(f"%{name}%"))

        if sort_order == "desc":
            stmt = stmt.order_by(getattr(Character, sort_by).desc())
        else:
            stmt = stmt.order_by(getattr(Character, sort_by).asc())

        result = await self.session.execute(stmt)
        return cast(List[Character], result.scalars().all())

    async def character_exists(self, product_id: int, name: str) -> bool:
        stmt = select(
            exists().where(
                Character.product_id == product_id,
                Character.name == name,
                Character.deleted_at == None,  # noqa: E711,
            )
        )
        result = await self.session.execute(stmt)
        return bool(result.scalar())

    async def create_character(self, name: str, product_id: int) -> Character:
        character = Character(name=name, product_id=product_id)
        self.session.add(character)
        await self.session.commit()
        await self.session.refresh(character)
        return character

    async def get_character(
        self, product_id: int, character_id: int
    ) -> Optional[Character]:
        stmt = (
            select(Character)
            .where(
                Character.product_id == product_id,
                Character.id == character_id,
                Character.deleted_at == None,  # noqa: E711,
            )
            .options(selectinload(Character.character_images))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_character(
        self,
        character: Character,
        data: dict
    ) -> Character:
        for field, value in data.items():
            setattr(character, field, value)
        await self.session.commit()
        await self.session.refresh(character)
        return character

    async def soft_delete_character(self, character: Character):
        character.deleted_at = datetime.utcnow()
        await self.session.commit()
