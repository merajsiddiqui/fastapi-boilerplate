from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from utils.jwt import verify_jwt, decode_jwt


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


reusable_oauth = OAuth2PasswordBearer(tokenUrl = "/login", scheme_name = "JWT")


async def get_current_user(token: str = Depends(reusable_oauth)):
    token_payload = decode_jwt(token)
    if token_payload is None:
        raise HTTPException(status_code = 401, detail = "unable to verify authorization token")
    return token_payload.sub
# here You can get data and return the user
