from flask import Blueprint

# This instance of a Blueprint that represents the Visit blueprint
visit_blueprint = Blueprint('visit', __name__)

from . import views
