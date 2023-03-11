import requests
from flask import render_template, request
from statok_app.rest.api import API_URL


def view_operations():
    """View for URL: /operation"""

    # Get operation with filters, retrieved form request URL
    # Slicing last char from request.host_url because it ends with slash and API_URL is also begins with slash
    operations = requests.get(f"{request.host_url[:-1]}{API_URL}/operation", params=request.args, timeout=5).json()

    # If filters in the URL are wrong - get all operations without filters (default behaviour)
    if "error" in operations:
        operations = requests.get(f"{request.host_url[:-1]}{API_URL}/operation", timeout=5).json()

    return render_template("operations.html", operations=operations)


def view_operation(operation_id: int):
    """View for URL: /operation/<int:operation_id>"""

    operation = requests.get(f"{request.host_url[:-1]}{API_URL}/operation/{operation_id}", timeout=5).json()

    return render_template("operation.html", operation=operation)
