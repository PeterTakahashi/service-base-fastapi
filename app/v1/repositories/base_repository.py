from sqlalchemy.ext.asyncio import AsyncSession
from app.v1.repositories.base.read_repository import ReadRepository
from app.v1.repositories.base.write_repository import WriteRepository


class BaseRepository(ReadRepository, WriteRepository):
    def __init__(self, session: AsyncSession, model=None):
        if not model:
            raise ValueError("Model is not set for this repository.")
        ReadRepository.__init__(self, session, model)
        WriteRepository.__init__(self, session, model)
