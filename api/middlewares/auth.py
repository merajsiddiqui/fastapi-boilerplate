from fastapi import Request, Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT


class JWTBearer(HTTPBearer):

    def __init__(self, auto_error: bool = False):
        super(JWTBearer, self).__init__(auto_error = auto_error)

    async def __call__(self, request: Request, Authorize: AuthJWT = Depends()):
        Authorize.jwt_required()
