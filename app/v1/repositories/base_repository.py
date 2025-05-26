from sqlalchemy.ext.asyncio import AsyncSession

class BaseRepository:
    def __init__(self, session: AsyncSession, model=None):
        self.session = session
        self.model = model
