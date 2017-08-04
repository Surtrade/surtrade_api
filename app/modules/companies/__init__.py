from flask import Blueprint

# This instance of a Blueprint that represents the Contract blueprint
company_blueprint = Blueprint('company', __name__)

from . import views
