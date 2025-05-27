from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.v1.repositories.base_repository import BaseRepository
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


class UserRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def get_user_with_wallet(self, user_id: int) -> User | None:
        result = await self.session.execute(
            select(User).filter(User.id == user_id).options(selectinload(User.wallet))
        )
        return result.scalars().first()

    async def update_user(self, user: User, update_data: dict) -> User:
        for field, value in update_data.items():
            setattr(user, field, value)
        await self.session.commit()
        await self.session.refresh(user)
        return user
