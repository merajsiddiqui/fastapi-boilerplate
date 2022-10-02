from fastapi import APIRouter
from api.requests.user import *

router = APIRouter(prefix = '/auth', tags = ['Auth'])


@router.post('/login')
async def login(login_credentials: UserLogin):
    return {
        'payload': login_credentials
    }


@router.post('/register')
async def register(user_details: UserRegister):
    return {
        'message': 'API working fine'
    }


@router.post('/logout')
async def logout():
    return {
        'message': 'API working fine'
    }
