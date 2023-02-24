import os
from datetime import datetime
import pytz

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from statok_app.models.database import Base
from statok_app.models.category import Category, CategoryType
from statok_app.models.operation import Operation, get_current_time


MYSQL_USER = os.environ.get("MYSQL_USER")
MYSQL_PASS = os.environ.get("MYSQL_PASS")
DB_NAME = "statok_test"

@pytest.fixture
def database_session() -> Session:
    engine = create_engine(f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASS}@localhost/{DB_NAME}")
    Base.metadata.drop_all(bind=engine)

    print("Creating all tables")
    Base.metadata.create_all(bind=engine)
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    yield session

    print("Rollback session")
    session.rollback()
    print("Dropping all tables")
    Base.metadata.drop_all(bind=engine)


def test_db_insert_category(database_session: Session):
    new_category = Category(name="Test", type=CategoryType.INCOME)

    database_session.add(new_category)
    database_session.commit()

    query_obj = database_session.query(Category).first()

    assert query_obj.name == "Test"
    assert query_obj.type == CategoryType.INCOME


def test_db_insert_operation(database_session: Session):
    new_category = Category(name="Test", type=CategoryType.INCOME)

    database_session.add(new_category)
    database_session.commit()

    new_operation = Operation(value=42, category_id=new_category.id)

    database_session.add(new_operation)
    database_session.commit()

    query_obj = database_session.query(Operation).first()

    assert query_obj.id == 1
    assert query_obj.value == 42
    assert query_obj.category.type == CategoryType.INCOME


def test_db_get_current_time():
    time = get_current_time()
    time_now = datetime.now(tz=pytz.timezone("Europe/Kyiv"))

    assert time.time() == time_now.time()
    assert time.date() == time_now.date()
