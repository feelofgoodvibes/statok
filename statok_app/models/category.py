from .database import Base
import enum
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship


class CategoryTypes(enum.Enum):
    income = 1
    expense = 2


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    type = Column(Enum(CategoryTypes), nullable=False)
    
    operations = relationship("Operation", back_populates="category")