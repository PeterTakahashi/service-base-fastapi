import uuid
from app.v1.models.user import User

async def create_user(session):
    user = User(
        id=uuid.uuid4(),
        email=f"user_{uuid.uuid4()}@example.com",
        hashed_password="fakehashedpassword",  # パスワードはテストなので適当でOK
        is_active=True,
        is_superuser=False,
        is_verified=True,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

