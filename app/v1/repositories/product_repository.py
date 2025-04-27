from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, exists
from app.v1.models import Product, Episode
from typing import Optional, List
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
    ) -> List[tuple[Product, int]]:
        stmt = (
            select(Product, func.count(Episode.id).label("episode_count"))
            .outerjoin(Episode, Episode.product_id == Product.id)
            .where(Product.user_id == user_id, Product.deleted_at.is_(None))
            .group_by(Product.id)
            .limit(limit)
            .offset(offset)
        )

        if title:
            stmt = stmt.where(Product.title.ilike(f"%{title}%"))

        result = await self.session.execute(stmt)
        return result.all()

    async def product_exists(self, user_id: str, title: str) -> bool:
        stmt = select(
            exists().where(
                Product.user_id == user_id,
                Product.title == title,
                Product.deleted_at.is_(None),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar()

    async def create_product(self, title: str, user_id: str) -> Product:
        product = Product(title=title, user_id=user_id)
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def get_product(self, user_id: str, display_id: str) -> Optional[Product]:
        stmt = select(Product).where(
            Product.display_id == display_id,
            Product.user_id == user_id,
            Product.deleted_at.is_(None),
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
