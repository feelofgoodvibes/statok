"""
This file contains all fixtures for tests
"""

import pytest
from flask_sqlalchemy import SQLAlchemy
from flask.testing import FlaskClient

from statok_app.app import create_test_app
from statok_app.models.database import db
from statok_app.models.category import Category, CategoryType
from statok_app.models.operation import Operation

from statok_app.rest.api import api_blueprint


@pytest.fixture()
def test_db() -> SQLAlchemy:
    """Clean testing database as fixture"""

    test_app = create_test_app()
    test_app.config["TESTING"] = True

    with test_app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def dummy_db() -> SQLAlchemy:
    """Testing database with test data as fixture"""

    test_app = create_test_app()
    test_app.config["TESTING"] = True

    with test_app.app_context():
        db.create_all()
        db.session.add_all([
            Category(name="Other", type=CategoryType.INCOME),
            Category(name="Other", type=CategoryType.EXPENSE),
            Category(name="Salary", type=CategoryType.INCOME),
            Category(name="Transaction", type=CategoryType.INCOME),
            Category(name="Food", type=CategoryType.EXPENSE),
            Category(name="Transaction", type=CategoryType.EXPENSE),
            Category(name="Books", type=CategoryType.EXPENSE),
        ])

        db.session.commit()

        db.session.add_all([
            Operation(value=100, category_id=3, date='2023-02-20 12:00:00'),
            Operation(value=50, category_id=1, date='2023-02-20 13:00:00'),
            Operation(value=75, category_id=1, date='2023-02-20 14:00:00'),
            Operation(value=250, category_id=4, date='2023-02-20 15:00:00'),
            Operation(value=15, category_id=5, date='2023-02-20 16:00:00'),
            Operation(value=75, category_id=6, date='2023-02-20 17:00:00'),
            Operation(value=5, category_id=6, date='2023-02-20 18:00:00'),
            Operation(value=10, category_id=2, date='2023-02-20 19:00:00')
        ])

        yield db
        db.session.remove()
        db.drop_all()



@pytest.fixture()
def api_client() -> FlaskClient:
    """Testing database with test data as fixture"""

    test_app = create_test_app()
    test_app.config["TESTING"] = True
    test_app.register_blueprint(api_blueprint, url_prefix="/api")

    with test_app.app_context():
        db.create_all()
        db.session.add_all([
            Category(name="Other", type=CategoryType.INCOME),
            Category(name="Other", type=CategoryType.EXPENSE),
            Category(name="Salary", type=CategoryType.INCOME),
            Category(name="Transaction", type=CategoryType.INCOME),
            Category(name="Food", type=CategoryType.EXPENSE),
            Category(name="Transaction", type=CategoryType.EXPENSE),
            Category(name="Books", type=CategoryType.EXPENSE),
        ])

        db.session.commit()

        db.session.add_all([
            Operation(value=100, category_id=3, date='2023-02-20 12:00:00'),
            Operation(value=50, category_id=1, date='2023-02-20 13:00:00'),
            Operation(value=75, category_id=1, date='2023-02-20 14:00:00'),
            Operation(value=250, category_id=4, date='2023-02-20 15:00:00'),
            Operation(value=15, category_id=5, date='2023-02-20 16:00:00'),
            Operation(value=75, category_id=6, date='2023-02-20 17:00:00'),
            Operation(value=5, category_id=6, date='2023-02-20 18:00:00'),
            Operation(value=10, category_id=2, date='2023-02-20 19:00:00')
        ])

        with test_app.test_client() as client:
            yield client

        db.session.remove()
        db.drop_all()
