# pylint: disable=wrong-import-position, cyclic-import, no-self-argument

from pydantic import BaseModel, validator, constr
from statok_app.schemas import json_encoders, CategoryType


class CategoryBase(BaseModel):
    """Base category schema
    Fields
    ------
    * id : `int`
    * name : `str`
    * type : `CategoryType`
    """

    id: int
    name: str
    type: CategoryType

    class Config:
        """Pydantic model config"""

        orm_mode = True
        json_encoders = json_encoders


class Category(CategoryBase):
    """Full category schema

    Fields
    ------
    * id : `int`
    * name : `str`
    * type : `CategoryType`
    * operations : `list[OperationBase]`
    """

    operations: "list[OperationBase]"


class CategoryCreate(BaseModel):
    """Category schema for POST creation

    Fields
    ------
    * name : `str`
    * type : `CategoryType`
    """

    name: constr(max_length=50)
    type: CategoryType

    @validator('type', pre=True)
    def type_str_to_int(cls, value):
        """A validator for transforming numeric strings to int for parsing CategoryType"""

        if isinstance(value, str) and value.isnumeric():
            return int(value)

        return value


from statok_app.schemas.operation import OperationBase
Category.update_forward_refs()
