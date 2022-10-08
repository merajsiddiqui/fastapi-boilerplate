from fastapi import Request, Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from services.user import get_user_by_id
from functools import wraps


class JWTBearer(HTTPBearer):

    def __init__(self, auto_error: bool = False):
        super(JWTBearer, self).__init__(auto_error = auto_error)

    async def __call__(self, request: Request, Authorize: AuthJWT = Depends()):
        Authorize.jwt_required()


def has_subscription(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        print(*args, 'her')
        # user = get_user_by_id(args(0).get_jwt_subject())
        # print(*args)
        pass

    return wrapper
