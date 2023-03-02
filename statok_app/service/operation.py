from datetime import datetime
from pydantic import validate_arguments
from flask_sqlalchemy import SQLAlchemy

from statok_app.models.category import Category, CategoryType
from statok_app.models.operation import Operation
from statok_app.service import pydantic_config
from statok_app.schemas.operation import OperationFilters
from statok_app.schemas import OPERATION_MAX_VALUE, OPERATION_DATE_FORMAT


@validate_arguments(config=pydantic_config)
def get_all_operations(db: SQLAlchemy, filters: dict = None):
    """Get list of all operations

    Params
    --------------
    - filter : `dict`
        * Dictionary of filter options

    Filter options
    --------------
    - date_from : `str`
        * filter operations from date. Format: `YYYY-MM-DD HH:MM:SS`
    - date_to : `str`
        * filter operations to date. Format: `YYYY-MM-DD HH:MM:SS`
    - category_id : `int`
        * filter operations by category id
    - operation_type : `CategoryType` | `int`
        * filter operation by operation type. Accepts: [1 (income), 2 (expense), CategoryType]
    """

    operations = db.session.query(Operation)

    if filters:
        # Validating filters
        val_filters = OperationFilters.parse_obj(filters)

        # Applying filters
        if val_filters.date_from:
            operations = operations.filter(Operation.date >= val_filters.date_from)

        if val_filters.date_to:
            operations = operations.filter(Operation.date <= val_filters.date_to)

        if val_filters.category_id:
            operations = operations.filter(Operation.category_id == val_filters.category_id)

        if val_filters.type:
            operations = operations.filter(Operation.category.has(Category.type==val_filters.type))

    return operations


@validate_arguments(config=pydantic_config)
def get_operation(db: SQLAlchemy, op_id: int) -> Operation:
    """Get operation by id

    Params
    ------
    - c_id : `int`
        * ID of the operation
    """

    operaion = db.session.query(Operation).filter(Operation.id==op_id).first()

    if operaion is None:
        raise ValueError("Operation not found!")

    return operaion


@validate_arguments(config=pydantic_config)
def create_operation(db: SQLAlchemy, value: float, category: Category) -> Operation:
    """Create new operation

    Params
    ------
    - value : `float`
        * Value of new operation (Max value = `+/-999,999,999.9999`)
        * For income category value should be positive, for expense category value should be negative
    - category: `Category`
        * Category of new operation
    """

    # Validating values
    if category.type == CategoryType.INCOME and value < 0:
        raise ValueError("Value of operation for income category cannot be negative")

    if category.type == CategoryType.EXPENSE and value > 0:
        raise ValueError("Value of operation for expense category cannot be positive")

    if abs(value) > OPERATION_MAX_VALUE:
        raise ValueError(f"Max value of operation equals to +/-{OPERATION_MAX_VALUE}")

    new_operation = Operation(value=value, category_id=category.id)
    db.session.add(new_operation)

    return new_operation


@validate_arguments(config=pydantic_config)
def delete_operation(db: SQLAlchemy, op_id: int) -> Operation:
    """Delete operation by its `id`.

    Params
    ------
    - op_id : `int`
        * ID of the operation to delete
    """

    operation = get_operation(db, op_id)
    db.session.delete(operation)

    return operation


@validate_arguments(config=pydantic_config)
def update_operation(db: SQLAlchemy, op_id: int, value: float = None, category: Category = None, date: str = None):
    """Update operation by its `id`.

    Params
    ------
    - op_id : `int`
        * ID of the operation to update
    - value : `float`
        * New value of the operation (Max value = `+/-999,999,999.9999`)
        * For income category value should be positive, for expense category value should be negative
    - category: `Category`
        * New category of the operation (Category should be same type as before update)
    - date : `str`
        * New date of the operation. Format: `YYYY-MM-DD HH:MM:SS`
    """

    operation = get_operation(db, op_id)
    op_category_after_update = category or operation.category

    # Validate update values
    if value is not None and abs(value) > OPERATION_MAX_VALUE:
        raise ValueError(f"Max value of operation equals to +/-{OPERATION_MAX_VALUE}")

    if category is not None and operation.category.type != category.type:
        raise ValueError("Category types should be same!")

    if value and op_category_after_update.type == CategoryType.INCOME and value < 0:
        raise ValueError("Value of operation for income category cannot be negative")

    if value and op_category_after_update.type == CategoryType.EXPENSE and value > 0:
        raise ValueError("Value of operation for expense category cannot be positive")

    if date:
        try:
            date = datetime.strptime(date, OPERATION_DATE_FORMAT)
        except Exception as exc:
            raise ValueError("date format should be: \"YYYY-MM-DD HH:MM:SS\"!") from exc

    # Update operation
    if value:
        operation.value = value

    if category:
        operation.category_id = category.id

    if date:
        operation.date = date

    return operation
