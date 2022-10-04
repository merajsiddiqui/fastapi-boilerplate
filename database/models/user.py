from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from config.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column('id', Integer, primary_key = True, autoincrement = True)
    name = Column('name', String(50))
    email = Column('email', String(100), unique = True)
    password = Column('password', String(100), nullable = False)
    mobile_number = Column('mobile_number', String(11), nullable = False)
    profile_image = Column('profile_image', Text)
    user_type = Column('user_type', String)
    created_at = Column('created_at', DateTime, default = func.now())
    updated_at = Column('updated_at', DateTime, nullable = True, onupdate = func.now())
    deleted_at = Column('deleted_at', DateTime, nullable = True)
