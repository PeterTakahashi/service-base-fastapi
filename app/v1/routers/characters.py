from fastapi import APIRouter, Depends, Path, Form, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.v1.schemas.character import CharacterRead
from app.core.user_setup import current_active_user
from app.db.session import get_async_session
from app.v1.repositories.product_repository import ProductRepository
from app.v1.repositories.character_repository import CharacterRepository
from app.v1.repositories.character_image_repository import CharacterImageRepository
from app.v1.services.character_service import CharacterService
from app.core.response_type import not_found_response, conflict_response
from app.lib.convert_id import decode_id
from typing import List

router = APIRouter()


def get_character_service(
    session: AsyncSession = Depends(get_async_session),
) -> CharacterService:
    product_repository = ProductRepository(session)
    character_repository = CharacterRepository(session)
    character_image_repository = CharacterImageRepository(session)
    return CharacterService(
        product_repository=product_repository,
        character_repository=character_repository,
        character_image_repository=character_image_repository,
    )


# @router.get("/", response_model=List[CharacterRead])
# async def index_characters(
#     user=Depends(current_active_user),
#     limit: int = Query(10, ge=1, le=100),
#     offset: int = Query(0, ge=0),
#     title: Optional[str] = Query(None),
#     service: CharacterService = Depends(get_character_service),
# ):
#     return await service.list_characters(user.id, limit, offset, title)


@router.post(
    "/",
    response_model=CharacterRead,
    status_code=201,
    responses=conflict_response("Character", "name"),
)
async def create_character(
    product_id: str = Path(...),
    name: str = Form(...),
    character_image_files: List[UploadFile] = File(
        ..., description="List of character image files", max_items=10, min_items=1
    ),
    user=Depends(current_active_user),
    service: CharacterService = Depends(get_character_service),
):
    return await service.create_character(
        user.id, decode_id(product_id), name, character_image_files
    )


@router.get(
    "/{character_id}",
    response_model=CharacterRead,
    status_code=200,
    responses=not_found_response("Character", "/character_id"),
)
async def get_character(
    product_id: str = Path(...),
    character_id: str = Path(...),
    user=Depends(current_active_user),
    service: CharacterService = Depends(get_character_service),
):
    return await service.get_character(
        user.id, decode_id(product_id), decode_id(character_id)
    )
