from pydantic import BaseModel
from database.models.user import User
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

UserModel = sqlalchemy_to_pydantic(db_model = User, exclude = ['password', 'updated_at', 'deleted_at'])


class UserLoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: UserModel

    class Config:
        schema_extra = {
            "access_token": "",
            "refresh_token": "",
            "user_detail": {}
        }


class RefreshTokenResponse(BaseModel):
    access_token: str
