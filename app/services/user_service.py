from app.repositories.user_repository import UserRepository
from app.models import User
from app.schemas.user import UserUpdate, UserRead

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_me(self, user: User) -> UserRead:
        return UserRead.model_validate(user)

    async def update_me(self, user: User, data: UserUpdate) -> UserRead:
        updated_user = await self.user_repository.update_user(user, data.model_dump(exclude_unset=True))
        return UserRead.model_validate(updated_user)
