from flask import render_template
import requests

API_URL = "http://localhost:5000/api/v1"


def view_categories():
    """View for URL: /category"""

    categories = requests.get(f"{API_URL}/category/stats", timeout=5).json()

    return render_template("categories.html", categories=categories)


def view_category(category_id: int):
    """View for URL: /category/<int:category_id>"""

    category = requests.get(f"{API_URL}/category/{category_id}", timeout=5).json()

    return render_template("category.html", category=category)
