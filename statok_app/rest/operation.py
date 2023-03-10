# pylint: disable=too-many-return-statements, inconsistent-return-statements

from flask import request
from pydantic import ValidationError
import orjson

from statok_app.models.database import db
from statok_app.models.operation import Operation
from statok_app.service import operation as service_operation
from statok_app.service import category as service_category
from statok_app.schemas import operation as schemas_operation
from statok_app.rest import api_logger


def api_operation_all():
    """View function for URL: `/operation`
    Methods: `GET`, `POST`
    
    `GET` method arguments
    ----------------------
    - date_from : `str`
        * filter operations from date. Format: `YYYY-MM-DD HH:MM:SS`
    - date_to : `str`
        * filter operations to date. Format: `YYYY-MM-DD HH:MM:SS`
    - category_id : `int`
        * filter operations by category id
    - type :  `int`
        * filter operation by operation type

    `POST` method data
    ------------------
    * value : `float` - value of operation
    * category_id : `int` - category id of operation
    """

    if request.method == "GET":
        api_logger.debug("GET request at %s. Args: %s; Form: %s", request.full_path, request.args, request.form)

        try:
            # Applying filters by passing arguments of requests as filtering dictionary for get_all_operations function
            operations = service_operation.get_all_operations(db, filters=request.args).order_by(Operation.date.desc())

            response_data = [orjson.loads(schemas_operation.Operation.from_orm(operation).json())
                            for operation in operations]

            api_logger.debug("Returning %s items", len(response_data))
            return response_data, 200
        except ValidationError as exc:
            api_logger.debug("ValidationError %s", exc.json())
            return { "error": orjson.loads(exc.json()) }, 400

    elif request.method == "POST":
        api_logger.debug("POST request at %s. Args: %s; Form: %s", request.full_path, request.args, request.form)

        try:
            operation_category = service_category.get_category(db, request.form.get("category_id"))

            new_operation = service_operation.create_operation(db,
                                                            value=request.form.get("value"),
                                                            category=operation_category)
        except ValidationError as exc:
            api_logger.debug("ValidationError %s", exc.json())
            return {"error": orjson.loads(exc.json())}, 400
        except ValueError as exc:
            api_logger.debug("ValueError %s", str(exc))
            return {"error": str(exc)}, 400

        db.session.commit()

        response_model = schemas_operation.Operation.from_orm(new_operation)
        response_data = orjson.loads(response_model.json())

        api_logger.debug("Item successfully created. Return item: %s", response_data)
        return response_data, 201


def api_operation(operation_id):
    """View function for URL: `/operation/<int:operation_id>`
    Methods: `GET`, `PUT`, `DELETE`

    `PUT` method data
    -----------------
    * category_id : `int` - new category of operation
    * value : `float` - value of operation
    * date : `str` - date in format: `YYYY-MM-DD HH:MM:SS`
    """

    if request.method == "GET":
        api_logger.debug("GET request at %s. Args: %s; Form: %s", request.full_path, request.args, request.form)

        try:
            operation = service_operation.get_operation(db, operation_id)
            response_data = orjson.loads(schemas_operation.Operation.from_orm(operation).json())

            api_logger.debug("Return item: %s", response_data)
            return response_data, 200
        except ValueError as exc:
            api_logger.debug("ValueError: %s", str(exc))
            return { "error": str(exc) }, 404

    elif request.method == "PUT":
        api_logger.debug("PUT request at %s. Args: %s; Form: %s", request.full_path, request.args, request.form)

        try:
            if request.form.get("category_id"):
                update_category = service_category.get_category(db, request.form.get("category_id"))
            else:
                update_category = None

            updated_operation = service_operation.update_operation(db,
                                                                   operation_id=operation_id,
                                                                   value=request.form.get("value"),
                                                                   category=update_category,
                                                                   date=request.form.get("date"))
            db.session.commit()

            response_model = schemas_operation.Operation.from_orm(updated_operation)
            response_data = orjson.loads(response_model.json())

            api_logger.debug("Item successfully updated. Return item: %s", response_data)
            return response_data, 200
        except ValidationError as exc:
            api_logger.debug("ValidationError %s", exc.json())
            return {"error": orjson.loads(exc.json())}, 400
        except ValueError as exc:
            api_logger.debug("ValueError %s", str(exc))
            return {"error": str(exc)}, 400

    elif request.method == "DELETE":
        api_logger.debug("DELETE request at %s. Args: %s; Form: %s", request.full_path, request.args, request.form)

        try:
            deleted_operation = service_operation.delete_operation(db, operation_id)
            response_data = orjson.loads(schemas_operation.Operation.from_orm(deleted_operation).json()), 200

            db.session.commit()

            api_logger.debug("Item successfully deleted. Return item: %s", response_data)
            return response_data
        except ValueError as exc:
            api_logger.debug("ValueError %s", str(exc))
            return { "error": str(exc) }, 404
