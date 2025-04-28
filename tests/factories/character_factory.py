from app.v1.models.product import Product
from app.v1.models.character import Character

async def create_character(session, product: Product, name: str = "Test Character"):
    character = Character(
        name=name,
        product_id=product.id,
    )
    session.add(character)
    await session.commit()
    await session.refresh(character)
    return character
