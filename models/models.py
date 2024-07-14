from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, TIMESTAMP
from sqlalchemy.orm import declarative_base, mapped_column

Base = declarative_base()


class Users(Base):
    """Таблица пользователя"""
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    username: str = Column(String, nullable=True, unique=True)
    phone: str = Column(String, nullable=True, unique=True)
    email: str = Column(String, nullable=True, unique=True)
    register_data: datetime.utcnow = Column(TIMESTAMP, default=datetime.utcnow())
    hashed_password: str = Column(String, nullable=True)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
