# app/__init__.py

from flask_api import FlaskAPI
#from flask-api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

# local import
from instance.config import app_config

# initialize sql-alchemy for interaction with the Database
db = SQLAlchemy()


def create_app(config_name):

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    # console.log("db: ", app.config.)
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # Registering the Catalog API
    from .modules.apiCatalog import apiCatalog_blueprint
    app.register_blueprint(apiCatalog_blueprint)

    # import the authentication blueprint and register it on the app
    from .modules.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Registering all the services provided
    from .modules.locations import location_blueprint
    app.register_blueprint(location_blueprint)

    from .modules.companies import company_blueprint
    app.register_blueprint(company_blueprint)

    from .modules.visits import visit_blueprint
    app.register_blueprint(visit_blueprint)

    from .modules.interests import interest_blueprint
    app.register_blueprint(interest_blueprint)

    from .modules.contracts import contract_blueprint
    app.register_blueprint(contract_blueprint)

    from .modules.users import users_blueprint
    app.register_blueprint(users_blueprint)

    return app
