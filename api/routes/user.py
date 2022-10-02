from fastapi import APIRouter, Depends
from api.middlewares.auth import JWTBearer, get_current_user

router = APIRouter(prefix = '/user', dependencies = [Depends(JWTBearer())], tags = ['User'])


@router.post('/profile')
async def profile(user = Depends(get_current_user)):
    return {
        'user': user,
        'message': 'API working fine'
    }
