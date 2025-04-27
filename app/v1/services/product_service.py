from app.v1.repositories.product_repository import ProductRepository
from app.v1.schemas.product import ProductCreate, ProductUpdate, ProductRead
from app.core.response_type import not_found_response_detail
from fastapi import HTTPException
from typing import List, Optional


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
        results = await self.product_repository.list_products(
            user_id, limit, offset, title
        )
        products = []
        for product, episode_count in results:
            product_dict = {**product.__dict__, "episode_count": episode_count}
            products.append(ProductRead.model_validate(product_dict))
        return products

    async def create_product(self, user_id: str, data: ProductCreate) -> ProductRead:
        exists = await self.product_repository.product_exists(user_id, data.title)
        if exists:
            raise HTTPException(
                status_code=409,
                detail={
                    "errors": [
                        {
                            "status": "409",
                            "code": "product_already_exists",
                            "title": "Conflict",
                            "detail": f"Product with title '{data.title}' already exists.",
                            "source": {"pointer": "/title"},
                        }
                    ]
                },
            )
        product = await self.product_repository.create_product(
            title=data.title, user_id=user_id
        )
        return ProductRead.model_validate(product)

    async def get_product(self, user_id: str, product_id: str) -> ProductRead:
        product = await self.product_repository.get_product(user_id, product_id)
        if not product:
            raise HTTPException(
                status_code=404,
                detail=not_found_response_detail("Product", "/product_id", product_id),
            )
        return ProductRead.model_validate(product)

    async def update_product(
        self, user_id: str, product_id: str, data: ProductUpdate
    ) -> ProductRead:
        product = await self.product_repository.get_product(user_id, product_id)
        if not product:
            raise HTTPException(
                status_code=404,
                detail=not_found_response_detail("Product", "/product_id", product_id),
            )
        updated_product = await self.product_repository.update_product(
            product, data.model_dump(exclude_unset=True)
        )
        return ProductRead.model_validate(updated_product)

    async def delete_product(self, user_id: str, product_id: str):
        product = await self.product_repository.get_product(user_id, product_id)
        if not product:
            raise HTTPException(
                status_code=404,
                detail=not_found_response_detail("Product", "/product_id", product_id),
            )
        await self.product_repository.soft_delete_product(product)
