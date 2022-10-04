from typing import Any
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


class HttpApiStandardResponse(BaseModel):
    success: bool = False
    message: str = 'Api Request successful'
    data: Any = {}

    class Config:
        schema_extra = {
            "example": {
                "success": False,
                "message": "Unable to Authorize user",
                "data": []
            }
        }


class StandardJsonResponse(JSONResponse):
    def __init__(self, code: int, response: Any):
        super().__init__(status_code = code, content = jsonable_encoder(response))
