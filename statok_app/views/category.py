from flask import render_template, request
import requests


def view_categories():
    """View for URL: /category"""

    categories = requests.get(f"{request.host_url}/api/v1/category/stats", timeout=5).json()

    return render_template("categories.html", categories=categories)


def view_category(category_id: int):
    """View for URL: /category/<int:category_id>"""

    category = requests.get(f"{request.host_url}/api/v1/category/{category_id}", timeout=5).json()

    return render_template("category.html", category=category)
