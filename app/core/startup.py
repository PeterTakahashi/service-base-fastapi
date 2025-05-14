from databases import Database
from app.core.config import settings

database = Database(settings.DATABASE_URL)


async def startup():
    await database.connect()


async def shutdown():
    await database.disconnect()
