# agents/__init__.py


from flask import Blueprint

# This instance of a Blueprint that represents the location blueprint
users_blueprint = Blueprint('users', __name__)

from . import views
