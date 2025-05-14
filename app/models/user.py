from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from app.db.base import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"
