from datetime import datetime, timedelta
import time
from enum import Enum
from typing import Union, Any
from jose import jwt
from decouple import config
from pydantic.main import BaseModel


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class TokenType(str, Enum):
    ACCESS_TOKEN = 'JWT_ACCESS_TOKEN_EXPIRE_MINUTES'
    REFRESH_TOKEN = 'JWT_REFRESH_TOKEN_EXPIRE_MINUTES'


def decode_jwt(token: str) -> TokenPayload | None:
    try:
        decoded_token = jwt.decode(token, config('JWT_SECRET'), algorithms = [config('JWT_ALGORITHM')])
        return TokenPayload(**decoded_token) if decoded_token["exp"] >= time.time() else None
    except jwt.JWTError:
        return None


def verify_jwt(jwt_token: str) -> bool:
    is_valid_token: bool = False

    try:
        payload = decode_jwt(jwt_token)
    except jwt.JWTError:
        payload = None
    if payload:
        is_valid_token = True
    return is_valid_token


def create_token(subject: Union[str, Any], token_type, expires_delta: int = None) -> str:
    if not isinstance(token_type, TokenType):
        raise Exception('invalid token type provided')
    expires_delta = datetime.utcnow() + expires_delta if expires_delta is not None else datetime.utcnow() + timedelta(
        minutes = float(config(token_type)))
    payload = {"exp": expires_delta, "sub": str(subject)}
    return jwt.encode(claims = payload, key = config('JWT_SECRET'), algorithm = config('JWT_ALGORITHM'))
