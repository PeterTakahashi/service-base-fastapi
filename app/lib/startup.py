from databases import Database
from app.lib.config import settings
from app.lib.utils.i18n import load_messages

database = Database(settings.DATABASE_URL)


async def startup():
    load_messages()
    await database.connect()


async def shutdown():
    await database.disconnect()
