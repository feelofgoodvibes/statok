# pylint: disable=wrong-import-position, cyclic-import, no-self-argument

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, validator
from statok_app.models.category import CategoryType

from statok_app.schemas import json_encoders, OPERATION_DATE_FORMAT


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
    """Model for parsing filter options for operation collection"""

    date_from: Optional[str]
    date_to: Optional[str]
    category_id: Optional[int]
    type: Optional[CategoryType]

    @validator("date_from", "date_to")
    def date_validation(cls, value):
        """A validator for transforming numeric strings to int for parsing CategoryType"""

        try:
            return datetime.strptime(value, OPERATION_DATE_FORMAT)
        except Exception as exc:
            raise ValueError("Filter date_from format should be: \"YYYY-MM-DD HH:MM:SS\"!") from exc


from statok_app.schemas.category import CategoryBase
Operation.update_forward_refs()
