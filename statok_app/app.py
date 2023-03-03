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

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = MYSQL_DBURI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    # Bluepring registering
    app.register_blueprint(api_blueprint, url_prefix="/api")

    return app


def create_test_app():
    """Initalize app for testing"""

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = MYSQL_TEST_DBURI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)
    
    # Bluepring registering
    app.register_blueprint(api_blueprint, url_prefix="/api")

    return app


if __name__ == "__main__":
    app = create_app()

    app.run(debug=True)