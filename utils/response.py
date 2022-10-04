from fastapi import Response, status
from typing import Any
from fastapi.encoders import jsonable_encoder


class ResponseConvert:

    def __init__(self, message: Any, code: int = 200):
        pass
