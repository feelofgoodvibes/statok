# pylint: disable=too-many-return-statements, inconsistent-return-statements

from flask import request
from pydantic import ValidationError
import orjson

from statok_app.models.database import db
from statok_app.service import operation as service_operation
from statok_app.service import category as service_category
from statok_app.schemas import operation as schemas_operation


def api_operation_all():
    """View function for URL: `/operation`"""

    if request.method == "GET":
        try:
            operations = service_operation.get_all_operations(db, filters=request.args)
            return [orjson.loads(schemas_operation.Operation.from_orm(operation).json())
                        for operation in operations], 200
        except ValidationError as exc:
            return { "error": orjson.loads(exc.json()) }, 400

    elif request.method == "POST":
        try:
            operation_category = service_category.get_category(db, request.form.get("category_id"))

            new_operation = service_operation.create_operation(db,
                                                            value=request.form.get("value"),
                                                            category=operation_category)
        except ValidationError as exc:
            return {"error": orjson.loads(exc.json())}, 400
        except ValueError as exc:
            return {"error": str(exc)}, 400

        db.session.commit()

        response_model = schemas_operation.Operation.from_orm(new_operation)
        return orjson.loads(response_model.json()), 201


def api_operation(operation_id):
    """View function for URL: `/operation/<int:operation_id>`"""

    if request.method == "GET":
        try:
            operation = service_operation.get_operation(db, operation_id)
            return orjson.loads(schemas_operation.Operation.from_orm(operation).json()), 200
        except ValueError as exc:
            return { "error": str(exc) }, 404

    elif request.method == "PUT":
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
            return orjson.loads(response_model.json()), 200
        except ValidationError as exc:
            return {"error": orjson.loads(exc.json())}, 400
        except ValueError as exc:
            return {"error": str(exc)}, 400

    elif request.method == "DELETE":
        try:
            deleted_operation = service_operation.delete_operation(db, operation_id)
            response = orjson.loads(schemas_operation.Operation.from_orm(deleted_operation).json()), 200

            db.session.commit()
            return response
        except ValueError as exc:
            return { "error": str(exc) }, 404
