from typing import List, Optional
from fastapi import HTTPException, UploadFile
from app.v1.repositories.character_repository import CharacterRepository
from app.v1.repositories.product_repository import ProductRepository
from app.v1.repositories.character_image_repository import CharacterImageRepository
from app.v1.schemas.character import CharacterRead
from app.v1.schemas.character_image import CharacterImageRead
from app.models.character import Character
from app.core.response_type import not_found_response_detail, conflict_response_detail
from app.core.s3 import generate_s3_storage_key, upload_file_to_s3
from app.lib.convert_id import encode_id
from app.lib.get_file_extension import get_file_extension


class CharacterService:
    def __init__(
        self,
        product_repository: ProductRepository,
        character_repository: CharacterRepository,
        character_image_repository: CharacterImageRepository,  # 追加
    ):
        self.product_repository = product_repository
        self.character_repository = character_repository
        self.character_image_repository = character_image_repository

    async def list_characters_by_product(
        self,
        user_id: str,
        product_id: int,
        limit: int = 10,
        offset: int = 0,
        name: Optional[str] = None,
        sort_by: str = "id",
        sort_order: str = "asc",
    ) -> List[CharacterRead]:
        product = await self.__find_product(user_id, product_id)
        characters = await self.character_repository.list_characters_by_product(
            product.id, limit, offset, name, sort_by, sort_order
        )
        return [
            CharacterRead.model_validate(character) for character in characters
        ]

    async def get_character(
        self, user_id: str, product_id: int, character_id: int
    ) -> CharacterRead:
        character = await self.__find_character(user_id, product_id, character_id)
        return CharacterRead.model_validate(character)

    async def create_character(
        self,
        user_id: str,
        product_id: int,
        name: str,
        character_image_files: List[UploadFile],
    ) -> CharacterRead:
        product = await self.__find_product(user_id, product_id)
        await self.__check_character_exists(product.id, name)
        character = await self.character_repository.create_character(name, product.id)
        character_read = CharacterRead(
            id=int(character.id),
            name=str(character.name),
            created_at=character.created_at,
            updated_at=character.updated_at,
            product_id=int(character.product_id),
            character_images=[],
        )
        return await self.__attach_images_to_character(
            character_read, character_image_files
        )

    async def __find_product(self, user_id: str, product_id: int):
        product = await self.product_repository.get_product(user_id, product_id)
        if not product:
            raise HTTPException(
                status_code=404,
                detail=not_found_response_detail(
                    "Product", "/product_id", encode_id(product_id)
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
                    "Character", "/character_id", encode_id(character_id)
                ),
            )
        return character

    async def __attach_images_to_character(
            self,
            character_read: CharacterRead,
            character_image_files: List[UploadFile]) -> CharacterRead:
        for file in character_image_files:
            # 1) character_image レコードを1件作成
            character_image = (
                await self.character_image_repository.character_image_create(
                    character_read.id
                )
            )

            # 2) S3にアップするためのオブジェクトキーを生成
            storage_key = generate_s3_storage_key(
                "character_images",
                encode_id(int(character_image.id)),
                "image",
                extension=get_file_extension(file.filename),
            )

            # 3) S3へアップロード
            upload_file_to_s3(file, storage_key)

            # 4) character_image レコードを更新
            character_image = await self.character_image_repository.update_character_image_storage_key(
                character_image, storage_key
            )
            character_image_read = CharacterImageRead.model_validate(
                character_image)
            character_read.character_images.append(character_image_read)
        return character_read

    async def __check_character_exists(
            self, product_id: int, name: str) -> bool:
        exists = await self.character_repository.character_exists(product_id, name)
        if exists:
            raise HTTPException(
                status_code=409,
                detail=conflict_response_detail("Character", "/name", name),
            )
        else:
            return False
