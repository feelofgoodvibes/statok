import pytest
from flask_sqlalchemy import SQLAlchemy

from statok_app.service import category as service_category
from statok_app.models.category import Category, CategoryType
from statok_app.models.operation import Operation

from test_fixtures import dummy_db


def test_get_categories(dummy_db: SQLAlchemy):
    assert len(service_category.get_all_categories(dummy_db)) == 6


def test_get_category(dummy_db: SQLAlchemy):
    category = service_category.get_category(dummy_db, 5)

    assert category.id == 5
    assert category.name == "Food"


def test_create_category(dummy_db: SQLAlchemy):
    categories_before = service_category.get_all_categories(dummy_db)
    category = service_category.create_category(dummy_db, "TestName", CategoryType.EXPENSE)
    dummy_db.session.commit()
    categories_after = service_category.get_all_categories(dummy_db)

    assert category.id == 7
    assert category.name == "TestName"
    assert len(categories_after) - len(categories_before) == 1


def test_create_category_wrong_type(dummy_db: SQLAlchemy):
    with pytest.raises(ValueError):
        service_category.create_category(dummy_db, "Test", "income")


def test_create_category_name_maxlen(dummy_db: SQLAlchemy):
    with pytest.raises(ValueError):
        service_category.create_category(dummy_db, "super-ultra-very-very-very-very-very-longcategoryname", CategoryType.INCOME)


def test_create_same_category(dummy_db: SQLAlchemy):
    service_category.create_category(dummy_db, "Test", CategoryType.INCOME)

    with pytest.raises(ValueError):
        service_category.create_category(dummy_db, "Test", CategoryType.INCOME)


def test_delete_category(dummy_db: SQLAlchemy):
    categories_before = service_category.get_all_categories(dummy_db)
    category = service_category.delete_category(dummy_db, 3)
    dummy_db.session.commit()
    categories_after = service_category.get_all_categories(dummy_db)

    deleted_category = service_category.get_category(dummy_db, 3)

    assert len(categories_before) - len(categories_after) == 1
    assert deleted_category is None


def test_delete_nonexisting_category(dummy_db: SQLAlchemy):
    with pytest.raises(ValueError):
        service_category.delete_category(dummy_db, 8)


def test_delete_default_category(dummy_db: SQLAlchemy):
    with pytest.raises(ValueError):
        service_category.delete_category(dummy_db, 1)

    with pytest.raises(ValueError):
        service_category.delete_category(dummy_db, 2)


def test_delete_category_operations(dummy_db: SQLAlchemy):
    deleted_operations = service_category.delete_category_operations(dummy_db, 6)
    dummy_db.session.commit()
    category_operations_after = service_category.get_category(dummy_db, 6).operations

    assert len(deleted_operations) == 2
    assert len(category_operations_after) == 0
    

def test_update_category(dummy_db: SQLAlchemy):
    category = service_category.get_category(dummy_db, 4)    
    service_category.update_category(dummy_db, 4, "NewName")
    dummy_db.session.commit()

    assert category.name == "NewName"


def test_update_nonexisting_category(dummy_db: SQLAlchemy):
    with pytest.raises(ValueError):
        service_category.update_category(dummy_db, 7, "NewName")


def test_update_category_name_maxlen(dummy_db: SQLAlchemy):
    with pytest.raises(ValueError):
        service_category.update_category(dummy_db, 3, "super-ultra-very-very-very-very-very-longcategoryname")


def test_update_default_category_error(dummy_db: SQLAlchemy):
    with pytest.raises(ValueError):
        service_category.update_category(dummy_db, 1, "Test")

    with pytest.raises(ValueError):
        service_category.update_category(dummy_db, 2, "Test")


def test_get_categories_report(dummy_db: SQLAlchemy):
    stats = service_category.get_categories_stats(dummy_db)

    assert len(stats) == 6
    assert stats[1] == {"name": "Other", "type": CategoryType.INCOME, "total": 125, "operations": 2}
    assert stats[3] == {"name": "Salary", "type": CategoryType.INCOME, "total": 100, "operations": 1}
    assert stats[6] == {"name": "Transaction", "type": CategoryType.EXPENSE, "total": 80, "operations": 2}
