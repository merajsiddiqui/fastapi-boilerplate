from enum import Enum
from pydantic import BaseModel, EmailStr
from typing import Optional


class UserTypeEnum(str, Enum):
    doctor = 'doctor'
    patient = 'patient'


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "merajsiddiqui@outlook.com",
                "password": "kota@9811"
            }
        }


class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    mobile_number: str
    user_type: UserTypeEnum
    registration_number: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "full_name": "Meraj Ahmad Siddiqui",
                "email": "merajsiddiqui@outlook.com",
                "password": "abc123",
                "mobile_number": "9990166950",
                "user_type": "patient"
            }
        }
