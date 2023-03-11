from tests.fixtures import api_client
from flask.testing import FlaskClient
from statok_app.rest.api import API_URL
from requests_mock.mocker import Mocker

BASE_URL = "http://localhost"


def test_category_views(api_client: FlaskClient, requests_mock: Mocker):
    requests_mock.get(f"{BASE_URL}{API_URL}/category/stats", text='{"Test": 1}')
    categories_request = api_client.get(f"/category")

    requests_mock.get(f"{BASE_URL}{API_URL}/category/1", text='{"Test": 1}')
    category_request = api_client.get(f"/category/1")

    assert categories_request.status_code == 200
    assert category_request.status_code == 200


def test_operation_views(api_client: FlaskClient, requests_mock: Mocker):
    operations_mock_text = '''[{"id": 1, "value": 100, "date": "2023-01-01 10:00", "category": {"id": 1, "name": "income", "type": 1}}]'''
    requests_mock.get(f"{BASE_URL}{API_URL}/operation", text=operations_mock_text)
    operations_request = api_client.get(f"/operation")

    requests_mock.get(f"{BASE_URL}{API_URL}/operation/1", text='{"id": 1, "value": 100, "date": "2023-01-01 10:00"}')
    operation_request = api_client.get(f"/operation/1")

    assert operations_request.status_code == 200
    assert operation_request.status_code == 200


def test_operation_filter_view(api_client: FlaskClient, requests_mock: Mocker):
    operations_mock_text = '''[{"id": 1, "value": 200, "date": "2023-01-01 15:00", "category": {"id": 1, "name": "income", "type": 1}}]'''

    requests_mock.get(f"{BASE_URL}{API_URL}/operation", text=operations_mock_text)
    requests_mock.get(f"{BASE_URL}{API_URL}/operation?date_from=20XX-02", text='{"error": "Wrong filter"}')

    operation_request = api_client.get("/operation?date_from=20XX-02")

    assert operation_request.status_code == 200


def test_404(api_client: FlaskClient):
    request_404 = api_client.get("/operations/9999")

    assert '<title>Not found | Statok</title>' in request_404.text