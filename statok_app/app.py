import os
from flask import Flask
from flask_migrate import Migrate

from statok_app.models.database import db
from statok_app.models.category import Category, CategoryType
from statok_app.models.operation import Operation

from statok_app.rest.api import api_blueprint


MYSQL_USER = os.environ.get("MYSQL_USER")
MYSQL_PASS = os.environ.get("MYSQL_PASS")
MYSQL_DBNAME = "statok_db"
MYSQL_TEST_DBNAME = "statok_test"

MYSQL_DBURI = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASS}@localhost/{MYSQL_DBNAME}"
MYSQL_TEST_DBURI = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASS}@localhost/{MYSQL_TEST_DBNAME}"

migrate = Migrate()


def create_app():
    """Initalize app with plugins"""

    new_app = Flask(__name__)

    new_app.config["SQLALCHEMY_DATABASE_URI"] = MYSQL_DBURI
    new_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(new_app)
    migrate.init_app(new_app, db)

    # Bluepring registering
    new_app.register_blueprint(api_blueprint, url_prefix="/api")

    return new_app


def create_test_app():
    """Initalize app for testing"""

    test_app = Flask(__name__)

    test_app.config["SQLALCHEMY_DATABASE_URI"] = MYSQL_TEST_DBURI
    test_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(test_app)
    migrate.init_app(test_app, db)

    # Bluepring registering
    test_app.register_blueprint(api_blueprint, url_prefix="/api")

    return test_app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
