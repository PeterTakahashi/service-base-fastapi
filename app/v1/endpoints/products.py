from fastapi import APIRouter, Depends, Query, HTTPException, status, Path
from sqlalchemy import select, func, exists
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.db.models import Product, Episode
from app.db.schemas.product import ProductRead, ProductCreate, ProductUpdate
from app.db.schemas.error import ErrorResponse
from app.core.user_setup import current_active_user
from app.core.user_manager import async_session_maker
from app.core.response_type import unauthorized_response, not_found_response, not_found_response_detail
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=List[ProductRead], responses=unauthorized_response)
async def index_products(
    user=Depends(current_active_user),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    title: Optional[str] = Query(None, description="Filter products by title", max_length=100, min_length=1)
):
    async with async_session_maker() as session:
        stmt = (
            select(
                Product,
                func.count(Episode.id).label("episode_count"),
            )
            .outerjoin(Episode, Episode.product_id == Product.id)
            .where(
                Product.user_id == user.id,
                Product.deleted_at.is_(None)
            )
            .group_by(Product.id)
            .limit(limit)
            .offset(offset)
        )

        if title:
            stmt = stmt.where(Product.title.ilike(f"%{title}%"))

        result = await session.execute(stmt)
        products = []
        for row in result.all():
            product, episode_count = row
            product_dict = {
                **product.__dict__,
                "episode_count": episode_count
            }
            products.append(ProductRead.model_validate(product_dict))
        return products

@router.post("/",
    response_model=ProductRead,
    status_code=201,
    responses={
        **unauthorized_response,
        409: {
            "description": "Product already exists.",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {
                        "errors": [
                            {
                                "status": "409",
                                "code": "product_already_exists",
                                "title": "Conflict",
                                "detail": "Product with title 'My Product' already exists.",
                                "source": { "pointer": "/title" }
                            }
                        ]
                    }
                }
            }
        }
    })
async def create_product(
    data: ProductCreate,
    user=Depends(current_active_user),
):
    async with async_session_maker() as session:
        stmt = select(exists().where(
            Product.user_id == user.id,
            Product.title == data.title,
            Product.deleted_at.is_(None)
        ))
        result = await session.execute(stmt)
        product_exists = result.scalar()

        if product_exists:
            raise HTTPException(
                status_code=409,
                detail={
                    "errors": [{
                        "status": "409",
                        "code": "product_already_exists",
                        "title": "Conflict",
                        "detail": f"Product with title '{data.title}' already exists.",
                        "source": { "pointer": "/title" }
                    }]
                }
            )
        product = Product(
            title=data.title,
            user_id=user.id
        )
        session.add(product)
        await session.commit()
        await session.refresh(product)

        return ProductRead.model_validate(product)

@router.get("/{product_id}",
    response_model=ProductRead,
    responses={
        **unauthorized_response,
        **not_found_response("Product", "/product_id")
    })

async def get_product(
    product_id: str = Path(..., title="The ID of the product to retrieve", description="The ID of the product to retrieve."),
    user=Depends(current_active_user),
):
    async with async_session_maker() as session:
        stmt = select(Product).where(
            Product.display_id == product_id,
            Product.user_id == user.id,
            Product.deleted_at.is_(None)
        )
        result = await session.execute(stmt)
        product = result.scalar_one_or_none()

        if not product:
            raise HTTPException(
                status_code=404,
                detail=not_found_response_detail("Product", "/product_id", product_id)
            )

        return ProductRead.model_validate(product)

@router.put("/{product_id}",
    response_model=ProductRead,
    responses={
        **unauthorized_response,
        **not_found_response("Product", "/product_id")
    })
async def update_product(
    data: ProductUpdate,
    product_id: str = Path(..., title="The ID of the product to update", description="The ID of the product to update."),
    user=Depends(current_active_user),
):
    async with async_session_maker() as session:
        stmt = select(Product).where(
            Product.display_id == product_id,
            Product.user_id == user.id,
            Product.deleted_at.is_(None)
        )
        result = await session.execute(stmt)
        product = result.scalar_one_or_none()

        if not product:
            raise HTTPException(
                status_code=404,
                detail=not_found_response_detail("Product", "/product_id", product_id)
            )

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(product, field, value)
        await session.commit()
        await session.refresh(product)

        return ProductRead.model_validate(product)

@router.delete("/{product_id}",
    status_code=204,
    responses={
        **unauthorized_response,
        **not_found_response("Product", "/product_id")
    })
async def delete_product(
    product_id: str = Path(..., title="The ID of the product to delete", description="The ID of the product to delete."),
    user=Depends(current_active_user),
):
    async with async_session_maker() as session:
        stmt = select(Product).where(
            Product.display_id == product_id,
            Product.user_id == user.id,
            Product.deleted_at.is_(None)
        )
        result = await session.execute(stmt)
        product = result.scalar_one_or_none()

        if not product:
            raise HTTPException(
                status_code=404,
                detail=not_found_response_detail("Product", "/product_id", product_id)
            )

        product.deleted_at = datetime.utcnow()
        await session.commit()
        return None
