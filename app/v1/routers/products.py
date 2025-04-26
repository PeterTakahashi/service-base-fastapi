from fastapi import APIRouter, Depends, Query, HTTPException, Path
from sqlalchemy import select, func, exists
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.models import Product, Episode
from app.schemas.product import ProductRead, ProductCreate, ProductUpdate
from app.schemas.error import ErrorResponse
from app.core.user_setup import current_active_user
from app.core.response_type import unauthorized_response, not_found_response, not_found_response_detail
from datetime import datetime
from app.db.session import get_async_session
from app.repositories.product_repository import ProductRepository

router = APIRouter()

@router.get("/", response_model=List[ProductRead], responses=unauthorized_response)
async def index_products(
    user=Depends(current_active_user),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    title: Optional[str] = Query(None),
    session: AsyncSession = Depends(get_async_session)
):
    product_repo = ProductRepository(session)
    product_results = await product_repo.list_products(user.id, limit=limit, offset=offset, title=title)

    products = []
    for product, episode_count in product_results:
        product_dict = {
            **product.__dict__,
            "episode_count": episode_count
        }
        products.append(product_dict)
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
    session: AsyncSession = Depends(get_async_session)
):
    product_repo = ProductRepository(session)

    # Check if the product already exists
    product_exists = await product_repo.product_exists(user.id, data.title)
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

    # Create the product using the repository
    product = await product_repo.create_product(title=data.title, user_id=user.id)

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
    session: AsyncSession = Depends(get_async_session)
):
    product_repo = ProductRepository(session)
    product = await product_repo.get_product(user.id, product_id)

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
    session: AsyncSession = Depends(get_async_session)
):
    product_repo = ProductRepository(session)
    product = await product_repo.get_product(user.id, product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail=not_found_response_detail("Product", "/product_id", product_id)
        )
    product = await product_repo.update_product(product, data.dict(exclude_unset=True))
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
    session: AsyncSession = Depends(get_async_session)
):
    product_repo = ProductRepository(session)
    product = await product_repo.get_product(user.id, product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail=not_found_response_detail("Product", "/product_id", product_id)
        )
    await product_repo.soft_delete_product(product)
    return None
