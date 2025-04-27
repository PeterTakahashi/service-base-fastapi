from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.schemas.product import ProductRead, ProductCreate, ProductUpdate
from app.core.user_setup import current_active_user
from app.db.session import get_async_session
from app.repositories.product_repository import ProductRepository
from app.services.product_service import ProductService

router = APIRouter()


def get_product_service(
    session: AsyncSession = Depends(get_async_session),
) -> ProductService:
    repository = ProductRepository(session)
    return ProductService(repository)


@router.get("/", response_model=List[ProductRead])
async def index_products(
    user=Depends(current_active_user),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    title: Optional[str] = Query(None),
    service: ProductService = Depends(get_product_service),
):
    return await service.list_products(user.id, limit, offset, title)


@router.post("/", response_model=ProductRead, status_code=201)
async def create_product(
    data: ProductCreate,
    user=Depends(current_active_user),
    service: ProductService = Depends(get_product_service),
):
    return await service.create_product(user.id, data)


@router.get("/{product_id}", response_model=ProductRead)
async def get_product(
    product_id: str,
    user=Depends(current_active_user),
    service: ProductService = Depends(get_product_service),
):
    return await service.get_product(user.id, product_id)


@router.put("/{product_id}", response_model=ProductRead)
async def update_product(
    data: ProductUpdate,
    product_id: str,
    user=Depends(current_active_user),
    service: ProductService = Depends(get_product_service),
):
    return await service.update_product(user.id, product_id, data)


@router.delete("/{product_id}", status_code=204)
async def delete_product(
    product_id: str,
    user=Depends(current_active_user),
    service: ProductService = Depends(get_product_service),
):
    await service.delete_product(user.id, product_id)
    return None
