from fastapi import APIRouter, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT
from services.user import *
from fastapi.security import HTTPBearer


router = APIRouter(prefix = '/auth', tags = ['Auth'])

denylist = set()


# For this example, we are just checking if the tokens jti
# (unique identifier) is in the denylist set. This could
# be made more complex, for example storing the token in Redis
# with the value true if revoked and false if not revoked
@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in denylist


@router.post('/login')
async def login(user: UserLogin, Authorize: AuthJWT = Depends()):
    user = validate_credentials(user)
    if user is None:
        raise HTTPException(status_code = 401, detail = "Bad username or password")
    # subject identifier for whom this token is for example id or username from database
    access_token = Authorize.create_access_token(subject = user.email)
    return {"access_token": access_token}


@router.post('/refresh',  dependencies = [Depends(HTTPBearer())],)
async def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject = current_user)
    return {"access_token": new_access_token}


@router.post('/logout', dependencies = [Depends(HTTPBearer())], )
async def refresh_revoke(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    jti = Authorize.get_raw_jwt()['jti']
    denylist.add(jti)
    return {"detail": "Access token has been revoked"}


@router.post('/register')
async def register_user(user: UserRegister):
    p = create_user(user)
    return {'a': p}
    # return StandardJsonResponse(200, User)
