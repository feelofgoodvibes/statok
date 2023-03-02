# pylint: disable=too-many-return-statements, inconsistent-return-statements

from flask import request
from pydantic import ValidationError
import orjson

from statok_app.service import category as service_category
from statok_app.models.database import db
from statok_app.schemas import category as schemas_category
from statok_app.schemas import operation as schemas_operation


def api_category_all():
    """View function for URL: `/category`"""

    if request.method == "GET":
        filter_category_type = request.args.get("type")

        # Convert string to int, because pydantic.validate_arguments decorator
        # can't convert numeric strings to Enum member
        if isinstance(filter_category_type, str) and filter_category_type.isnumeric():
            filter_category_type = int(filter_category_type)

        try:
            categories = service_category.get_all_categories(db, category_type=filter_category_type).all()
            response = [orjson.loads(schemas_category.CategoryBase.from_orm(category).json())
                        for category in categories], 200
        except ValidationError as exc:
            response = { "error": orjson.loads(exc.json()) }, 400

    elif request.method == "POST":
        try:
            category_fields = schemas_category.CategoryCreate.parse_obj(request.form)
        except ValidationError as exc:
            return { "error": orjson.loads(exc.json()) }, 400

        new_category = service_category.create_category(db,
                                                        name=category_fields.name,
                                                        category_type=category_fields.type)
        db.session.commit()

        response_model = schemas_category.Category.from_orm(new_category)

        response = orjson.loads(response_model.json()), 201

    return response


def api_category(category_id: int):
    """View function for URL: `/category/<int: category_id>`"""

    if request.method == "GET":
        try:
            category = service_category.get_category(db, category_id)
            response = orjson.loads(schemas_category.Category.from_orm(category).json()), 200
        except ValueError as exc:
            response = { "error": str(exc) }, 404

    elif request.method == "PUT":
        name = request.form.get("name")

        if name is None:
            return {"error": "Argument name is required!"}, 400

        try:
            updated_category = service_category.update_category(db, category_id, name)
            db.session.commit()
            response = orjson.loads(schemas_category.Category.from_orm(updated_category).json()), 200
        except ValidationError as exc:
            response = { "error": orjson.loads(exc.json()) }, 400
        except ValueError as exc:
            response =  { "error": str(exc) }, 400

    elif request.method == "DELETE":
        try:
            deleted_category = service_category.delete_category(db, category_id)
            db.session.commit()
            response = orjson.loads(schemas_category.Category.from_orm(deleted_category).json()), 200
        except ValueError as exc:
            response = { "error": str(exc) }, 400

    return response


def api_category_clear(category_id: int):
    """View function for URL: `/category/<int: category_id>/operation`

    This endpoint ONLY for deleting all operations within category
    """

    if request.method == "DELETE":
        del_operations = service_category.delete_category_operations(db, category_id)
        db.session.commit()

        return [orjson.loads(schemas_operation.OperationBase.from_orm(operation).json())
                for operation in del_operations], 200


def api_category_stats():
    """View function for URL: `/category/stats`

    This endpoint ONLY for getting statistics of all categories
    """

    if request.method == "GET":
        return service_category.get_categories_stats(db), 200
