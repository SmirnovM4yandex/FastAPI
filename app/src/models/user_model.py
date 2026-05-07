from sqlalchemy import Column, Integer, String, DateTime, Boolean

from src.database import Base


class User(Base):
    __tablename__ = "auth_user"

    id = Column(Integer, primary_key=True)

    username = Column(String(150), unique=True, nullable=False)

    email = Column(String(254), unique=True, nullable=False)

    password = Column(String(128), nullable=False)

    first_name = Column(String(150), nullable=False, default="")

    last_name = Column(String(150), nullable=False, default="")

    last_login = Column(DateTime, nullable=True)

    date_joined = Column(DateTime, nullable=False)

    is_superuser = Column(Boolean, nullable=False, default=False)

    is_staff = Column(Boolean, nullable=False, default=False)

    is_active = Column(Boolean, nullable=False, default=True)