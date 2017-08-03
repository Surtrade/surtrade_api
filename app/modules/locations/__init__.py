# location/__init__.py


from flask import Blueprint

# This instance of a Blueprint that represents the location blueprint
location_blueprint = Blueprint('location', __name__)

from . import views
