from typing import Optional, Union
from sqlalchemy import func
from sqlalchemy.orm import Query
from flask_sqlalchemy import SQLAlchemy

from statok_app.models.category import Category, CategoryType
from statok_app.models.operation import Operation
from statok_app.service.operation import get_all_operations

# @TODO: add filter by category type
def get_all_categories(db: SQLAlchemy, category_type: Union[str, int, CategoryType] = None) -> Query:
    """Get list of all categories"""

    categories = db.session.query(Category)

    if category_type and (category_type not in (1, 2, 'income', 'expense') and not isinstance(category_type, CategoryType)):
        raise ValueError("Filter category_type accepts only: \"income\" (1) \"expense\" (2) or CategoryType")

    if category_type is not None:
        categories = categories.filter(Category.type==category_type)

    return categories


def get_category(db: SQLAlchemy, c_id: int) -> Optional[Category]:
    """Get category by id

    Params
    ------
    - c_id : `int`
        * ID of the category
    """

    return db.session.query(Category).filter(Category.id==c_id).first()


def create_category(db: SQLAlchemy, name: str, c_type: CategoryType) -> Category:
    """Create new category

    Params
    ------
    - name : `str`
        * Name of new category
    - c_type: `CategoryType`
        * Type of new category
    """

    if not isinstance(c_type, CategoryType):
        raise ValueError("Category type should be instance of CategoryType!")

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


def delete_category(db: SQLAlchemy, c_id: int) -> Category:
    """Delete category by its `id`.
    All operation within its category will be moved to default category "Other"

    Params
    ------
    - c_id : `int`
        * ID of the category to delete
    """

    category = get_category(db, c_id)

    if category is None:
        raise ValueError("Category not found!")

    if category.name == "Other":
        raise ValueError("This category cannot be deleted!")

    operaions_in_category = get_all_operations(db, {"category_id": c_id})

    for operation in operaions_in_category:
        operation.category_id = 1 if category.type == CategoryType.INCOME else 2

    db.session.commit()
    db.session.delete(category)

    return category


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

    if category is None:
        raise ValueError("Category not found!")

    if category.name == "Other":
        raise ValueError("This category cannot be edited!")

    if len(name) > 50:
        raise ValueError("Maximum length of category name is 50 characters!")

    category.name = name

    return category


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
