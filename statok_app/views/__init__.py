import os
from flask import Blueprint, redirect, render_template
from statok_app.views import operation as views_operation
from statok_app.views import category as views_category


# Constructing path to html templates folder
templates_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "templates")
static_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "templates")

# Creating blueprint for web application views
web_application_blueprint = Blueprint("web_application",
                                      __name__,
                                      template_folder=templates_folder,
                                      static_folder=static_folder)

# Add endpoints
web_application_blueprint.add_url_rule("/category", view_func=views_category.view_categories)
web_application_blueprint.add_url_rule("/category/<int:category_id>", view_func=views_category.view_category)

web_application_blueprint.add_url_rule("/operation", view_func=views_operation.view_operations)
web_application_blueprint.add_url_rule("/operation/<int:operation_id>", view_func=views_operation.view_operation)

# Add handler for 404 pages
@web_application_blueprint.app_errorhandler(404)
def views_404_error():
    """View for pages that doesn't exist"""

    return render_template("page404.html"), 404

# Add redirect from `index` to `/operation`
web_application_blueprint.add_url_rule("/", view_func=lambda: redirect("/operation"))
