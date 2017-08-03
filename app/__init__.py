# app/__init__.py

from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    # print("stuff "+str(app_config[config_name].GOOGLE_API_KEY))

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # import the authentication blueprint and register it on the app
    from .modules.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .modules.locations import location_blueprint
    app.register_blueprint(location_blueprint)

    from .modules.contracts import contract_blueprint
    app.register_blueprint(contract_blueprint)

    from .modules.users import users_blueprint
    app.register_blueprint(users_blueprint)

    return app
