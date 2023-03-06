from flask import render_template, request
import requests

API_URL = "http://localhost:5000/api/v1"


def view_operations():
    operations = requests.get(f"{API_URL}/operation", params=request.args).json()
    
    if "error" in operations:
        operations = requests.get(f"{API_URL}/operation").json()

    return render_template("_operations.html", operations=operations)


def view_operation(operation_id: int):
    operation = requests.get(f"{API_URL}/operation/{operation_id}").json()

    return render_template("_operation.html", operation=operation)
