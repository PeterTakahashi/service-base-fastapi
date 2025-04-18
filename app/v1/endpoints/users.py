from fastapi import APIRouter, Depends
from app.core.user_setup import current_active_user
from app.db.schemas import UserRead, UserUpdate
from app.db.models import User
from app.core.response_type import unauthorized_response

router = APIRouter()

@router.get("/me", response_model=UserRead, responses=unauthorized_response)
async def get_me(user: User = Depends(current_active_user)):
    return user

@router.patch("/me", response_model=UserRead, responses=unauthorized_response)
async def update_me(data: UserUpdate, user: User = Depends(current_active_user)):
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    return user
