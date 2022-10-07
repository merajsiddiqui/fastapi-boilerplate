import importlib
import sys

from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseSettings
from decouple import config
from api.routes import __all__
from database import models
from api.responses.response import ApiResponse
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from doc import open_api_details
from config.database import db_engine

# initialing fast api App
app = FastAPI(**open_api_details)

models.Base.metadata.create_all(bind = db_engine)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

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
    return ApiResponse(message = "This token is invalid or expired", success = False)


# Global exception handler
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        error_code = 500
        error_message = 'Something went wrong, We Messed up, we will fix it'
        if len(e.args) == 2:
            error_code = e.args[0] if isinstance(e.args[0], int) else error_code
            error_message = e.args[1] if isinstance(e.args[1], str) else error_message
        if len(e.args) == 1:
            error_message = e.args[0] if isinstance(e.args[0], str) else error_message
        # you probably want some kind of logging here
        print(sys.exc_info())
        return JSONResponse(status_code = error_code, content = error_message)


app.middleware('http')(catch_exceptions_middleware)


@app.get('/')
def check_api():
    return {
        'message': 'API working fine'
    }


if __name__ == '__main__':
    uvicorn.run("main:app", host = '127.0.0.1', port = 8005, log_level = "info", reload = True)
    print("running")
