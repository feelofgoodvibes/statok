from typing import Union
from pydantic import validate_arguments

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.orm import Query

from statok_app.models.category import Category, CategoryType
from statok_app.models.operation import Operation
from statok_app.service.operation import get_all_operations
from statok_app.service import pydantic_config


@validate_arguments(config=pydantic_config)
def get_all_categories(db: SQLAlchemy, category_type: CategoryType = None) -> Query:
    """Get list of all categories
    
    Params
    -------
    - category_type : `Optional[int]`
        * Type of the categories
    """

    categories = db.session.query(Category)

    if category_type is not None:
        categories = categories.filter(Category.type==category_type)

    return categories


@validate_arguments(config=pydantic_config)
def get_category(db: SQLAlchemy, c_id: int) -> Category:
    """Get category by id

    Params
    ------
    - c_id : `int`
        * ID of the category
    """

    category = db.session.query(Category).filter(Category.id==c_id).first()

    if category is None:
        raise ValueError("Category not found!")

    return category


@validate_arguments(config=pydantic_config)
def create_category(db: SQLAlchemy, name: str, c_type: CategoryType) -> Category:
    """Create new category

    Params
    ------
    - name : `str`
        * Name of new category
    - c_type: `CategoryType`
        * Type of new category
    """
    if len(name) > 50:
        raise ValueError("Maximum length of category name is 50 characters!")

    same_category_check = (db.session.query(Category)
                                    .filter(Category.name==name,
                                            Category.type==c_type)).first()

    if same_category_check is not None:
        raise ValueError(f"Category with that name and type already exists (Category id = {same_category_check.id})")

    new_category = Category(name=name, type=c_type)
    db.session.add(new_category)

    return new_category


@validate_arguments(config=pydantic_config)
def delete_category_operations(db: SQLAlchemy, c_id: int) -> list[Operation]:
    """Delete all operations withing category by its `id`.

    Params
    ------
    - c_id : `int`
        * ID of the category
    """

    operaions_in_category = get_all_operations(db, {"category_id": c_id})
    deleted_operations = operaions_in_category.all()

    operaions_in_category.delete()

    return deleted_operations


@validate_arguments(config=pydantic_config)
def delete_category(db: SQLAlchemy, c_id: int) -> Category:
    """Delete category by its `id`.
    All operation within its category will be moved to default category "Other"

    Params
    ------
    - c_id : `int`
        * ID of the category to delete
    """

    category = get_category(db, c_id)

    if category.name == "Other":
        raise ValueError("This category cannot be deleted!")

    operaions_in_category = get_all_operations(db, {"category_id": c_id})

    for operation in operaions_in_category:
        operation.category_id = 1 if category.type == CategoryType.INCOME else 2

    db.session.commit()
    db.session.delete(category)

    return category


@validate_arguments(config=pydantic_config)
def update_category(db: SQLAlchemy, c_id: int, name: str) -> Category:
    """Update category by its `id`.

    Params
    ------
    - c_id : `int`
        * ID of the category to update
    - name : `str`
        * New name of the category
    """

    category = get_category(db, c_id)

    if category.name == "Other":
        raise ValueError("This category cannot be edited!")

    if len(name) > 50:
        raise ValueError("Maximum length of category name is 50 characters!")

    category.name = name

    return category


@validate_arguments(config=pydantic_config)
def get_categories_stats(db: SQLAlchemy) -> dict:
    """Get statistics of all categories as dictionary.
    Statistics contains:
    - ID [dict key]
    - Name ["name"]
    - Type ["type"]
    - Sum of all operations within category ["total"]
    - Amount of operations within category ["operations"]
    """

    query = (
        db.session.query(Category.id,
                         Category.name,
                         Category.type,
                         func.sum(Operation.value),
                         func.count(Category.operations)
                ).join(Operation, Category.operations)
                 .group_by(Category.id)
    )

    query_result = query.all()

    stats = { result[0] : {
                            "name": result[1],
                            "type": result[2],
                            "total": float(result[3]),
                            "operations": result[4],
                            } for result in query_result }

    return stats
