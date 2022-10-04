import importlib
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import FastAPI, Request
from pydantic import BaseSettings
from decouple import config
from fastapi.responses import JSONResponse
from api.routes import __all__
from api.responses.response import HttpApiStandardResponse, StandardJsonResponse

# initialing fast api App
app = FastAPI()
# registering all routes
for route in __all__:
    module = importlib.import_module(name = 'api.routes.' + route)
    app.include_router(module.router)


# in production, you can use Settings management
# from pydantic to get secret key from .env
class Settings(BaseSettings):
    authjwt_secret_key: str = config('JWT_SECRET')
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {"access", "refresh"}


# callback to get your configuration
@AuthJWT.load_config
def get_config():
    return Settings()


# exception handler for auth_jwt
# in production, you can tweak performance using orjson response
@app.exception_handler(AuthJWTException)
def auth_jwt_exception_handler(req: Request, exc: AuthJWTException):
    return StandardJsonResponse(
        code = 401,
        response = HttpApiStandardResponse(message = 'This token has been expired or invalid')
    )


@app.get('/')
def check_api():
    return {
        'message': 'API working fine'
    }
