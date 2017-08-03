from flask import Blueprint

# This instance of a Blueprint that represents the authentication blueprint
contract_blueprint = Blueprint('contracts', __name__)

from . import views
