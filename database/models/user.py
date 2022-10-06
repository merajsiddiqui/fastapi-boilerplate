import bcrypt
from sqlalchemy.sql import func
from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean


class User(Base):
    __tablename__ = 'users'

    id = Column('id', Integer, primary_key = True, autoincrement = True)
    name = Column('name', String(50))
    email = Column('email', String(100), unique = True)
    email_verified = Column('email_verified', Boolean, default = False)
    password = Column('password', String(100), nullable = True)
    mobile_number = Column('mobile_number', String(11), nullable = False)
    mobile_verified = Column('mobile_verified', Boolean, default = False)
    profile_image = Column('profile_image', Text)
    user_type = Column('user_type', String)
    created_at = Column('created_at', DateTime, default = func.now())
    updated_at = Column('updated_at', DateTime, nullable = True, onupdate = func.now())
    deleted_at = Column('deleted_at', DateTime, nullable = True)

    def __init__(self, password, **kwargs):
        password_hash = self.generate_hash(password)
        super().__init__(password = password_hash, **kwargs)

    @staticmethod
    def generate_hash(password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf8'), salt).decode('utf8')

    def validate_password(self, plain_password):
        return bcrypt.checkpw(plain_password.encode('utf8'), self.password.encode('utf8'))
