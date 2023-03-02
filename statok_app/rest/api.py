from flask import Blueprint
from statok_app.rest import category as api_category


# General api blueprint
api_blueprint = Blueprint("api", __name__)

# Category api
api_blueprint.add_url_rule("/category",
                           view_func=api_category.api_category_all,
                           methods=["GET", "POST"])

api_blueprint.add_url_rule("/category/<int:category_id>",
                           view_func=api_category.api_category,
                           methods=["GET", "PUT", "DELETE"])

api_blueprint.add_url_rule("/category/<int:category_id>/operation",
                           view_func=api_category.api_category_clear,
                           methods=["DELETE"])

api_blueprint.add_url_rule("/category/stats",
                           view_func=api_category.api_category_stats,
                           methods=["GET"])
