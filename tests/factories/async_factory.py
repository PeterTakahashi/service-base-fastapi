import factory


class AsyncSQLAlchemyModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    """
    SQLAlchemyModelFactory の非同期版
    factory
    """

    class Meta:
        abstract = True
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    @classmethod
    async def _create(cls, model_class, *args, **create_params):
        """
        factory_boy が `create()` するときに呼ばれるメソッドをオーバーライド。
        非同期で session.add & commit する。
        """
        # cls._meta からセッションを取得する想定
        session = cls._meta.session
        if session is None:
            raise ValueError("No session provided in factory Meta.")

        # モデルを初期化
        obj = model_class(*args, **create_params)

        # 非同期セッションに追加 → commit → refresh
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    @classmethod
    async def create_batch(cls, size: int, **create_params):  # type: ignore
        return [await cls.create(**create_params) for _ in range(size)]
