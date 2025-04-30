from app.v1.models.user import User
from app.v1.models.product import Product
from .user_factory import create_user

async def create_product(session, user: User = None, title: str = "Test Product"):
    if user is None:
        user = await create_user(session)

    product = Product(
        title=title,
        user_id=user.id,
    )
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product
