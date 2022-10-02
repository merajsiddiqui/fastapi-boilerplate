from fastapi import APIRouter, Depends
from api.middlewares.auth import JWTBearer

router = APIRouter(prefix = '/user', dependencies = [Depends(JWTBearer())], tags = ['User'])


@router.post('/profile')
async def profile():
    return {
        'message': 'API working fine'
    }
