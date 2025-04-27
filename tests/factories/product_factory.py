from app.models.user import User
from app.models.product import Product


async def create_product(session, user: User, title: str = "Test Product"):
    product = Product(
        title=title,
        user_id=user.id,
    )
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product
