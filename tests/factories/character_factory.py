from app.v1.models.product import Product
from app.v1.models.character import Character
from .product_factory import create_product

async def create_character(session, product: Product = None, name: str = "Test Character"):
    if product is None:
        product = await create_product(session)

    character = Character(
        name=name,
        product_id=product.id,
    )
    session.add(character)
    await session.commit()
    await session.refresh(character)
    return character
