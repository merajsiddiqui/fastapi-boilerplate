from fastapi import APIRouter, HTTPException
from api.requests.user import *
from services.auth import *

router = APIRouter(prefix = '/auth', tags = ['Auth'])


@router.post('/login')
async def login(login_credentials: UserLogin):
    valid_credentials, token_or_message = validate_credentials(login_credentials.email, login_credentials.password)
    if valid_credentials:
        return {
            'access': token_or_message
        }
    else:
        raise HTTPException(status_code = 401, detail = token_or_message)


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
