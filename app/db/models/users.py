from sqlalchemy import Boolean, Column, Integer, String
from ..base import Base


class Users(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    phone_number = Column(String)
    role = Column(String)
    is_active = Column(Boolean)
