from app.v1.repositories.character_repository import CharacterRepository
from app.v1.repositories.product_repository import ProductRepository
from app.v1.schemas.character import CharacterRead
from typing import List, Optional


class CharacterService:
    def __init__(self, product_repository: ProductRepository, character_repository: CharacterRepository):
        self.product_repository = product_repository
        self.character_repository = character_repository

    async def list_characters_by_product(
        self,
        user_id: str,
        product_id: str,
        limit: int = 10,
        offset: int = 0,
        name: Optional[str] = None,
        sort_by: Optional[str] = "id",
        sort_order: Optional[str] = "asc",
    ) -> List[CharacterRead]:
        product = await self.__find_product(user_id, product_id)
        characters = await self.character_repository.list_characters_by_product(
            product.id, limit, offset, name, sort_by, sort_order
        )
        return [CharacterRead.model_validate(character) for character in characters]

    async def __find_product(self, user_id: str, product_id: str):
        product = await self.product_repository.get_product(user_id, product_id)
        if not product:
            raise HTTPException(
                status_code=404,
                detail=not_found_response_detail("Product", "/product_id", product_id),
            )
        return product