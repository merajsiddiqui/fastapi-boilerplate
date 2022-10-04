from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer

router = APIRouter(prefix = '/user', dependencies = [Depends(HTTPBearer())], tags = ['User'])


@router.post('/profile')
async def profile(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    user = Authorize.get_jwt_subject()
    return {
        'user': user,
        'message': 'API working fine'
    }
