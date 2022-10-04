from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from api.middlewares.auth import JWTBearer


router = APIRouter(prefix = '/user', dependencies = [Depends(JWTBearer())], tags = ['User'])


@router.post('/profile')
async def profile(Authorize: AuthJWT = Depends()):
    user = Authorize.get_jwt_subject()
    return {
        'user': user,
        'message': 'API working fine'
    }
