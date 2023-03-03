# pylint: disable=wrong-import-position, cyclic-import, no-self-argument

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, validator, confloat
from statok_app.models.category import CategoryType, Category

from statok_app.schemas import json_encoders, OPERATION_DATE_FORMAT, OPERATION_MAX_VALUE


class OperationBase(BaseModel):
    """Base operation schema

    Fields
    ------
    * id : `int`
    * value : `float`
    * date : `datetime`
    """

    id: int
    value: float
    date: datetime

    class Config:
        """Pydantic model config"""

        orm_mode = True
        json_encoders = json_encoders


class Operation(OperationBase):
    """Full operation schema

    Fields
    ------
    * id : `int`
    * value : `float`
    * date : `datetime`
    * category : `CategoryBase`
    """

    category: "CategoryBase"


class OperationFilters(BaseModel):
    """Schema for parsing filter options for operation collection"""

    date_from: Optional[str]
    date_to: Optional[str]
    category_id: Optional[int]
    type: Optional[CategoryType]


    @validator("date_from", "date_to")
    def date_validation(value: str):
        """A validator for transforming numeric strings to int for parsing CategoryType"""

        try:
            datetime.strptime(value, OPERATION_DATE_FORMAT)
            return value
        except Exception as exc:
            raise ValueError("Filter date_from format should be: \"YYYY-MM-DD HH:MM:SS\"!") from exc


    @validator('type', pre=True)
    def type_str_to_int(cls, value):
        """A validator for transforming numeric strings to int for parsing CategoryType"""

        if isinstance(value, str) and value.isnumeric():
            return int(value)

        return value


from statok_app.schemas.category import CategoryBase
Operation.update_forward_refs()
