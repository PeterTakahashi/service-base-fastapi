from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select
from uuid import UUID
from sqlalchemy.orm import joinedload, lazyload
from sqlalchemy import func
from typing import Optional, List, Union

OPERATORS = {
    # 完全一致
    "exact": lambda col, val: col == val,
    "iexact": lambda col, val: col.ilike(val),
    # 部分一致
    "contains": lambda col, val: col.contains(val),
    "icontains": lambda col, val: col.ilike(f"%{val}%"),
    # in句
    "in": lambda col, val: col.in_(val) if isinstance(val, list) else col.in_([val]),
    # 大小比較
    "gt": lambda col, val: col > val,
    "gte": lambda col, val: col >= val,
    "lt": lambda col, val: col < val,
    "lte": lambda col, val: col <= val,
    # 前方・後方一致
    "startswith": lambda col, val: col.startswith(val),
    "istartswith": lambda col, val: col.ilike(f"{val}%"),
    "endswith": lambda col, val: col.endswith(val),
    "iendswith": lambda col, val: col.ilike(f"%{val}"),
}


class BaseRepository:
    def __init__(self, session: AsyncSession, model=None):
        self.session = session
        if not model:
            raise ValueError("Model is not set for this repository.")
        self.model = model

    async def find(
        self,
        id: Union[int, UUID],
        sorted_by: Optional[str] = None,
        sorted_order: str = "asc",
        joinedload_models: Optional[List] = None,
        lazyload_models: Optional[List] = None,
    ):
        """
        Find a record by its ID. Raise an exception if not found.
        """
        query = await self.__generate_query(
            limit=1,
            offset=0,
            sorted_by=sorted_by,
            sorted_order=sorted_order,
            joinedload_models=joinedload_models,
            lazyload_models=lazyload_models,
            id=id,
        )

        result = await self.session.execute(query)
        instance = result.scalars().first()

        if not instance:
            raise NoResultFound(f"{self.model.__name__} with id {id} not found.")

        return instance

    async def find_by(
        self,
        sorted_by: Optional[str] = None,
        sorted_order: str = "asc",
        joinedload_models: Optional[List] = None,
        lazyload_models: Optional[List] = None,
        **kwargs,
    ):
        """
        Find a record by given attributes. Return None if not found.
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
        sorted_by: Optional[str] = None,
        sorted_order: str = "asc",
        joinedload_models: Optional[List] = None,
        lazyload_models: Optional[List] = None,
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
        sorted_by: Optional[str] = None,
        sorted_order: str = "asc",
        joinedload_models: Optional[List] = None,
        lazyload_models: Optional[List] = None,
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

    async def count(self, **kwargs) -> int:
        """
        Count records with optional filtering.
        """
        conditions = await self.__get_conditions(**kwargs)
        query = select(func.count("*")).select_from(self.model).where(*conditions)
        result = await self.session.execute(query)
        return result.scalar() or 0

    async def exists(self, **kwargs) -> bool:
        """
        Check if any record exists with the given attributes.
        """
        counted = await self.count(**kwargs)
        return counted > 0

    async def __generate_query(
        self,
        limit: int = 100,
        offset: int = 0,
        sorted_by: Optional[str] = None,
        sorted_order: str = "asc",
        joinedload_models: Optional[List] = None,
        lazyload_models: Optional[List] = None,
        **kwargs,
    ):
        """
        Generate a query with optional filtering, sorting, and pagination.
        """
        conditions = await self.__get_conditions(**kwargs)
        query = select(self.model).where(*conditions)

        if joinedload_models:
            for model in joinedload_models:
                query = query.options(joinedload(model))
        if lazyload_models:
            for model in lazyload_models:
                query = query.options(lazyload(model))

        if sorted_by:
            query = self._apply_order_by(query, sorted_by, sorted_order)

        return query.limit(limit).offset(offset)

    def _apply_order_by(self, query, sorted_by: str, sorted_order: str):
        """
        クエリに対して order_by を適用するヘルパー。
        """
        column = getattr(self.model, sorted_by, None)
        if not column:
            raise AttributeError(
                f"{self.model.__name__} has no attribute '{sorted_by}'"
            )

        if sorted_order.lower() == "asc":
            query = query.order_by(column.asc())
        else:
            query = query.order_by(column.desc())
        return query

    async def __get_conditions(self, **kwargs):
        """
        Generate conditions for filtering based on provided keyword arguments.
        Supports Ransack-like operators (field__operator=value).
        """
        conditions = []
        for key, value in kwargs.items():
            # keyに "__" が含まれていれば、フィールド名と演算子を分割する
            if "__" in key:
                field_name, op = key.split("__", 1)
                column = getattr(self.model, field_name, None)
                if column is None:
                    raise AttributeError(
                        f"{self.model.__name__} has no attribute '{field_name}'"
                    )

                operator_func = OPERATORS.get(op)
                if not operator_func:
                    raise ValueError(f"Unsupported operator '{op}' in '{key}'")

                conditions.append(operator_func(column, value))
            else:
                # "__"が含まれていない場合は eq (=) 比較とみなす
                column = getattr(self.model, key, None)
                if column is None:
                    raise AttributeError(
                        f"{self.model.__name__} has no attribute '{key}'"
                    )
                conditions.append(column == value)

        return conditions

    async def create(self, **kwargs):
        """
        Generic create method that instantiates the model,
        saves it, and returns the new instance.
        """
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance