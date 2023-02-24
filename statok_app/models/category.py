import enum
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from .database import Base


class CategoryType(enum.Enum):
    """Types of category

    Possible Values
    ---------------
    - `income`
    - `expense`
    """

    INCOME = 1
    EXPENSE = 2


class Category(Base):
    """Model which describes category

    Init fields
    -----------
    - name : `str(50)`
        * name of the category
    - type : `CategoryType`
        * type of the category

    Other fields
    ------------
    - id : `int`
        * ID of the category
    - operations : `list[Operation]`
        * list of the operations within category 
    """

    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    type = Column(Enum(CategoryType), nullable=False)

    operations = relationship("Operation", back_populates="category")
