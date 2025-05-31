from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select
from uuid import UUID


class BaseRepository:
    def __init__(self, session: AsyncSession, model=None):
        self.session = session
        if not model:
            raise ValueError("Model is not set for this repository.")
        self.model = model

    async def find(self, id: int | UUID):
        """
        Find a record by its ID. Raise an exception if not found.
        """

        query = select(self.model).where(self.model.id == id)
        result = await self.session.execute(query)
        instance = result.scalars().first()

        if not instance:
            raise NoResultFound(f"{self.model.__name__} with id {id} not found.")

        return instance

    async def find_by(self, **kwargs):
        """
        Find a record by given attributes. Raise an exception if not found.
        """
        query = select(self.model).where(
            *[getattr(self.model, key) == value for key, value in kwargs.items()]
        )
        result = await self.session.execute(query)
        instance = result.scalars().first()

        return instance

    async def find_by_or_raise(self, **kwargs):
        """
        Find a record by given attributes. Raise an exception if not found.
        """
        instance = await self.find_by(**kwargs)
        if not instance:
            raise NoResultFound(f"{self.model.__name__} with attributes {kwargs} not found.")
        return instance
