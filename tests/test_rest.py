from fixtures import api_client
from flask.testing import FlaskClient

import logging

# Disable logging when testing rest api
logging.disable(logging.DEBUG)

# REST Category tests --------------------------------

def test_rest_get_all_categories(api_client: FlaskClient):
    response = api_client.get("/api/category")
    response_data = response.json

    assert response.status_code == 200
    assert len(response_data) == 7
    assert response_data[2]["name"] == "Salary" and response_data[2]["type"].lower() == "income"
    assert response_data[3]["name"] == "Transaction" and response_data[3]["type"].lower() == "income"
    assert response_data[4]["name"] == "Food" and response_data[4]["type"].lower() == "expense"


def test_rest_get_all_categories_filter(api_client: FlaskClient):
    response = api_client.get("/api/category", query_string={"type": 1})
    response_data = response.json

    assert response.status_code == 200
    assert len(response_data) == 3
    assert response_data[0]["name"] == "Other"
    assert response_data[1]["name"] == "Salary"
    assert response_data[2]["name"] == "Transaction"

    for category in response_data:
        assert category["type"].lower() == "income"

    response = api_client.get("/api/category", query_string={"type": "2"})
    response_data = response.json

    assert len(response_data) == 4
    assert response_data[0]["name"] == "Other"
    assert response_data[1]["name"] == "Food"
    assert response_data[2]["name"] == "Transaction"
    assert response_data[3]["name"] == "Books"

    for category in response_data:
        assert category["type"].lower() == "expense"


def test_rest_get_all_categories_filter_wrong(api_client: FlaskClient):
    response = api_client.get("/api/category", query_string={"type": "income"})
    response_data = response.json

    assert response.status_code == 400
    assert "error" in response_data
    assert "type" in response_data["error"][0]["loc"]

    response = api_client.get("/api/category", query_string={"type": "random"})
    response_data = response.json

    assert response.status_code == 400
    assert "error" in response_data
    assert "type" in response_data["error"][0]["loc"]


def test_rest_get_category(api_client: FlaskClient):
    response = api_client.get("/api/category/6")
    response_data = response.json

    assert response.status_code == 200
    assert response_data["name"] == "Transaction"
    assert response_data["type"] == "EXPENSE"
    assert len(response_data["operations"]) == 2


def test_rest_get_nonexisting_category(api_client: FlaskClient):
    response = api_client.get("/api/category/12")
    response_data = response.json

    assert response.status_code == 404
    assert "error" in response_data
    assert response_data["error"] == "Category not found!"


def test_rest_create_category(api_client: FlaskClient):
    response = api_client.post("/api/category", data={"name": "NewCategory!", "type": 1})
    response_data = response.json

    assert response.status_code == 201
    assert response_data["name"] == "NewCategory!"

    response = api_client.post("/api/category", data={"name": "NewCategory!", "type": "2"})
    response_data = response.json

    assert response.status_code == 201
    assert response_data["name"] == "NewCategory!"


def test_rest_create_category_max_name(api_client: FlaskClient):
    category_name = "this-is-very-long-category-length-it-is-so-long-that-api-refuses-to-create-it"
    response = api_client.post("/api/category", data={"name": category_name, "type": 1})

    assert response.status_code == 400
    assert "error" in response.json
    assert "name" in response.json["error"][0]["loc"]


def test_rest_create_category_wrong_type(api_client: FlaskClient):
    response = api_client.post("/api/category", data={"name": "NewCategory!", "type": "income"})
    response_data = response.json

    assert response.status_code == 400
    assert "error" in response_data
    assert "type" in response.json["error"][0]["loc"]


def test_rest_update_category(api_client: FlaskClient):
    response = api_client.put("/api/category/3", data={"name": "new_cool_name"})

    assert response.status_code == 200
    assert response.json["name"] == "new_cool_name"
    assert response.json["type"] == "INCOME"


def test_rest_update_category_max_name(api_client: FlaskClient):
    category_name = "this-is-very-long-category-length-it-is-so-long-that-api-refuses-to-create-it"
    response = api_client.put("/api/category/3", data={"name": category_name})

    assert response.status_code == 400
    assert "error" in response.json
    assert "name" in response.json["error"][0]["loc"]


def test_rest_update_category_no_name(api_client: FlaskClient):
    response = api_client.put("/api/category/3")

    assert response.status_code == 400
    assert "error" in response.json
    assert "name" in response.json["error"][0]["loc"]


def test_rest_update_category_error_default(api_client: FlaskClient):
    response = api_client.put("/api/category/1", data={"name": "new_name"})

    assert response.status_code == 400
    assert "error" in response.json
    assert response.json["error"] == "This category cannot be edited!"


def test_rest_delete_category(api_client: FlaskClient):
    categories_before = api_client.get("/api/category").json
    response = api_client.delete("/api/category/4")
    categories_after = api_client.get("/api/category").json

    assert response.status_code == 200
    assert len(categories_before) - len(categories_after) == 1
    assert response.json["name"] == "Transaction"


def test_rest_delete_default_category(api_client: FlaskClient):
    response = api_client.delete("/api/category/1")
    assert response.status_code == 400
    assert "error" in response.json

    response = api_client.delete("/api/category/15")
    assert response.status_code == 400
    assert "error" in response.json


def test_rest_category_clear(api_client: FlaskClient):
    deleted_operations = api_client.delete("/api/category/6/operation")
    category_after_clear = api_client.get("/api/category/6")

    assert len(deleted_operations.json) == 2
    assert len(category_after_clear.json["operations"]) == 0


def test_rest_category_stats(api_client: FlaskClient):
    stats_request = api_client.get("/api/category/stats")
    stats = stats_request.json

    assert stats_request.status_code == 200
    assert stats["1"] == {"name": "Other", "type": "INCOME", "total": 125.0, "operations": 2}
    assert stats["2"] == {"name": "Other", "type": "EXPENSE", "total": 10.0, "operations": 1}
    assert stats["3"] == {"name": "Salary", "type": "INCOME", "total": 100.0, "operations": 1}
    assert stats["4"] == {"name": "Transaction", "type": "INCOME", "total": 250.0, "operations": 1}
    assert stats["5"] == {"name": "Food", "type": "EXPENSE", "total": 15.0, "operations": 1}
    assert stats["6"] == {"name": "Transaction", "type": "EXPENSE", "total": 80.0, "operations": 2}


# REST Operation tests --------------------------------

def test_rest_operation_get_all(api_client: FlaskClient):
    request = api_client.get("/api/operation")
    data = request.json

    assert request.status_code == 200
    assert len(data) == 8
    assert data[0]["value"] == 100
    assert data[1]["value"] == 50
    assert data[2]["value"] == 75
    assert data[3]["value"] == 250


def test_rest_operation_get_all_filters(api_client: FlaskClient):
    # date_from
    filters = {"date_from": "2023-02-20 15:00:00"}
    request = api_client.get("/api/operation", query_string=filters)
    assert request.status_code == 200 and len(request.json) == 5
    assert set([operation['value'] for operation in request.json]) == set([250, 15, 75, 5, 10])
    
    # date_to
    filters = {"date_to": "2023-02-20 17:00:00"}
    request = api_client.get("/api/operation", query_string=filters)
    assert request.status_code == 200 and len(request.json) == 6
    assert set([operation['value'] for operation in request.json]) == set([100, 50, 75, 250, 15, 75])
    
    # date_from + date_to
    filters = {
        "date_from": "2023-02-20 15:20:00",
        "date_to": "2023-02-20 17:25:00"
    }
    request = api_client.get("/api/operation", query_string=filters)
    assert request.status_code == 200 and len(request.json) == 2
    assert set([operation['value'] for operation in request.json]) == set([15, 75])
    
    # category_id
    filters = {
        "category_id": 1
    }
    request = api_client.get("/api/operation", query_string=filters)
    assert request.status_code == 200 and len(request.json) == 2
    assert set([operation['value'] for operation in request.json]) == set([50, 75])

    # category_id as str
    filters = {
        "category_id": "5"
    }
    request = api_client.get("/api/operation", query_string=filters)
    assert request.status_code == 200 and len(request.json) == 1
    assert set([operation['value'] for operation in request.json]) == set([15])

    # operation_type
    filters = {
        "type": 1
    }
    request = api_client.get("/api/operation", query_string=filters)
    assert request.status_code == 200 and len(request.json) == 4
    assert set([operation['value'] for operation in request.json]) == set([100, 50, 75, 250])

    # Complex
    filters = {
        "date_from": "2023-02-20 13:15:00",
        "date_to": "2023-02-20 17:15:11",
        "type": "2"
    }
    request = api_client.get("/api/operation", query_string=filters)
    assert request.status_code == 200 and len(request.json) == 2
    assert set([operation['value'] for operation in request.json]) == set([15, 75])


def test_rest_operation_get_all_wrong_filter(api_client: FlaskClient):
    filters = { "date_from": "2023-02-XX 16:00:00" }
    request = api_client.get("/api/operation", query_string=filters)
    
    assert request.status_code == 400
    assert "error" in request.json
    assert "date_from" in request.json["error"][0]["loc"]

    filters = { "date_to": "2023-02-00 16:00:x1" }
    request = api_client.get("/api/operation", query_string=filters)
    
    assert request.status_code == 400
    assert "error" in request.json
    assert "date_to" in request.json["error"][0]["loc"]

    filters = { "category_id": "R" }
    request = api_client.get("/api/operation", query_string=filters)
    
    assert request.status_code == 400
    assert "error" in request.json
    assert "category_id" in request.json["error"][0]["loc"]

    filters = { "type": "43" }
    request = api_client.get("/api/operation", query_string=filters)

    assert request.status_code == 400
    assert "error" in request.json
    assert "type" in request.json["error"][0]["loc"]


def test_rest_operation_create(api_client: FlaskClient):
    operation_data = {
        "value": 150.26,
        "category_id": 4
    }

    request = api_client.post("/api/operation", data=operation_data)

    assert request.status_code == 201
    assert request.json["value"] == 150.26
    assert request.json["category"]["name"] == "Transaction"


def test_rest_operation_create_empty(api_client: FlaskClient):
    operation_data = {}

    request = api_client.post("/api/operation", data=operation_data)

    assert request.status_code == 400
    assert "error" in request.json


def test_rest_operation_create_wrong_value(api_client: FlaskClient):
    operation_data = {
        "value": 9999999999.22,
        "category_id": 1
    }

    request = api_client.post("/api/operation", data=operation_data)

    assert request.status_code == 400
    assert "error" in request.json
    assert request.json["error"][0]["type"] == "value_error.number.not_le"
    
    operation_data = {
        "value": -9999999999.22,
        "category_id": 2
    }

    request = api_client.post("/api/operation", data=operation_data)

    assert request.status_code == 400
    assert "error" in request.json
    assert request.json["error"][0]["type"] == "value_error.number.not_ge"

    operation_data = {
        "value": "15as",
        "category_id": 2
    }

    request = api_client.post("/api/operation", data=operation_data)

    assert request.status_code == 400
    assert "error" in request.json


def test_rest_operation_create_wrong_category_id(api_client: FlaskClient):
    operation_data = {
        "value": 250,
        "category_id": 9
    }

    request = api_client.post("/api/operation", data=operation_data)

    assert request.status_code == 400
    assert "error" in request.json
    
    operation_data = {
        "value": 250,
        "category": "random"
    }

    request = api_client.post("/api/operation", data=operation_data)

    assert request.status_code == 400
    assert "error" in request.json


def test_rest_operation_create_category_value_conflict(api_client: FlaskClient):
    operation_data = {
        "value": -250,
        "category_id": 1
    }

    request = api_client.post("/api/operation", data=operation_data)

    assert request.status_code == 400
    assert "error" in request.json
    assert request.json["error"] == "Value of operation for income category cannot be negative"
    
    operation_data = {
        "value": 250,
        "category_id": 2
    }

    request = api_client.post("/api/operation", data=operation_data)

    assert request.status_code == 400
    assert "error" in request.json
    assert request.json["error"] == "Value of operation for expense category cannot be positive"


def test_rest_operation_update_value(api_client: FlaskClient):
    update_dict = {
        "value": 1337.0,
    }

    request = api_client.put("/api/operation/3", data=update_dict)

    assert request.status_code == 200
    assert request.json["value"] == 1337.0


def test_rest_operation_update_value_date(api_client: FlaskClient):
    update_dict = {
        "value": 1337.0,
        "date": "2023-02-20 14:00:00"
    }

    request = api_client.put("/api/operation/3", data=update_dict)

    assert request.status_code == 200
    assert request.json["value"] == 1337.0
    assert request.json["date"] == "2023-02-20 14:00:00"


def test_rest_operation_update_date(api_client: FlaskClient):
    update_dict = {
        "date": "2023-01-28 14:50:22",
    }

    request = api_client.put("/api/operation/3", data=update_dict)

    assert request.status_code == 200
    assert request.json["value"] == 75
    assert request.json["date"] == "2023-01-28 14:50:22"


def test_rest_operation_update_category(api_client: FlaskClient):
    update_dict = {
        "category_id": "4",
    }

    request = api_client.put("/api/operation/3", data=update_dict)

    assert request.status_code == 200
    assert request.json["value"] == 75
    assert request.json["category"]["name"] == "Transaction"


def test_rest_operation_update_not_same_category_type(api_client: FlaskClient):
    update_dict = {
        "category_id": "2",
    }

    request = api_client.put("/api/operation/3", data=update_dict)
    assert request.status_code == 400
    assert request.json["error"] == "Category types should be same!"


def test_rest_operation_update_nonexisting_category(api_client: FlaskClient):
    update_dict = {
        "category_id": 12,
    }

    request = api_client.put("/api/operation/3", data=update_dict)
    assert request.status_code == 400
    assert request.json["error"] == "Category not found!"


def test_rest_operation_update_wrong_value(api_client: FlaskClient):
    update_dict = {
        "value": "215a",
    }

    request = api_client.put("/api/operation/3", data=update_dict)
    assert request.status_code == 400
    assert "value" in request.json["error"][0]["loc"]


def test_rest_operation_update_wrong_date(api_client: FlaskClient):
    update_dict = {
        "date": "2022-01-28 XX:01:11",
    }

    request = api_client.put("/api/operation/3", data=update_dict)
    assert request.status_code == 400
    assert "date" in request.json["error"][0]["loc"]


def test_rest_operation_update_clear(api_client: FlaskClient):
    update_dict = {}

    request = api_client.put("/api/operation/3", data=update_dict)
    assert request.status_code == 200
    assert request.json["value"] == 75
    assert request.json["category"]["name"] == "Other"


def test_rest_operation_get(api_client: FlaskClient):
    request = api_client.get("/api/operation/4")

    assert request.status_code == 200
    assert request.json["value"] == 250
    assert request.json["category"]["name"] == "Transaction"


def test_rest_operation_get_nonexisting(api_client: FlaskClient):
    request = api_client.get("/api/operation/15")

    assert request.status_code == 404
    assert request.json["error"] == "Operation not found!"


def test_rest_operation_delete(api_client: FlaskClient):
    operations_before = api_client.get("/api/operation").json
    request = api_client.delete("/api/operation/5")
    operations_after = api_client.get("/api/operation").json

    assert request.status_code == 200
    assert request.json["value"] == 15
    assert len(operations_before) - len(operations_after) == 1


def test_rest_operation_delete_nonexisting(api_client: FlaskClient):
    request = api_client.delete("/api/operation/22")
    assert request.status_code == 404
    assert request.json["error"] == "Operation not found!"
