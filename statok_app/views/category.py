import requests
from flask import render_template, request
from statok_app.rest.api import API_URL


def view_categories():
    """View for URL: /category"""

    # Getting data using API endpoint
    # Slicing last char from request.host_url because it ends with slash and API_URL is also begins with slash
    categories = requests.get(f"{request.host_url[:-1]}{API_URL}/category/stats", timeout=5).json()

    return render_template("categories.html", categories=categories)


def view_category(category_id: int):
    """View for URL: /category/<int:category_id>"""

    # Getting data using API endpoint
    category = requests.get(f"{request.host_url[:-1]}{API_URL}/category/{category_id}", timeout=5).json()

    return render_template("category.html", category=category)
