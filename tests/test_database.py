from datetime import datetime
import pytz
from flask_sqlalchemy import SQLAlchemy

from statok_app.models.category import Category, CategoryType
from statok_app.models.operation import Operation, get_current_time

from test_fixtures import test_db, dummy_db


def test_db_insert_category(test_db: SQLAlchemy):
    new_category = Category(name="Test", type=CategoryType.INCOME)

    test_db.session.add(new_category)
    test_db.session.commit()

    query_obj = test_db.session.query(Category).first()

    assert query_obj.name == "Test"
    assert query_obj.type == CategoryType.INCOME


def test_db_insert_operation(test_db: SQLAlchemy):
    new_category = Category(name="Test", type=CategoryType.INCOME)

    test_db.session.add(new_category)
    test_db.session.commit()

    new_operation = Operation(value=42, category_id=new_category.id)

    test_db.session.add(new_operation)
    test_db.session.commit()

    query_obj = test_db.session.query(Operation).first()

    assert query_obj.id == 1
    assert query_obj.value == 42
    assert query_obj.category.type == CategoryType.INCOME


def test_db_get_current_time():
    time = get_current_time()
    time_now = datetime.now(tz=pytz.timezone("Europe/Kyiv"))

    assert time.hour == time_now.hour
    assert time.minute == time_now.minute
    assert time.year == time_now.year
    assert time.month == time_now.month
    assert time.day == time_now.day
