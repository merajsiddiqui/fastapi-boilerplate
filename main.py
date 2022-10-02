import importlib

from fastapi import FastAPI
from api.routes import __all__

# initialing fast api App
app = FastAPI()
# registering all routes
for route in __all__:
    t = importlib.import_module(name = 'api.routes.' + route)
    if route is not None:
        app.include_router(t.router)


@app.get('/')
def check_api():
    return {
        'message': 'API working fine'
    }
