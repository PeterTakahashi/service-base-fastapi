from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from app.db.base import Base
from app.models.oauth_account import OAuthAccount
from sqlalchemy.orm import relationship, Mapped
from typing import List

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"
    oauth_accounts: Mapped[List[OAuthAccount]] = relationship("OAuthAccount", lazy="joined")
