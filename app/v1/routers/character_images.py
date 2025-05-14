from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.response_type import not_found_response
from app.v1.repositories.character_image_repository import CharacterImageRepository
from app.v1.services.character_image_service import CharacterImageService
from app.core.user_setup import current_active_user
from app.lib.convert_id import decode_id
from app.db.session import get_async_session

router = APIRouter()


def get_character_image_service(
    session: AsyncSession = Depends(get_async_session),
) -> CharacterImageService:
    character_image_repository = CharacterImageRepository(session)
    return CharacterImageService(
        character_image_repository=character_image_repository,
    )


@router.delete(
    "/{character_image_id}",
    status_code=204,
    responses=not_found_response("CharacterImage", "character_image_id"),
)
async def delete_product(
    character_image_id: str = Path(...),
    user=Depends(current_active_user),
    service: CharacterImageService = Depends(get_character_image_service),
):
    await service.delete_character_image(
        user_id=user.id,
        character_image_id=decode_id(character_image_id),
    )
