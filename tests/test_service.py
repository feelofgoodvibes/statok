import pytest
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from statok_app.service import category as service_category
from statok_app.service import operation as service_operation
from statok_app.models.category import Category, CategoryType
from statok_app.models.operation import Operation

from tests.fixtures import dummy_db

# ------------ Category tests ------------

def test_get_categories(dummy_db: SQLAlchemy):
    categories = service_category.get_all_categories(dummy_db).all()
    assert len(categories) == 7


def test_get_categories_by_type(dummy_db: SQLAlchemy):
    categories_str = service_category.get_all_categories(dummy_db, "income").all()
    assert len(categories_str) == 3

    categories_int = service_category.get_all_categories(dummy_db, 2).all()
    assert len(categories_int) == 4

    categories_type = service_category.get_all_categories(dummy_db, CategoryType.INCOME).all()
    assert len(categories_type) == 3


def test_get_categories_wrong_type(dummy_db: SQLAlchemy):
    with pytest.raises(ValueError):
        service_category.get_all_categories(dummy_db, 5).all()

def test_get_category(dummy_db: SQLAlchemy):
    category = service_category.get_category(dummy_db, 5)

    assert category.id == 5
    assert category.name == "Food"


def test_create_category(dummy_db: SQLAlchemy):
    categories_before = service_category.get_all_categories(dummy_db).all()
    category = service_category.create_category(dummy_db, "TestName", CategoryType.EXPENSE)
    dummy_db.session.commit()
    categories_after = service_category.get_all_categories(dummy_db).all()

    assert category.id == 8
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
    TARGET_CATEGORY = 6

    categories_before = service_category.get_all_categories(dummy_db).all()
    operation_in_category = dummy_db.session.query(Operation).filter(Operation.category_id==TARGET_CATEGORY).all()
    
    service_category.delete_category(dummy_db, TARGET_CATEGORY)
    dummy_db.session.commit()
    
    categories_after = service_category.get_all_categories(dummy_db).all()
    deleted_category = service_category.get_category(dummy_db, TARGET_CATEGORY)

    assert len(categories_before) - len(categories_after) == 1
    assert deleted_category is None

    for operation in operation_in_category:
        assert operation.category_id in (1, 2)


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
        service_category.update_category(dummy_db, 15, "NewName")


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


# ------------ Operations tests ------------

def test_get_all_operations(dummy_db: SQLAlchemy):
    operations = service_operation.get_all_operations(dummy_db).all()
    assert len(operations) == 8


def test_get_all_operations_filter_date_from(dummy_db: SQLAlchemy):
    filters = { "date_from": "2023-02-20 16:00:00" }

    date_from = datetime.strptime(filters["date_from"], service_operation.OPERATION_DATE_FORMAT)
    operations = service_operation.get_all_operations(dummy_db, filters=filters).all()

    for operation in operations:
        assert operation.date >= date_from

    assert len(operations) == 4


def test_get_all_operations_filter_date_to(dummy_db: SQLAlchemy):
    filters = { "date_to": "2023-02-20 14:00:00" }

    date_to = datetime.strptime(filters["date_to"], service_operation.OPERATION_DATE_FORMAT)
    operations = service_operation.get_all_operations(dummy_db, filters=filters).all()

    for operation in operations:
        assert operation.date <= date_to
        
    assert len(operations) == 3


def test_get_all_operations_filter_date(dummy_db: SQLAlchemy):
    filters = {
        "date_from": "2023-02-20 13:30:00",
        "date_to": "2023-02-20 17:45:00"
    }

    date_from = datetime.strptime(filters["date_from"], service_operation.OPERATION_DATE_FORMAT)
    date_to = datetime.strptime(filters["date_to"], service_operation.OPERATION_DATE_FORMAT)
    operations = service_operation.get_all_operations(dummy_db, filters=filters).all()
    
    for operation in operations:
        assert date_from <= operation.date <= date_to
        
    assert len(operations) == 4


def test_get_all_operations_filter_category_id(dummy_db: SQLAlchemy):
    filters = { "category_id": 1 }

    operations = service_operation.get_all_operations(dummy_db, filters=filters).all()
    
    assert len(operations) == 2
    for operation in operations:
        assert operation.category.id == filters["category_id"]


def test_get_all_operations_filter_operation_type(dummy_db: SQLAlchemy):
    filters = {"type": "income"}

    operations = service_operation.get_all_operations(dummy_db, filters=filters).all()
    
    assert len(operations) == 4
    for operation in operations:
        assert operation.category.type == CategoryType.INCOME


def test_get_all_operations_filter_complex(dummy_db: SQLAlchemy):
    filters = {
        "type": "expense",
        "date_from": "2023-02-20 16:10:00",
        "date_to": "2023-02-20 18:40:00"
    }

    date_from = datetime.strptime(filters["date_from"], service_operation.OPERATION_DATE_FORMAT)
    date_to = datetime.strptime(filters["date_to"], service_operation.OPERATION_DATE_FORMAT)
    operations = service_operation.get_all_operations(dummy_db, filters=filters).all()
    
    assert len(operations) == 2

    for operation in operations:
        assert date_from <= operation.date <= date_to
        assert operation.category.type == CategoryType.EXPENSE


def test_get_all_operations_wrong_date_from(dummy_db: SQLAlchemy):
    filters = { "date_from": "2023-02-XX 14:00:00" }

    with pytest.raises(ValueError):
        service_operation.get_all_operations(dummy_db, filters=filters).all()


def test_get_all_operations_wrong_date_to(dummy_db: SQLAlchemy):
    filters = { "date_to": "2023-02-XX 14:00:00" }

    with pytest.raises(ValueError):
        service_operation.get_all_operations(dummy_db, filters=filters).all()


def test_get_all_operations_wrong_category_id(dummy_db: SQLAlchemy):
    filters = { "category_id": "2" }

    with pytest.raises(ValueError):
        service_operation.get_all_operations(dummy_db, filters=filters).all()


def test_get_all_operations_wrong_operation_type(dummy_db: SQLAlchemy):
    filters = { "type": "wrong-input" }

    with pytest.raises(ValueError):
        service_operation.get_all_operations(dummy_db, filters=filters).all()


def test_get_operation(dummy_db: SQLAlchemy):
    operation = service_operation.get_operation(dummy_db, 2)

    assert operation.id == 2
    assert operation.value == 50


def test_get_nonexisting_operation(dummy_db: SQLAlchemy):
    with pytest.raises(ValueError):
        service_operation.get_operation(dummy_db, 10)


def test_create_operation(dummy_db: SQLAlchemy):
    category = service_category.get_category(dummy_db, 1)
    operation = service_operation.create_operation(dummy_db, 12.50, category)
    dummy_db.session.commit()

    assert operation.value == 12.50
    assert operation.category == category
    assert len(service_operation.get_all_operations(dummy_db).all()) == 9


def test_create_operation_wrong_value_income(dummy_db: SQLAlchemy):
    category = service_category.get_category(dummy_db, 1)

    with pytest.raises(ValueError):
        service_operation.create_operation(dummy_db, -12.50, category)


def test_create_operation_wrong_value_expense(dummy_db: SQLAlchemy):
    category = service_category.get_category(dummy_db, 2)

    with pytest.raises(ValueError):
        service_operation.create_operation(dummy_db, 12.50, category)


def test_create_operation_value_too_large(dummy_db: SQLAlchemy):
    category = service_category.get_category(dummy_db, 1)

    with pytest.raises(ValueError):
        service_operation.create_operation(dummy_db, service_operation.OPERATION_MAX_VALUE+1, category)


def test_delete_operation(dummy_db: SQLAlchemy):
    service_operation.delete_operation(dummy_db, 1)
    dummy_db.session.commit()

    assert len(service_operation.get_all_operations(dummy_db).all()) == 7


def test_update_operation_value(dummy_db: SQLAlchemy):
    updated_operation = service_operation.update_operation(dummy_db, 1, value=500.00)
    dummy_db.session.commit()

    assert updated_operation.value == 500.00


def test_update_operation_category(dummy_db: SQLAlchemy):
    new_category = service_category.get_category(dummy_db, 4)
    updated_operation = service_operation.update_operation(dummy_db, 1, category=new_category)
    dummy_db.session.commit()

    assert updated_operation.category.id == 4


def test_update_operation_value_and_category(dummy_db: SQLAlchemy):
    new_category = service_category.get_category(dummy_db, 4)
    updated_operation = service_operation.update_operation(dummy_db, 1, value=500.00, category=new_category)
    dummy_db.session.commit()

    assert updated_operation.category.id == 4
    assert updated_operation.value == 500


def test_update_operation_wrong_category(dummy_db: SQLAlchemy):
    new_category = service_category.get_category(dummy_db, 4)

    with pytest.raises(ValueError):
        service_operation.update_operation(dummy_db, 6, category=new_category)


def test_update_operation_wrong_value_for_income(dummy_db: SQLAlchemy):
    with pytest.raises(ValueError):
        service_operation.update_operation(dummy_db, 1, value=-500.00)


def test_update_operation_wrong_value_for_income_2(dummy_db: SQLAlchemy):
    new_category = service_category.get_category(dummy_db, 4)

    with pytest.raises(ValueError):
        service_operation.update_operation(dummy_db, 1, value=-500.00, category=new_category)


def test_update_operation_wrong_value_for_expense(dummy_db: SQLAlchemy):
    with pytest.raises(ValueError):
        service_operation.update_operation(dummy_db, 5, value=500.00)


def test_update_operation_wrong_value_too_large(dummy_db: SQLAlchemy):
    with pytest.raises(ValueError):
        service_operation.update_operation(dummy_db, 1, value=service_operation.OPERATION_MAX_VALUE+1)


def test_update_operation_date(dummy_db: SQLAlchemy):
    new_date = "2022-02-02 02:02:02"

    updated_operation = service_operation.update_operation(dummy_db, 1, date=new_date)
    dummy_db.session.commit()

    assert (updated_operation.date.month
            == updated_operation.date.day
            == updated_operation.date.hour
            == updated_operation.date.minute
            == updated_operation.date.second
            == 2)


def test_update_operation_wrong_date(dummy_db: SQLAlchemy):
    new_date = "2022-02-XX 02:02:02"

    with pytest.raises(ValueError):
        service_operation.update_operation(dummy_db, 1, date=new_date)


def test_update_operation_empty(dummy_db: SQLAlchemy):
    service_operation.update_operation(dummy_db, 1)


def test_update_operation_full(dummy_db: SQLAlchemy):
    new_category = service_category.get_category(dummy_db, 4)
    new_date = "2022-02-02 02:02:02"

    updated_operation = service_operation.update_operation(dummy_db, 1, value=500.00, category=new_category, date=new_date)
    dummy_db.session.commit()

    assert updated_operation.category.id == 4
    assert updated_operation.value == 500
    assert (updated_operation.date.month
            == updated_operation.date.day
            == updated_operation.date.hour
            == updated_operation.date.minute
            == updated_operation.date.second
            == 2)
