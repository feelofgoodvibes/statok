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
            response = [orjson.loads(schemas_operation.Operation.from_orm(operation).json())
                        for operation in operations], 200
        except ValidationError as exc:
            response = { "error": orjson.loads(exc.json()) }, 400
    
    elif request.method == "POST":
        try:
            operation_category = service_category.get_category(db, request.form.get("category"))
            operation_dict = {"value": request.form.get("value"), "category": operation_category}
            operation_fields = schemas_operation.OperationCreate.parse_obj(operation_dict)
            
            new_operation = service_operation.create_operation(db,
                                                            value=operation_fields.value,
                                                            category=operation_fields.category)
            db.session.commit()

            response_model = schemas_operation.Operation.from_orm(new_operation)
            response = orjson.loads(response_model.json()), 201
        except ValidationError as exc:
            return {"error": orjson.loads(exc.json())}, 400
        except ValueError as exc:
            return {"error": str(exc)}, 400


    return response


def api_operation(operation_id):
    """View function for URL: `/operation/<int:operation_id>`"""

    if request.method == "GET":
        try:
            operation = service_operation.get_operation(db, operation_id)
            response = orjson.loads(schemas_operation.Operation.from_orm(operation).json()), 200
        except ValueError as exc:
            response = { "error": str(exc) }, 404

    elif request.method == "PUT":
        try:
            if request.form.get("category"):
                update_category = service_category.get_category(db, request.form.get("category"))
            else:
                update_category = None

            update_dict = {
                "value": request.form.get("value"),
                "category": update_category,
                "date": request.form.get("date")
                }

            update_fields = schemas_operation.OperationUpdate.parse_obj(update_dict)
            updated_operation = service_operation.update_operation(db,
                                                                   operation_id=operation_id,
                                                                   value=update_fields.value,
                                                                   category=update_fields.category,
                                                                   date=update_fields.date)
            db.session.commit()

            response_model = schemas_operation.Operation.from_orm(updated_operation)
            response = orjson.loads(response_model.json()), 200
        except ValidationError as exc:
            return {"error": orjson.loads(exc.json())}, 400
        except ValueError as exc:
            return {"error": str(exc)}, 400

    elif request.method == "DELETE":
        try:
            deleted_operation = service_operation.delete_operation(db, operation_id)
            response = orjson.loads(schemas_operation.Operation.from_orm(deleted_operation).json()), 200
            db.session.commit()
        except ValueError as exc:
            response = { "error": str(exc) }, 404

    return response
