# pylint: disable=wrong-import-position, cyclic-import, no-self-argument

from pydantic import BaseModel
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


from statok_app.schemas.operation import OperationBase
Category.update_forward_refs()
