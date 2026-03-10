from sqlalchemy import Column, Integer, String
from src.database import Base


class User(Base):
    __tablename__ = "auth_user"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(150), unique=True, nullable=False)
    email = Column(String(254), unique=True, nullable=False)
    password = Column(String(128), nullable=False)

    first_name = Column(String(150), nullable=True)
    second_name = Column(String(150), nullable=True)
