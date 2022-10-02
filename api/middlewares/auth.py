import time
from jose import jwt
from decouple import config
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, config('JWT_SECRET'), algorithms = [config('JWT_ALGORITHM')])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except jwt.JWTError:
        return {}


def sign_jwt(user_id: str) -> str:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    return jwt.encode(claims = payload, key = config('JWT_SECRET'), algorithm = config('JWT_ALGORITHM'))


def verify_jwt(jwt_token: str) -> bool:
    is_valid_token: bool = False

    try:
        payload = decode_jwt(jwt_token)
    except jwt.JWTError:
        payload = None
    if payload:
        is_valid_token = True
    return is_valid_token


class JWTBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error = auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code = 403, detail = "Invalid authentication scheme.")
            if not verify_jwt(credentials.credentials):
                raise HTTPException(status_code = 403, detail = "Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code = 403, detail = "Invalid authorization code.")
