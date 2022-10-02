from typing import Any
from pydantic import BaseModel

custom_encoder = lambda obj: dict(_type = type(obj).__name__, **obj.dict())


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
        json_encoders = {

        }
