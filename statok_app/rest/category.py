# pylint: disable=too-many-return-statements, inconsistent-return-statements

from flask import request
from pydantic import ValidationError
import orjson

from statok_app.service import category as service_category
from statok_app.models.database import db
from statok_app.schemas import category as schemas_category
from statok_app.schemas import operation as schemas_operation
from statok_app.rest import api_logger


def api_category_all():
    """View function for URL: `/category`"""

    if request.method == "GET":
        api_logger.debug("GET request at %s. Args: %s; Form: %s", request.full_path, request.args, request.form)

        filter_category_type = request.args.get("type")

        # Convert string to int, because pydantic.validate_arguments decorator
        # can't convert numeric strings to Enum member
        if isinstance(filter_category_type, str) and filter_category_type.isnumeric():
            filter_category_type = int(filter_category_type)

        try:
            categories = service_category.get_all_categories(db, category_type=filter_category_type).all()
            response_data = [orjson.loads(schemas_category.CategoryBase.from_orm(category).json())
                        for category in categories]

            api_logger.debug("Returning %s items", len(response_data))
            return response_data, 200
        except ValidationError as exc:
            api_logger.debug("ValidationError %s", exc.json())
            return { "error": orjson.loads(exc.json().replace("category_type", "type")) }, 400

    elif request.method == "POST":
        api_logger.debug("POST request at %s. Args: %s; Form: %s", request.full_path, request.args, request.form)

        category_type = request.form.get("type")

        if isinstance(category_type, str) and category_type.isnumeric():
            category_type = int(category_type)

        try:
            new_category = service_category.create_category(db,
                                                            name=request.form.get("name"),
                                                            category_type=category_type)
        except ValidationError as exc:
            api_logger.debug("ValidationError %s", exc.json())
            return { "error": orjson.loads(exc.json().replace("category_type", "type")) }, 400

        db.session.commit()

        response_model = schemas_category.Category.from_orm(new_category)
        response_data = orjson.loads(response_model.json())

        api_logger.debug("Item successfully created. Returning item: %s", response_data)
        return response_data, 201


def api_category(category_id: int):
    """View function for URL: `/category/<int: category_id>`"""

    if request.method == "GET":
        api_logger.debug("GET request at %s. Args: %s; Form: %s", request.full_path, request.args, request.form)

        try:
            category = service_category.get_category(db, category_id)
            response_data = orjson.loads(schemas_category.Category.from_orm(category).json())

            api_logger.debug("Return item: %s", response_data)
            return response_data, 200
        except ValueError as exc:
            api_logger.debug("ValueError %s", str(exc))
            return { "error": str(exc) }, 404

    elif request.method == "PUT":
        api_logger.debug("PUT request at %s. Args: %s; Form: %s", request.full_path, request.args, request.form)

        name = request.form.get("name")

        try:
            updated_category = service_category.update_category(db, category_id, name)
        except ValidationError as exc:
            api_logger.debug("ValidationError %s", exc.json())
            return { "error": orjson.loads(exc.json()) }, 400
        except ValueError as exc:
            api_logger.debug("ValueError %s", str(exc))
            return  { "error": str(exc) }, 400

        db.session.commit()
        response_data = orjson.loads(schemas_category.Category.from_orm(updated_category).json())

        api_logger.debug("Item successfully updated. Return item: %s", response_data)
        return response_data, 200

    elif request.method == "DELETE":
        api_logger.debug("DELETE request at %s. Args: %s; Form: %s", request.full_path, request.args, request.form)

        try:
            deleted_category = service_category.delete_category(db, category_id)
        except ValueError as exc:
            api_logger.debug("ValueError %s", str(exc))
            return { "error": str(exc) }, 400

        db.session.commit()
        response_data = orjson.loads(schemas_category.Category.from_orm(deleted_category).json())

        api_logger.debug("Item successfully deleted. Return item: %s", response_data)
        return response_data, 200


def api_category_clear(category_id: int):
    """View function for URL: `/category/<int: category_id>/operation`

    This endpoint ONLY for deleting all operations within category
    """

    if request.method == "DELETE":
        api_logger.debug("DELETE request at %s. Args: %s; Form: %s", request.full_path, request.args, request.form)
        del_operations = service_category.delete_category_operations(db, category_id)
        db.session.commit()

        response_data = [orjson.loads(schemas_operation.OperationBase.from_orm(operation).json())
                         for operation in del_operations]

        api_logger.debug("Return %s items", len(response_data))
        return response_data, 200


def api_category_stats():
    """View function for URL: `/category/stats`

    This endpoint ONLY for getting statistics of all categories
    """

    if request.method == "GET":
        api_logger.debug("GET request at %s. Args: %s; Form: %s", request.full_path, request.args, request.form)
        response_data = service_category.get_categories_stats(db)

        api_logger.debug("Return %s items", len(response_data))
        return response_data, 200
