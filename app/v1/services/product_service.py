from app.v1.repositories.product_repository import ProductRepository
from app.v1.schemas.product import ProductCreate, ProductUpdate, ProductRead
from app.core.response_type import not_found_response_detail, conflict_response_detail
from fastapi import HTTPException
from typing import List, Optional
from app.lib.convert_id import encode_id


class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def list_products(
        self,
        user_id: str,
        limit: int = 10,
        offset: int = 0,
        title: Optional[str] = None,
    ) -> List[ProductRead]:
        products = await self.product_repository.list_products(
            user_id, limit, offset, title
        )
        return [ProductRead.model_validate(product) for product in products]

    async def create_product(self, user_id: str, data: ProductCreate) -> ProductRead:
        await self.__check_product_exists(user_id, data.title)
        product = await self.product_repository.create_product(
            title=data.title, user_id=user_id
        )
        return ProductRead.model_validate(product)

    async def get_product(self, user_id: str, product_id: int) -> ProductRead:
        product = await self.__find_product(user_id, product_id)
        return ProductRead.model_validate(product)

    async def update_product(
        self, user_id: str, product_id: int, data: ProductUpdate
    ) -> ProductRead:
        await self.__check_product_exists(user_id, data.title)
        product = await self.__find_product(user_id, product_id)
        updated_product = await self.product_repository.update_product(
            product, data.model_dump(exclude_unset=True)
        )
        return ProductRead.model_validate(updated_product)

    async def delete_product(self, user_id: str, product_id: int):
        product = await self.__find_product(user_id, product_id)
        await self.product_repository.soft_delete_product(product)

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

    async def __check_product_exists(self, user_id: str, title: str) -> bool:
        exists = await self.product_repository.product_exists(user_id, title)
        if exists:
            raise HTTPException(
                status_code=409,
                detail=conflict_response_detail("Product", "/title", title),
            )
        else:
            return False
