from fixtures import api_client
from flask.testing import FlaskClient


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

    for category in response_data:
        assert category["type"].lower() == "income"

    response = api_client.get("/api/category", query_string={"type": "2"})
    response_data = response.json

    assert len(response_data) == 4

    for category in response_data:
        assert category["type"].lower() == "expense"


def test_rest_get_all_categories_filter_wrong(api_client: FlaskClient):
    response = api_client.get("/api/category", query_string={"type": "income"})
    response_data = response.json

    assert response.status_code == 400
    assert "error" in response_data

    response = api_client.get("/api/category", query_string={"type": "random"})
    response_data = response.json

    assert response.status_code == 400
    assert "error" in response_data


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

def test_rest_create_category_wrong_type(api_client: FlaskClient):
    response = api_client.post("/api/category", data={"name": "NewCategory!", "type": "income"})
    response_data = response.json

    assert response.status_code == 400
    assert "error" in response_data


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


def test_rest_update_category_no_name(api_client: FlaskClient):
    response = api_client.put("/api/category/3")

    assert response.status_code == 400
    assert "error" in response.json
    assert response.json["error"] == "Argument name is required!"


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

    response = api_client.delete("/api/category/15")

    assert response.status_code == 400


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