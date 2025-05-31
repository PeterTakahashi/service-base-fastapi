from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select
from uuid import UUID
from sqlalchemy.orm import joinedload, lazyload


class BaseRepository:
    def __init__(self, session: AsyncSession, model=None):
        self.session = session
        if not model:
            raise ValueError("Model is not set for this repository.")
        self.model = model

    async def find(
        self,
        id: int | UUID,
        sorted_by: str = None,
        sorted_order: str = "asc",
        joinedload_models: list = None,
        lazyload_models: list = None,
    ):
        """
        Find a record by its ID. Raise an exception if not found.
        """

        query = select(self.model).where(self.model.id == id)
        result = await self.session.execute(query)
        instance = result.scalars().first()

        if not instance:
            raise NoResultFound(f"{self.model.__name__} with id {id} not found.")

        return instance

    async def find_by(
        self,
        sorted_by: str = None,
        sorted_order: str = "asc",
        joinedload_models: list = None,
        lazyload_models: list = None,
        **kwargs,
    ):
        """
        Find a record by given attributes. Raise an exception if not found.
        """
        query = await self.__generate_query(
            limit=1,
            offset=0,
            sorted_by=sorted_by,
            sorted_order=sorted_order,
            joinedload_models=joinedload_models,
            lazyload_models=lazyload_models,
            **kwargs,
        )
        result = await self.session.execute(query)
        instance = result.scalars().first()

        return instance

    async def find_by_or_raise(
        self,
        sorted_by: str = None,
        sorted_order: str = "asc",
        joinedload_models: list = None,
        lazyload_models: list = None,
        **kwargs,
    ):
        """
        Find a record by given attributes. Raise an exception if not found.
        """
        instance = await self.find_by(
            sorted_by=sorted_by,
            sorted_order=sorted_order,
            joinedload_models=joinedload_models,
            lazyload_models=lazyload_models,
            **kwargs,
        )
        if not instance:
            raise NoResultFound(
                f"{self.model.__name__} with attributes {kwargs} not found."
            )
        return instance

    async def where(
        self,
        limit: int = 100,
        offset: int = 0,
        sorted_by: str = None,
        sorted_order: str = "asc",
        joinedload_models: list = None,
        lazyload_models: list = None,
        **kwargs,
    ):
        """
        Find records with optional filtering, sorting, and pagination.
        """
        query = await self.__generate_query(
            limit=limit,
            offset=offset,
            sorted_by=sorted_by,
            sorted_order=sorted_order,
            joinedload_models=joinedload_models,
            lazyload_models=lazyload_models,
            **kwargs,
        )
        result = await self.session.execute(query)
        return result.unique().scalars().all()

    async def __generate_query(
        self,
        limit: int = 100,
        offset: int = 0,
        sorted_by: str = None,
        sorted_order: str = "asc",
        joinedload_models: list = None,
        lazyload_models: list = None,
        **kwargs,
    ):
        """
        Generate a query with optional filtering, sorting, and pagination.
        """
        conditions = [
            getattr(self.model, key) == value for key, value in kwargs.items()
        ]
        query = select(self.model).where(*conditions)

        if joinedload_models:
            for model in joinedload_models:
                query = query.options(joinedload(model))
        if lazyload_models:
            for model in lazyload_models:
                query = query.options(lazyload(model))

        if sorted_by:
            if sorted_order == "asc":
                query = query.order_by(getattr(self.model, sorted_by).asc())
            else:
                query = query.order_by(getattr(self.model, sorted_by).desc())

        return query.limit(limit).offset(offset)
