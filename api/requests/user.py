from enum import Enum
from pydantic import BaseModel, EmailStr


class UserTypeEnum(str, Enum):
    doctor = 'doctor'
    patient = 'patient'


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    mobile_number: str
    user_type: UserTypeEnum
