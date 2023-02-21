from .database import Base
from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import pytz

def default_operation_date():
    return datetime.now(tz=pytz.timezone("Europe/Kyiv")).replace(tzinfo=None)


class Operation(Base):
    __tablename__ = "operation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Numeric(13, 4), nullable=False, unique=False)
    date = Column(DateTime, default=default_operation_date)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False, default=0)

    category = relationship("Category", back_populates="operations")