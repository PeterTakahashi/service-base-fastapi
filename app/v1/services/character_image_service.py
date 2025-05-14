from fastapi import HTTPException
from app.core.response_type import not_found_response_detail
from app.lib.convert_id import encode_id
from app.models.character import Character


class CharacterImageService:
    def __init__(
        self, product_repository, character_repository, character_image_repository
    ):
        self.product_repository = product_repository
        self.character_repository = character_repository
        self.character_image_repository = character_image_repository

    async def delete_character_image(
        self, user_id: str, product_id: int, character_id: int, character_image_id: int
    ) -> None:
        """
        Delete a character image by its ID.
        :param character_image_id: The ID of the character image to delete.
        :return: None
        """
        character = await self.__find_character(user_id, product_id, character_id)
        character_image = await self.character_image_repository.get_character_image(
            character.id, character_image_id
        )
        if not character_image:
            raise HTTPException(
                status_code=404,
                detail=not_found_response_detail(
                    "CharacterImage",
                    "character_image_id",
                    encode_id(character_image_id),
                ),
            )
        await self.character_image_repository.soft_delete_character_image(
            character_image
        )

    async def __find_product(self, user_id: str, product_id: int):
        product = await self.product_repository.get_product(user_id, product_id)
        if not product:
            raise HTTPException(
                status_code=404,
                detail=not_found_response_detail(
                    "Product", "product_id", encode_id(product_id)
                ),
            )
        return product

    async def __find_character(
        self, user_id: str, product_id: int, character_id: int
    ) -> Character:
        product = await self.__find_product(user_id, product_id)
        character = await self.character_repository.get_character(
            product.id, character_id
        )
        if not character:
            raise HTTPException(
                status_code=404,
                detail=not_found_response_detail(
                    "Character", "character_id", encode_id(character_id)
                ),
            )
        return character
