from datetime import datetime
import pytz
from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


def get_current_time():
    """Get current time without tzinfo"""

    return datetime.now(tz=pytz.timezone("Europe/Kyiv")).replace(tzinfo=None)


class Operation(Base):
    """Model which describes operation

    Init fields
    -----------
    - value : `int`
        * Value of the operation (for income operation should be >= 0, for expense operation < 0)
    - category_id : `int`
        * ID of the category of operation

    Other fields
    ------------
    - id : `int`
        * ID of the operation
    - date : `datetime.datetime`
        * Datetime of the operation
    - category : `Category`
        * Category of the operation
    """

    __tablename__ = "operation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Numeric(13, 4), nullable=False, unique=False)
    date = Column(DateTime, default=get_current_time)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False, default=0)

    category = relationship("Category", back_populates="operations")
