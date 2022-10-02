from fastapi import APIRouter


router = APIRouter(prefix = '/user', tags = ['User'])


@router.post('/profile')
async def profile():
    return {
        'message': 'API working fine'
    }

