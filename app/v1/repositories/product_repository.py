from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists
from sqlalchemy.sql import and_
from app.models.product import Product
from typing import Optional, List, cast
from datetime import datetime


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_products(
        self,
        user_id: str,
        limit: int = 10,
        offset: int = 0,
        title: Optional[str] = None,
    ) -> List[Product]:
        stmt = (
            select(Product)
            .where(
                and_(
                    Product.user_id == user_id, Product.deleted_at == None  # noqa: E711
                )
            )
            .group_by(Product.id)
            .limit(limit)
            .offset(offset)
        )

        if title:
            stmt = stmt.where(Product.title.ilike(f"%{title}%"))

        result = await self.session.execute(stmt)
        return cast(List[Product], result.scalars().all())

    async def product_exists(self, user_id: str, title: str) -> bool:
        stmt = select(
            exists().where(
                and_(
                    Product.user_id == user_id,
                    Product.title == title,
                    Product.deleted_at == None,  # noqa: E711
                )
            )
        )
        result = await self.session.execute(stmt)
        return bool(result.scalar())

    async def create_product(self, title: str, user_id: str) -> Product:
        product = Product(title=title, user_id=user_id)
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def get_product(self, user_id: str, product_id: int) -> Optional[Product]:
        stmt = select(Product).where(
            and_(
                Product.id == product_id,
                Product.user_id == user_id,
                Product.deleted_at == None,  # noqa: E711
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_product(self, product: Product, data: dict) -> Product:
        for field, value in data.items():
            setattr(product, field, value)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def soft_delete_product(self, product: Product):
        product.deleted_at = datetime.utcnow()
        await self.session.commit()
