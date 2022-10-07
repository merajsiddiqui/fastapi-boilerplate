from typing import Generic, Optional, TypeVar
from pydantic.generics import GenericModel

DataType = TypeVar("DataType")


class ApiResponse(GenericModel, Generic[DataType]):
    success: bool = True
    message: str = ""
    data: Optional[DataType] = None

    class Config:
        allow_population_by_field_name = True
