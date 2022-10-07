from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from services.user import *
from fastapi.security import HTTPBearer
from api.responses.response import ApiResponse
from api.responses.user import *

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


@router.post('/login', response_model = ApiResponse[UserLoginResponse])
async def login(user_login: UserLogin, Authorize: AuthJWT = Depends()):
    user = validate_credentials(user_login)
    user_response = UserLoginResponse(
        access_token = Authorize.create_access_token(subject = user.id),
        refresh_token = Authorize.create_refresh_token(subject = user.id),
        user = user
    )
    return ApiResponse[UserLoginResponse](data = user_response, message = "You have logged in successfully")


@router.post('/refresh', dependencies = [Depends(HTTPBearer())], response_model = ApiResponse[RefreshTokenResponse])
async def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    token = RefreshTokenResponse(access_token = Authorize.create_access_token(subject = current_user))
    return ApiResponse[RefreshTokenResponse](data = token, message = "Your token refreshed successfully ")


@router.post('/logout', dependencies = [Depends(HTTPBearer())], response_model = ApiResponse)
async def refresh_revoke(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    jti = Authorize.get_raw_jwt()['jti']
    denylist.add(jti)
    return ApiResponse(message = "Access token has been revoked")


@router.post('/register')
async def register_user(user: UserRegister):
    p = create_user(user)
    return {'a': p}
    # return StandardJsonResponse(200, User)
