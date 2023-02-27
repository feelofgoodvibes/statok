"""
This file contains all fixtures for tests
"""

import pytest
import os
from flask_sqlalchemy import SQLAlchemy

from statok_app.app import create_test_app
from statok_app.models.database import db
from statok_app.models.category import Category, CategoryType
from statok_app.models.operation import Operation


MYSQL_USER = os.environ.get("MYSQL_USER")
MYSQL_PASS = os.environ.get("MYSQL_PASS")
MYSQL_DBNAME = "statok_test"


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
        ])

        db.session.commit()

        db.session.add_all([
            Operation(value=100, category_id=3),
            Operation(value=50, category_id=1),
            Operation(value=75, category_id=1),
            Operation(value=250, category_id=4),
            Operation(value=15, category_id=5),
            Operation(value=75, category_id=6),
            Operation(value=5, category_id=6),
            Operation(value=10, category_id=2)
        ])

        yield db
        db.session.remove()
        db.drop_all()