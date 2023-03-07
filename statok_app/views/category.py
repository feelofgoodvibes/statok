from flask import render_template
import requests

API_URL = "http://localhost:5000/api/v1"


def view_categories():
    categories = requests.get(f"{API_URL}/category/stats").json()

    return render_template("categories.html", categories=categories)


def view_category(category_id: int):
    category = requests.get(f"{API_URL}/category/{category_id}").json()

    return render_template("category.html", category=category)
