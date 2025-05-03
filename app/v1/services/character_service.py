from typing import List, Optional
from fastapi import HTTPException, UploadFile
from app.v1.repositories.character_repository import CharacterRepository
from app.v1.repositories.product_repository import ProductRepository
from app.v1.repositories.character_image_repository import CharacterImageRepository
from app.v1.schemas.character import CharacterRead
from app.v1.schemas.character_image import CharacterImageRead
from app.models.character import Character
from app.core.response_type import not_found_response_detail
from app.core.s3 import generate_s3_object_key, upload_file_to_s3, generate_presigned_url
from app.lib.convert_id import encode_id


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
        sort_by: Optional[str] = "id",
        sort_order: Optional[str] = "asc",
    ) -> List[CharacterRead]:
        product = await self.__find_product(user_id, product_id)
        characters = await self.character_repository.list_characters_by_product(
            product.id, limit, offset, name, sort_by, sort_order
        )
        return [CharacterRead.model_validate(character) for character in characters]

    # ここから追加: キャラクター + 複数画像を一度に作成する例
    async def create_character(
        self,
        user_id: str,
        product_id: int,
        name: str,
        image_files: List[UploadFile],  # 複数画像を受け取る
    ) -> CharacterRead:
        # 1) user_id が所有する product が存在するかチェック
        product = await self.__find_product(user_id, product_id)

        # 2) キャラクター名の重複チェック（任意: 重複NGとする例）
        if await self.character_repository.character_exists(product.id, name):
            raise HTTPException(
                status_code=409,
                detail={
                    "errors": [
                        {
                            "status": "409",
                            "code": "character_already_exists",
                            "title": "Conflict",
                            "detail": f"Character '{name}' already exists.",
                            "source": {"pointer": "/name"},
                        }
                    ]
                },
            )

        # 3) CharacterRepositoryを用いてキャラクターを作成
        character = await self.character_repository.create_character(name, product.id)

        character_read = CharacterRead(
            id=character.id,
            name=character.name,
            created_at=character.created_at,
            updated_at=character.updated_at,
            product_id=character.product_id,
            character_images=[]
        )

        # 4) 複数画像を character_image として作成
        if image_files:
            character_read = await self.__attach_images_to_character(
                character_read, image_files
            )

        # 5) 最終的に作成した character を返す
        return character_read

    # product を探して存在しなければ404を返す共通処理 (既存)
    async def __find_product(self, user_id: str, product_id: int):
        product = await self.product_repository.get_product(user_id, product_id)
        if not product:
            raise HTTPException(
                status_code=404,
                detail=not_found_response_detail("Product", "/product_id", product_id),
            )
        return product

    async def __attach_images_to_character(
        self, character_read: CharacterRead, image_files: List[UploadFile]
    ) -> CharacterRead:
        for file in image_files:
            # 1) character_image レコードを1件作成
            character_image = await self.character_image_repository.character_image_create(
                character_read.id
            )

            # 2) S3にアップするためのオブジェクトキーを生成
            object_key = generate_s3_object_key(
                "character_images",
                encode_id(character_image.id),
                "image",
                extension=file.filename.split(".")[-1] if "." in file.filename else "jpg",
            )

            # 3) S3へアップロード
            upload_file_to_s3(file, object_key)

            # 4) character_image レコードを更新
            await self.character_image_repository.update_character_image_storage_key(
                character_image, object_key
            )
            character_image_read = CharacterImageRead.model_validate({ "id": character_image.id,"image_url": generate_presigned_url(object_key) })
            character_read.character_images.append(character_image_read)
        return character_read
