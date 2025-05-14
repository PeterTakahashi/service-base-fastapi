from fastapi import HTTPException
from app.core.response_type import not_found_response_detail
from app.lib.convert_id import encode_id


class CharacterImageService:
    def __init__(self, character_image_repository):
        self.character_image_repository = character_image_repository

    async def delete_character_image(self, character_image_id: int) -> None:
        """
        Delete a character image by its ID.
        :param character_image_id: The ID of the character image to delete.
        :return: None
        """
        character_image = await self.character_image_repository.get_character_image(
            character_image_id
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
