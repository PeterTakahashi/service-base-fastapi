from app.v1.repositories.character_repository import CharacterRepository
from app.v1.schemas.character import CharacterRead
from typing import List, Optional


class CharacterService:
    def __init__(self, character_repository: CharacterRepository):
        self.character_repository = character_repository

    async def list_characters_by_product(
        self,
        product_id: int,
        limit: int = 10,
        offset: int = 0,
        name: Optional[str] = None,
        sort_by: Optional[str] = "id",
        sort_order: Optional[str] = "asc",
    ) -> List[CharacterRead]:
        characters = await self.character_repository.list_characters_by_product(
            product_id, limit, offset, name, sort_by, sort_order
        )
        return [CharacterRead.model_validate(character) for character in characters]